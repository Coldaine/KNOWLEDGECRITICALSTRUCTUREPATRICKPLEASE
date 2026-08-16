import json
import tempfile
import unittest
from pathlib import Path

from tools.run_simulations import replay
from tools.run_semantic_evaluations import (
    build_gate_report,
    score_semantics,
    write_results,
)


def legal_fixture(*, fixture_id: str, derived: list[str], items: list[str]) -> dict:
    item_map = {
        "request": "One request",
        "response": "One response",
    }
    item_map.update({item: item.replace(".", " ") for item in items})
    return {
        "id": fixture_id,
        "title": "Wrong-but-legal semantic fixture",
        "basis": ["test"],
        "feasibility": "conditional",
        "items": item_map,
        "initial": {
            "outside": ["request"],
            "layer": [],
            "store": [],
            "durable": [],
        },
        "steps": [
            {
                "id": "submit",
                "actor": "outside",
                "mode": "transfer",
                "note": "Submit request",
                "requires": ["request"],
                "send": [{"to": "layer", "items": ["request"]}],
            },
            {
                "id": "judge",
                "actor": "layer",
                "mode": "semantic",
                "note": "Make a legal semantic judgment",
                "requires": ["request"],
                "derive": derived,
            },
            {
                "id": "respond",
                "actor": "layer",
                "mode": "response",
                "note": "Return response",
                "requires": ["request"],
                "derive": ["response"],
                "send": [{"to": "outside", "items": ["response"]}],
            },
        ],
        "expected": {
            "has": {"outside": ["response"]},
            "not_has": {},
            "durable_added": [],
            "durable_removed": [],
            "response": "response",
        },
    }


def one_case_rubric(
    fixture_id: str,
    *,
    workflow_id: str,
    must_produce: list[str],
    must_not_produce: list[str] | None = None,
    allowed_produce: list[str] | None = None,
    mode: str | None = None,
    threshold: float = 1.0,
) -> dict:
    return {
        "version": 1,
        "gate": {"id": "T061", "required_workflows": [workflow_id]},
        "workflows": {
            workflow_id: {
                "title": workflow_id,
                "pass_threshold": threshold,
                "cases": {
                    fixture_id: {
                        "criteria": [
                            {
                                "id": "semantic-judgment",
                                "must_produce": must_produce,
                                "must_not_produce": must_not_produce or [],
                                **({"allowed_produce": allowed_produce} if allowed_produce is not None else {}),
                                **({"mode": mode} if mode is not None else {}),
                            }
                        ]
                    }
                },
            }
        },
    }


class SemanticEvaluationTests(unittest.TestCase):
    def score(self, fixture: dict, rubrics: dict) -> dict:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / f"{fixture['id']}.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            replay(path)  # prove the wrong judgment is still structurally legal
            return score_semantics(path, rubrics)

    def test_wrong_but_legal_observation_promoted_to_decision_fails(self) -> None:
        fixture = legal_fixture(
            fixture_id="01-observation-wrong",
            derived=["decision.arc-2g-required"],
            items=["meaning.arc-2g-observation", "decision.arc-2g-required"],
        )
        rubrics = one_case_rubric(
            fixture["id"],
            workflow_id="01-observation",
            must_produce=["meaning.arc-2g-observation"],
            allowed_produce=["meaning.arc-2g-observation"],
            mode="semantic",
        )

        result = self.score(fixture, rubrics)

        self.assertFalse(result["passed"])
        self.assertEqual(
            result["criteria"][0]["missing"],
            ["meaning.arc-2g-observation"],
        )
        self.assertEqual(
            result["criteria"][0]["unexpected_produced"],
            ["decision.arc-2g-required"],
        )

    def test_wrong_but_legal_ambiguous_correction_target_fails(self) -> None:
        fixture = legal_fixture(
            fixture_id="03-correction-wrong",
            derived=["proposal.correct-candidate-a"],
            items=[
                "coverage.target-ambiguous",
                "response.choose-target",
                "proposal.correct-candidate-a",
            ],
        )
        rubrics = one_case_rubric(
            fixture["id"],
            workflow_id="03-correction",
            must_produce=[],
            allowed_produce=[],
            mode="semantic",
        )

        result = self.score(fixture, rubrics)

        self.assertFalse(result["passed"])
        self.assertEqual(result["criteria"][0]["missing"], [])
        self.assertEqual(
            result["criteria"][0]["unexpected_produced"],
            ["proposal.correct-candidate-a"],
        )

    def test_wrong_but_legal_forced_conflict_winner_fails(self) -> None:
        fixture = legal_fixture(
            fixture_id="04-conflict-wrong",
            derived=["meaning.forced-winner"],
            items=[
                "meaning.unresolved-conflict",
                "response.conflict-and-blocker",
                "meaning.forced-winner",
            ],
        )
        rubrics = one_case_rubric(
            fixture["id"],
            workflow_id="04-conflict",
            must_produce=["meaning.unresolved-conflict"],
            allowed_produce=["meaning.unresolved-conflict"],
            mode="semantic",
        )

        result = self.score(fixture, rubrics)

        self.assertFalse(result["passed"])
        self.assertEqual(
            result["criteria"][0]["unexpected_produced"],
            ["meaning.forced-winner"],
        )

    def test_t061_gate_requires_every_case_and_threshold(self) -> None:
        rubrics = {
            "version": 1,
            "gate": {"id": "T061", "required_workflows": ["01", "03"]},
            "workflows": {
                "01": {
                    "title": "Observation",
                    "pass_threshold": 1.0,
                    "cases": {"case-a": {"criteria": []}},
                },
                "03": {
                    "title": "Correction",
                    "pass_threshold": 1.0,
                    "cases": {"case-b": {"criteria": []}},
                },
            },
        }
        case_a = {
            "id": "case-a",
            "replay": {"passed": True},
            "semantic": {"score": 1.0, "passed": True},
        }

        gate, workflows = build_gate_report([case_a], rubrics)
        self.assertFalse(gate["evaluated"])
        self.assertFalse(gate["passed"])
        self.assertFalse(workflows[1]["evaluated"])

        case_b = {
            "id": "case-b",
            "replay": {"passed": True},
            "semantic": {"score": 1.0, "passed": True},
        }
        gate, workflows = build_gate_report([case_a, case_b], rubrics)
        self.assertTrue(gate["evaluated"])
        self.assertTrue(gate["passed"])
        self.assertTrue(all(workflow["passed"] for workflow in workflows))

    def test_combined_result_report_is_persisted(self) -> None:
        report = {
            "fixtures": [
                {
                    "id": "case-a",
                    "replay": {"passed": True},
                    "semantic": {"score": 1.0, "passed": True},
                }
            ],
            "gate": {"id": "T061", "evaluated": True, "passed": True},
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "results" / "latest.json"
            write_results(path, report)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), report)


if __name__ == "__main__":
    unittest.main()
