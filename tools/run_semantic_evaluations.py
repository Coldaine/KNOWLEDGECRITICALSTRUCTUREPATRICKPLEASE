#!/usr/bin/env python3
"""Replay fixtures, score reviewed semantic judgments, and persist one result report."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if __package__:
    from tools.run_simulations import TraceError, find_fixtures, replay
else:
    from run_simulations import TraceError, find_fixtures, replay

DEFAULT_RUBRICS = Path("simulations") / "semantic-rubrics.json"
DEFAULT_RESULTS = Path("simulations") / "results" / "latest.json"


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TraceError(f"cannot load {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise TraceError(f"{path} must contain a JSON object")
    return value


def string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise TraceError(f"{label} must contain only non-empty strings")
    return value


def load_semantic_rubrics(path: Path) -> dict[str, Any]:
    root = load_json(path)
    if root.get("version") != 1:
        raise TraceError(f"{path}: version must be 1")
    gate = root.get("gate")
    workflows = root.get("workflows")
    if not isinstance(gate, dict) or not isinstance(workflows, dict) or not workflows:
        raise TraceError(f"{path}: gate and non-empty workflows are required")
    if not isinstance(gate.get("id"), str) or not gate["id"]:
        raise TraceError(f"{path}.gate.id must be a non-empty string")
    required_workflows = string_list(gate.get("required_workflows"), f"{path}.gate.required_workflows")
    unknown = sorted(set(required_workflows) - set(workflows))
    if unknown:
        raise TraceError(f"{path}: gate references unknown workflows: {', '.join(unknown)}")

    seen_cases: set[str] = set()
    for workflow_id, workflow in workflows.items():
        if not isinstance(workflow_id, str) or not isinstance(workflow, dict):
            raise TraceError(f"{path}: invalid workflow entry")
        threshold = workflow.get("pass_threshold")
        if not isinstance(threshold, (int, float)) or isinstance(threshold, bool) or not 0 <= threshold <= 1:
            raise TraceError(f"{workflow_id}: pass_threshold must be between 0 and 1")
        cases = workflow.get("cases")
        if not isinstance(cases, dict) or not cases:
            raise TraceError(f"{workflow_id}: cases must be a non-empty object")
        for case_id, case in cases.items():
            if case_id in seen_cases:
                raise TraceError(f"duplicate semantic case id {case_id}")
            seen_cases.add(case_id)
            if not isinstance(case, dict) or not isinstance(case.get("criteria"), list) or not case["criteria"]:
                raise TraceError(f"{case_id}: criteria must be a non-empty list")
            for criterion in case["criteria"]:
                if not isinstance(criterion, dict) or not isinstance(criterion.get("id"), str):
                    raise TraceError(f"{case_id}: invalid semantic criterion")
                string_list(criterion.get("must_produce"), f"{case_id}/{criterion.get('id')}.must_produce")
                string_list(criterion.get("must_not_produce"), f"{case_id}/{criterion.get('id')}.must_not_produce")
                allowed = criterion.get("allowed_produce")
                if allowed is not None:
                    string_list(allowed, f"{case_id}/{criterion['id']}.allowed_produce")
                mode = criterion.get("mode")
                if mode is not None and (not isinstance(mode, str) or not mode):
                    raise TraceError(f"{case_id}/{criterion['id']}: mode must be a non-empty string")
                weight = criterion.get("weight", 1.0)
                if not isinstance(weight, (int, float)) or isinstance(weight, bool) or weight <= 0:
                    raise TraceError(f"{case_id}/{criterion['id']}: weight must be positive")
    return root


def semantic_case_index(rubrics: dict[str, Any]) -> dict[str, tuple[str, dict[str, Any]]]:
    return {
        case_id: (workflow_id, case)
        for workflow_id, workflow in rubrics["workflows"].items()
        for case_id, case in workflow["cases"].items()
    }


def produced_tokens(fixture: dict[str, Any], mode: str | None = None) -> set[str]:
    produced: set[str] = set()
    for step in fixture.get("steps", []):
        if mode is not None and step.get("mode") != mode:
            continue
        produced.update(step.get("derive", []))
        produced.update(step.get("persist", []))
    return produced


def score_semantics(path: Path, rubrics: dict[str, Any]) -> dict[str, Any]:
    fixture = load_json(path)
    fixture_id = fixture.get("id")
    index = semantic_case_index(rubrics)
    if fixture_id not in index:
        raise TraceError(f"{fixture_id}: no semantic rubric is defined")
    workflow_id, case = index[fixture_id]
    workflow = rubrics["workflows"][workflow_id]
    known = set(fixture.get("items", {}))
    results = []
    earned = total = 0.0

    for criterion in case["criteria"]:
        criterion_id = criterion["id"]
        weight = float(criterion.get("weight", 1.0))
        must = set(criterion["must_produce"])
        forbidden = set(criterion["must_not_produce"])
        allowed = criterion.get("allowed_produce")
        referenced = must | forbidden | (set(allowed) if allowed is not None else set())
        unknown = sorted(referenced - known)
        if unknown:
            raise TraceError(f"{fixture_id}/{criterion_id}: unknown rubric tokens: {', '.join(unknown)}")
        produced = produced_tokens(fixture, criterion.get("mode"))
        missing = sorted(must - produced)
        forbidden_produced = sorted(forbidden & produced)
        unexpected = sorted(produced - set(allowed)) if allowed is not None else []
        passed = not missing and not forbidden_produced and not unexpected
        total += weight
        earned += weight if passed else 0.0
        results.append({
            "id": criterion_id,
            "weight": weight,
            "passed": passed,
            "missing": missing,
            "forbidden_produced": forbidden_produced,
            "unexpected_produced": unexpected,
        })

    score = earned / total
    threshold = float(workflow["pass_threshold"])
    return {
        "workflow": workflow_id,
        "workflow_title": workflow.get("title", workflow_id),
        "score": score,
        "threshold": threshold,
        "passed": score >= threshold,
        "criteria": results,
    }


def build_gate_report(fixture_results: list[dict[str, Any]], rubrics: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    by_id = {result["id"]: result for result in fixture_results}
    workflow_reports = []
    ready = passed = True
    for workflow_id in rubrics["gate"]["required_workflows"]:
        workflow = rubrics["workflows"][workflow_id]
        required_cases = list(workflow["cases"])
        missing = [case_id for case_id in required_cases if case_id not in by_id]
        cases = [by_id[case_id] for case_id in required_cases if case_id in by_id]
        evaluated = not missing and all(
            case.get("replay", {}).get("passed") and case.get("semantic") is not None for case in cases
        )
        if evaluated:
            score = sum(case["semantic"]["score"] for case in cases) / len(cases)
            workflow_passed = score >= float(workflow["pass_threshold"]) and all(
                case["semantic"]["passed"] for case in cases
            )
        else:
            score = None
            workflow_passed = False
            ready = False
        passed = passed and workflow_passed
        workflow_reports.append({
            "id": workflow_id,
            "title": workflow.get("title", workflow_id),
            "threshold": float(workflow["pass_threshold"]),
            "required_cases": required_cases,
            "missing_cases": missing,
            "evaluated": evaluated,
            "score": score,
            "passed": workflow_passed,
        })
    gate = rubrics["gate"]
    return ({
        "id": gate["id"],
        "evaluated": ready,
        "passed": ready and passed,
        "required_workflows": list(gate["required_workflows"]),
    }, workflow_reports)


def write_results(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", nargs="*", help="fixture stem(s); default is every fixture")
    parser.add_argument("--rubrics", type=Path, help=f"default: {DEFAULT_RUBRICS}")
    parser.add_argument("--results", type=Path, help=f"default: {DEFAULT_RESULTS}")
    parser.add_argument("--no-results", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parent.parent

    try:
        rubrics = load_semantic_rubrics(args.rubrics or repo_root / DEFAULT_RUBRICS)
        paths = find_fixtures(repo_root, args.fixture)
    except TraceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    failures = 0
    fixture_results = []
    total_steps = 0
    for path in paths:
        result: dict[str, Any] = {"id": path.stem}
        try:
            label, steps, feasibility = replay(path, verbose=args.verbose)
            total_steps += steps
            result["replay"] = {"passed": True, "steps": steps, "feasibility": feasibility}
            result["semantic"] = score_semantics(path, rubrics)
            semantic = result["semantic"]
            status = "PASS" if semantic["passed"] else "FAIL"
            print(f"TRACE VALID [{feasibility}] {label} ({steps} steps) | SEMANTIC {semantic['score']:.3f}/{semantic['threshold']:.3f} {status}")
            failures += 0 if semantic["passed"] else 1
        except TraceError as exc:
            result["replay"] = {"passed": False, "error": str(exc)}
            result["semantic"] = None
            failures += 1
            print(f"FAIL {path.name}: {exc}", file=sys.stderr)
        fixture_results.append(result)

    gate, workflows = build_gate_report(fixture_results, rubrics)
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rubric_version": rubrics["version"],
        "fixtures": fixture_results,
        "workflows": workflows,
        "gate": gate,
    }
    if not args.no_results:
        try:
            destination = args.results or repo_root / DEFAULT_RESULTS
            write_results(destination, report)
            print(f"Results written to {destination}")
        except OSError as exc:
            failures += 1
            print(f"FAIL writing results: {exc}", file=sys.stderr)

    if gate["evaluated"]:
        print(f"{gate['id']} GATE {'PASS' if gate['passed'] else 'FAIL'}")
    else:
        print(f"{gate['id']} GATE NOT EVALUATED: run every required workflow case")
    if failures:
        return 1
    print(f"Dataflow-checked and semantically scored {len(paths)} fixtures and {total_steps} steps.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
