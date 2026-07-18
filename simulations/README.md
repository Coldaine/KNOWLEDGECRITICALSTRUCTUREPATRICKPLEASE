# Schema-blind simulation fixtures

The fixtures make the [candidate interaction traces](../docs/interaction-traces.md) machine-replayable without choosing a database, ontology, record schema, API, or state machine.

Each fixture contains:

- Opaque information tokens with human-readable meanings.
- What the outside caller, translation layer, and durable side know initially.
- Every transfer across the left or right boundary.
- Every semantic derivation the translation layer attempts.
- Every explicit durable addition or removal.
- Expected returned, durable, and forbidden information.

Run all fixtures with the Python standard library:

```powershell
python tools/run_simulations.py
```

Use `--verbose` to print the full left/right replay. Pass one or more fixture stems to run only those cases.

## What the runner checks

- Every declared step prerequisite is already held by its actor or available to the durable side.
- The outside actor never bypasses the translation layer to manipulate the durable side.
- The translation layer never sends information it does not have.
- Every durable addition/removal event and the one terminal layer-to-outside response match the fixture oracle.
- A failure or ambiguity can remain explicit instead of being filled by hidden context.

## What it does not prove

- That an LLM will make the right semantic judgment.
- That the fixture author declared every real semantic dependency; undeclared requirements cannot be discovered by token bookkeeping.
- That a real retrieval system will find the required material.
- That the candidate organization is sufficient outside these fixtures.
- Database durability, atomicity, concurrency, authorization, security, or performance.
- That the current trace vocabulary should become a production API or state machine.

A later candidate implementation can emit the same observable token flow and be compared with these fixtures. The runner itself is disposable.
