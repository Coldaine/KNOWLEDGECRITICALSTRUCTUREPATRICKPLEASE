# Schema-blind simulation fixtures

The fixtures make the [candidate interaction traces](../docs/interaction-traces.md) machine-replayable without choosing a database, ontology, record schema, API, or state machine.

Each fixture contains:

- Opaque information tokens with human-readable meanings.
- What the outside caller, translation layer, and durable side know initially.
- Every transfer across the left or right boundary.
- Every semantic derivation the translation layer attempts.
- Every explicit durable addition or removal.
- Expected returned, durable, and forbidden information.

The separate [`semantic-rubrics.json`](semantic-rubrics.json) file is the reviewed semantic oracle. It groups the 18 cases into the nine workflows, names the judgment each case must make, and gives every workflow an explicit pass threshold.

Run all fixtures with the Python standard library:

```powershell
python tools/run_semantic_evaluations.py
```

Use `--verbose` to print the full left/right replay. Pass one or more fixture stems to run only those cases. A normal full run writes the combined replay and semantic report to `simulations/results/latest.json`; use `--no-results` to suppress it or `--results PATH` to choose another location.

## What the runner checks

### Structural replay

- Every declared step prerequisite is already held by its actor or available to the durable side.
- The outside actor never bypasses the translation layer to manipulate the durable side.
- The translation layer never sends information it does not have.
- The ordered sequence of durable addition/removal events and the one terminal layer-to-outside response match the fixture oracle.
- A failure or ambiguity can remain explicit instead of being filled by hidden context.

### Semantic scoring

- Every fixture has a per-workflow rubric.
- A criterion can require or forbid particular produced tokens.
- For judgment-heavy `mode: semantic` steps, `allowed_produce` can define the exact legal output set. An extra invented judgment therefore fails even if every transfer remains structurally legal.
- Ambiguity cases can require an empty semantic output set, so guessing a correction target or organization target is a deterministic failure.
- Pressure cases that intentionally exercise a bad proposal can instead score the expected enforcement/result behavior.
- A workflow passes only when its mean case score reaches its declared threshold and every required case passes. The current T061 thresholds are all `1.0`.

The T061 gate is evaluated only on a run containing every required case. A subset run can pass its selected cases but reports `T061 GATE NOT EVALUATED`.

## Result shape

`simulations/results/latest.json` records, in one report:

- replay pass/fail, step count, and feasibility for every fixture;
- semantic score, threshold, criterion failures, and workflow for every fixture;
- aggregate workflow scores; and
- whether the T061 gate was evaluated and passed.

Generated result files are ignored by Git; the rubric and fixtures are the reviewed inputs.

## What it still does not prove

- That a real LLM will achieve these semantic judgments reliably over repeated live runs.
- That the fixture author declared every real semantic dependency; undeclared requirements cannot be discovered by token bookkeeping.
- That a real retrieval system will find the required material.
- That the candidate organization is sufficient outside these fixtures.
- Database durability, atomicity, concurrency, authorization, security, or performance.
- That the current trace vocabulary should become a production API or state machine.

A candidate implementation can emit the same normalized observable token events and be scored against these rubrics. The runner and fixtures remain design-spike machinery, not the production data model.
