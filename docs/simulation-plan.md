# Simulation status and next review

This is supporting design-spike evidence. The product is the semantic knowledge boundary described in the [overview](overview.md); the simulations exist only to expose whether that boundary can actually perform the required work.

## Purpose

The simulations make each intermediate dependency visible before any architecture is selected. They test whether the outside caller, short-lived translation layer, and durable side have the information needed for every step. They do not pretend that replaying a trace proves model quality or database behavior. ([T061](../source/origin-conversation-verbatim.md#t061---user))

## First pass completed

- The nine [workflow stories](workflows.md) have been expanded into [candidate interaction traces](interaction-traces.md).
- Every trace records starting durable knowledge, exact left input, left/right transfers, internal semantic judgments, durable effects, returned results, feasibility limits, and a pressure variation.
- Each primary flow and first pressure variation has a separate schema-blind fixture under [`simulations/fixtures`](../simulations/fixtures).
- The dependency-free [replay tool](../tools/run_simulations.py) currently dataflow-checks 18 candidate fixtures and 97 declared steps.
- These traces are implemented, but they are not yet human-accepted golden behavior.

Run the current simulations:

```powershell
python tools/run_simulations.py
```

Use `--verbose` to inspect every boundary crossing.

## What the first pass exposed

| Workflow | Primary case | Pressure case | Main finding |
| --- | --- | --- | --- |
| Record observation | `01-observation-normal` | `01-observation-missing-source` | A model can separate observation from policy, but identity and source binding must be supplied |
| Retrieve task context | `02-context-normal` | `02-context-incomplete-coverage` | Relevance ranking is plausible; safety-critical completeness requires explicit coverage reporting |
| Correct a reading | `03-correction-normal` | `03-correction-ambiguous-target` | Semantic correction is possible only after an exact target and history are available |
| Preserve conflict | `04-conflict-normal` | `04-conflict-unsupported-winner` | Comparing sources is semantic work; choosing a winner requires decisive evidence or an explicit rule |
| Retry a submission | `05-retry-prior-outcome` | `05-retry-indeterminate` | Retry safety is a durable protocol problem, not an LLM inference problem |
| Link and reorganize | `06-link-normal` | `06-link-ambiguous-context` | The model can propose discovery paths; endpoints and durable outcomes must come from tools |
| Handle partial effects | `07-invalid-target-no-effects` | `07-interrupted-partial-outcome` | Generic success/failure is insufficient; every effect and unknown outcome must be observable |
| Answer erase safety | `08-erase-not-established` | `08-erase-supported-no-action` | The model can follow a stored evidence chain; missing retained success cannot be inferred from elapsed activity |
| Discover organization | `09-auto-organize-normal` | `09-auto-organize-ambiguous-subject` | The caller can submit ordinary evidence; the layer can propose organization only after the durable side supplies resolvable subjects, candidate contexts, and retrieval-path limits |

## What the replay tool checks

- Every step names the actor performing it.
- Every declared required information token is already held by that actor or available to the durable side.
- Information can cross only L→T, T→R, R→T, or T→L; the outside caller cannot bypass the translation layer.
- A participant cannot send information it never received or derived.
- Only the durable side can add or remove durable tokens.
- Expected returned, durable, and forbidden tokens match the candidate trace.
- The ordered sequence of durable addition/removal events and the one terminal layer-to-outside response match the fixture oracle.

The fixture items are deliberately opaque. The runner has no entity model, claim schema, relation vocabulary, database query, API, or universal lifecycle.

## What remains unproven

- Whether a real model makes each semantic distinction reliably.
- Whether each fixture author identified every real semantic dependency.
- Whether real retrieval finds the required material with useful latency and coverage.
- Whether the candidate knowledge organization generalizes outside these N5-grounded examples.
- The correct source-retention behavior when interpretation fails.
- Authorization, concurrency, durability, atomicity, idempotency, and recovery mechanisms.
- Whether any candidate state names deserve to become a state machine.

## Review loop

1. Review each [interaction trace](interaction-traces.md) against the verbatim transcript.
2. Correct the trace before correcting its fixture.
3. Change the fixture to match the reviewed trace and run the replay.
4. Add a new case only when it exposes behavior the existing primary and pressure cases do not.
5. Record distinctions that repeat across unrelated domains.
6. Test a real translation model separately from deterministic state or protocol behavior.
7. Compare architecture candidates only after the traces are stable enough to serve as observable acceptance examples.

## Candidate implementation comparison

A future candidate can emit the same observable information transfers and durable outcomes. An adapter can normalize those events to the opaque fixture tokens, then compare them with the reviewed trace. This keeps the behavior examples stable while allowing the database, retrieval method, model, tool surface, and deployment shape to change.

The fixtures are disposable. Their purpose is to expose hidden context and expected outcomes, not to become the production data model.
