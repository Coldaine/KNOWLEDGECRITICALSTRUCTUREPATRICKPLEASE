import json
import tempfile
import unittest
from pathlib import Path

from tools.run_simulations import TraceError, replay


def minimal_fixture() -> dict:
    return {
        "id": "test-fixture",
        "title": "Test fixture",
        "basis": ["test"],
        "feasibility": "conditional",
        "items": {
            "request": "One request",
            "response": "One response",
            "durable.unexpected": "An unexpected durable effect",
        },
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


class ReplayValidationTests(unittest.TestCase):
    def replay_fixture(self, fixture: dict) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "fixture.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            replay(path)

    def test_rejects_non_string_token(self) -> None:
        fixture = minimal_fixture()
        fixture["steps"][0]["requires"] = [{"not": "a token"}]
        with self.assertRaisesRegex(TraceError, "non-empty string item names"):
            self.replay_fixture(fixture)

    def test_rejects_unknown_step_field(self) -> None:
        fixture = minimal_fixture()
        fixture["steps"][1]["requirez"] = fixture["steps"][1]["requires"]
        with self.assertRaisesRegex(TraceError, "unknown fields: requirez"):
            self.replay_fixture(fixture)

    def test_response_must_cross_layer_to_outside_boundary(self) -> None:
        fixture = minimal_fixture()
        fixture["initial"]["outside"].append("response")
        fixture["steps"] = fixture["steps"][:1]
        with self.assertRaisesRegex(TraceError, "layer-to-outside result"):
            self.replay_fixture(fixture)

    def test_rejects_unexpected_durable_addition(self) -> None:
        fixture = minimal_fixture()
        fixture["steps"].insert(
            1,
            {
                "id": "persist-unexpected",
                "actor": "layer",
                "mode": "semantic",
                "note": "Send an effect that the oracle does not expect",
                "requires": ["request"],
                "derive": ["durable.unexpected"],
                "send": [{"to": "store", "items": ["durable.unexpected"]}],
            },
        )
        fixture["steps"].insert(
            2,
            {
                "id": "apply-unexpected",
                "actor": "store",
                "mode": "enforcement",
                "note": "Persist the unlisted effect",
                "requires": ["durable.unexpected"],
                "persist": ["durable.unexpected"],
            },
        )
        with self.assertRaisesRegex(TraceError, "durable addition events differ"):
            self.replay_fixture(fixture)

    def test_rejects_persist_then_remove_hidden_by_final_state(self) -> None:
        fixture = minimal_fixture()
        fixture["steps"].insert(
            1,
            {
                "id": "derive-transient",
                "actor": "layer",
                "mode": "semantic",
                "note": "Derive an unlisted transient effect",
                "requires": ["request"],
                "derive": ["durable.unexpected"],
                "send": [{"to": "store", "items": ["durable.unexpected"]}],
            },
        )
        fixture["steps"].insert(
            2,
            {
                "id": "persist-transient",
                "actor": "store",
                "mode": "enforcement",
                "note": "Persist the transient effect",
                "requires": ["durable.unexpected"],
                "persist": ["durable.unexpected"],
            },
        )
        fixture["steps"].insert(
            3,
            {
                "id": "remove-transient",
                "actor": "store",
                "mode": "enforcement",
                "note": "Remove the transient effect before the final state",
                "requires": ["durable.unexpected"],
                "remove": ["durable.unexpected"],
            },
        )
        with self.assertRaisesRegex(TraceError, "durable addition events differ"):
            self.replay_fixture(fixture)

    def test_rejects_duplicate_response_emission(self) -> None:
        fixture = minimal_fixture()
        fixture["steps"][-1]["send"].append({"to": "outside", "items": ["response"]})
        with self.assertRaisesRegex(TraceError, "final transfer of the final step"):
            self.replay_fixture(fixture)

    def test_rejects_mutation_after_response(self) -> None:
        fixture = minimal_fixture()
        fixture["steps"].append(
            {
                "id": "late-mutation",
                "actor": "store",
                "mode": "enforcement",
                "note": "Attempt a mutation after returning to the caller",
                "requires": [],
            }
        )
        with self.assertRaisesRegex(TraceError, "final transfer of the final step"):
            self.replay_fixture(fixture)


if __name__ == "__main__":
    unittest.main()
