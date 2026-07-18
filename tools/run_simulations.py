#!/usr/bin/env python3
"""Replay schema-blind information-flow fixtures.

The runner knows only actors, opaque information tokens, transfers, and durable
additions/removals. It intentionally knows nothing about a production schema,
ontology, database, API, or state machine.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ACTORS = {"outside", "layer", "store"}
LOCATIONS = ACTORS | {"durable"}
ALLOWED_TRANSFERS = {
    ("outside", "layer"),
    ("layer", "outside"),
    ("layer", "store"),
    ("store", "layer"),
}
DIRECTIONS = {
    ("outside", "layer"): "L->T",
    ("layer", "outside"): "T->L",
    ("layer", "store"): "T->R",
    ("store", "layer"): "R->T",
}
FEASIBILITY = {"plausible", "conditional", "protocol-dependent", "not-executable"}


class TraceError(Exception):
    """A fixture has an impossible or internally inconsistent step."""


def expect_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TraceError(f"{label} must be an object")
    return value


def expect_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise TraceError(f"{label} must be a list")
    return value


def check_known(items: list[str], known: set[str], label: str) -> None:
    unknown = sorted(set(items) - known)
    if unknown:
        raise TraceError(f"{label} references undeclared items: {', '.join(unknown)}")


def effective_holdings(actor: str, holdings: dict[str, set[str]], durable: set[str]) -> set[str]:
    if actor == "store":
        return holdings[actor] | durable
    return holdings[actor]


def replay(path: Path, verbose: bool = False) -> tuple[str, int]:
    try:
        fixture = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TraceError(f"cannot load {path}: {exc}") from exc

    root = expect_mapping(fixture, str(path))
    fixture_id = root.get("id")
    if not isinstance(fixture_id, str) or not fixture_id:
        raise TraceError(f"{path}: id must be a non-empty string")

    title = root.get("title")
    if not isinstance(title, str) or not title:
        raise TraceError(f"{fixture_id}: title must be a non-empty string")

    feasibility = root.get("feasibility")
    if feasibility not in FEASIBILITY:
        allowed = ", ".join(sorted(FEASIBILITY))
        raise TraceError(f"{fixture_id}: feasibility must be one of {allowed}")

    item_map = expect_mapping(root.get("items"), f"{fixture_id}.items")
    known = set(item_map)
    if not known:
        raise TraceError(f"{fixture_id}: items cannot be empty")
    for token, description in item_map.items():
        if not isinstance(token, str) or not token:
            raise TraceError(f"{fixture_id}: every item key must be a non-empty string")
        if not isinstance(description, str) or not description:
            raise TraceError(f"{fixture_id}: item {token} needs a description")

    initial = expect_mapping(root.get("initial"), f"{fixture_id}.initial")
    holdings: dict[str, set[str]] = {actor: set() for actor in ACTORS}
    for actor in ACTORS:
        values = expect_list(initial.get(actor, []), f"{fixture_id}.initial.{actor}")
        check_known(values, known, f"{fixture_id}.initial.{actor}")
        holdings[actor].update(values)
    durable_values = expect_list(initial.get("durable", []), f"{fixture_id}.initial.durable")
    check_known(durable_values, known, f"{fixture_id}.initial.durable")
    durable = set(durable_values)

    steps = expect_list(root.get("steps"), f"{fixture_id}.steps")
    if not steps:
        raise TraceError(f"{fixture_id}: steps cannot be empty")

    seen_step_ids: set[str] = set()
    for index, raw_step in enumerate(steps, start=1):
        step = expect_mapping(raw_step, f"{fixture_id}.steps[{index}]")
        step_id = step.get("id")
        if not isinstance(step_id, str) or not step_id:
            raise TraceError(f"{fixture_id}: step {index} needs a non-empty id")
        if step_id in seen_step_ids:
            raise TraceError(f"{fixture_id}: duplicate step id {step_id}")
        seen_step_ids.add(step_id)

        actor = step.get("actor")
        if actor not in ACTORS:
            raise TraceError(f"{fixture_id}/{step_id}: invalid actor {actor!r}")
        mode = step.get("mode")
        note = step.get("note")
        if not isinstance(mode, str) or not mode:
            raise TraceError(f"{fixture_id}/{step_id}: mode must be a non-empty string")
        if not isinstance(note, str) or not note:
            raise TraceError(f"{fixture_id}/{step_id}: note must be a non-empty string")

        requires = expect_list(step.get("requires", []), f"{fixture_id}/{step_id}.requires")
        derive = expect_list(step.get("derive", []), f"{fixture_id}/{step_id}.derive")
        persist = expect_list(step.get("persist", []), f"{fixture_id}/{step_id}.persist")
        remove = expect_list(step.get("remove", []), f"{fixture_id}/{step_id}.remove")
        for label, values in (
            ("requires", requires),
            ("derive", derive),
            ("persist", persist),
            ("remove", remove),
        ):
            check_known(values, known, f"{fixture_id}/{step_id}.{label}")

        missing = sorted(set(requires) - effective_holdings(actor, holdings, durable))
        if missing:
            raise TraceError(
                f"{fixture_id}/{step_id}: {actor} lacks required information: {', '.join(missing)}"
            )

        holdings[actor].update(derive)

        sends = expect_list(step.get("send", []), f"{fixture_id}/{step_id}.send")
        rendered_directions: list[str] = []
        for send_index, raw_send in enumerate(sends, start=1):
            send = expect_mapping(raw_send, f"{fixture_id}/{step_id}.send[{send_index}]")
            target = send.get("to")
            if target not in ACTORS:
                raise TraceError(f"{fixture_id}/{step_id}: invalid transfer target {target!r}")
            if (actor, target) not in ALLOWED_TRANSFERS:
                raise TraceError(
                    f"{fixture_id}/{step_id}: boundary bypass {actor}→{target} is not allowed"
                )
            sent_items = expect_list(send.get("items"), f"{fixture_id}/{step_id}.send[{send_index}].items")
            check_known(sent_items, known, f"{fixture_id}/{step_id}.send[{send_index}]")
            unavailable = sorted(set(sent_items) - effective_holdings(actor, holdings, durable))
            if unavailable:
                raise TraceError(
                    f"{fixture_id}/{step_id}: {actor} cannot send information it lacks: "
                    + ", ".join(unavailable)
                )
            holdings[target].update(sent_items)
            rendered_directions.append(DIRECTIONS[(actor, target)])

        if persist or remove:
            if actor != "store":
                raise TraceError(f"{fixture_id}/{step_id}: only store steps may change durable items")
            unavailable = sorted(set(persist) - effective_holdings(actor, holdings, durable))
            if unavailable:
                raise TraceError(
                    f"{fixture_id}/{step_id}: store cannot persist information it lacks: "
                    + ", ".join(unavailable)
                )
            missing_remove = sorted(set(remove) - durable)
            if missing_remove:
                raise TraceError(
                    f"{fixture_id}/{step_id}: cannot remove absent durable items: "
                    + ", ".join(missing_remove)
                )
            durable.update(persist)
            durable.difference_update(remove)

        if verbose:
            direction = ",".join(rendered_directions) if rendered_directions else actor
            changes = []
            if derive:
                changes.append(f"derive={len(derive)}")
            if persist:
                changes.append(f"persist={len(persist)}")
            if remove:
                changes.append(f"remove={len(remove)}")
            suffix = f" ({', '.join(changes)})" if changes else ""
            print(f"  {index:02d} {direction:<7} {step_id}: {note}{suffix}")

    expected = expect_mapping(root.get("expected"), f"{fixture_id}.expected")
    expected_has = expect_mapping(expected.get("has", {}), f"{fixture_id}.expected.has")
    expected_not = expect_mapping(expected.get("not_has", {}), f"{fixture_id}.expected.not_has")

    def contents(location: str) -> set[str]:
        if location == "durable":
            return durable
        if location == "store":
            return effective_holdings("store", holdings, durable)
        return holdings[location]

    for label, assertions, should_exist in (
        ("has", expected_has, True),
        ("not_has", expected_not, False),
    ):
        for location, values in assertions.items():
            if location not in LOCATIONS:
                raise TraceError(f"{fixture_id}.expected.{label}: invalid location {location!r}")
            checked = expect_list(values, f"{fixture_id}.expected.{label}.{location}")
            check_known(checked, known, f"{fixture_id}.expected.{label}.{location}")
            present = contents(location)
            failed = sorted((set(checked) - present) if should_exist else (set(checked) & present))
            if failed:
                verb = "missing" if should_exist else "unexpectedly present"
                raise TraceError(
                    f"{fixture_id}.expected.{label}.{location}: {verb}: {', '.join(failed)}"
                )

    response = expected.get("response")
    if not isinstance(response, str) or response not in known:
        raise TraceError(f"{fixture_id}.expected.response must name one declared item")
    if response not in holdings["outside"]:
        raise TraceError(f"{fixture_id}: expected response {response} never reached outside")

    return f"{fixture_id}: {title}", len(steps)


def find_fixtures(root: Path, selected: list[str]) -> list[Path]:
    fixtures_dir = root / "simulations" / "fixtures"
    paths = sorted(fixtures_dir.glob("*.json"))
    if selected:
        wanted = set(selected)
        paths = [path for path in paths if path.stem in wanted]
        missing = sorted(wanted - {path.stem for path in paths})
        if missing:
            raise TraceError(f"unknown fixture(s): {', '.join(missing)}")
    if not paths:
        raise TraceError(f"no fixtures found in {fixtures_dir}")
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", nargs="*", help="fixture stem(s); default is every fixture")
    parser.add_argument("--verbose", action="store_true", help="print every replayed step")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    try:
        paths = find_fixtures(repo_root, args.fixture)
    except TraceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    failures = 0
    total_steps = 0
    for path in paths:
        try:
            label, steps = replay(path, verbose=args.verbose)
            total_steps += steps
            print(f"PASS {label} ({steps} steps)")
        except TraceError as exc:
            failures += 1
            print(f"FAIL {path.name}: {exc}", file=sys.stderr)

    if failures:
        print(f"{failures} of {len(paths)} fixtures failed", file=sys.stderr)
        return 1
    print(f"Validated {len(paths)} fixtures and {total_steps} explicit steps.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
