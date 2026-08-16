# Simulation status and next review

This is supporting design-spike evidence. The product is the semantic knowledge boundary described in the [overview](overview.md); the simulations exist only to expose whether that boundary can actually perform the required work.

## Purpose

The simulations make each intermediate dependency visible before any architecture is selected. They test both whether information flow is legal and whether the declared semantic judgments match the reviewed workflow expectations. They still do not pretend that replaying a trace proves model reliability or database behavior. ([T061](../source/origin-conversation-verbatim.md#t061---user))

## Current pass

- The nine [workflow stories](workflows.md) have been expanded into [candidate interaction traces](interaction-traces.md).
- Every trace records starting durable knowledge, exact left input, left/right transfers, internal semantic judgments, durable effects, returned results, feasibility limits, and a pressure variation.
- Each primary flow and first pressure variation has a separate schema-blind fixture under [`simulations/fixtures`](../simulations/fixtures): 18 cases and 97 declared steps.
- The existing dependency-free [replay tool](../tools/run_simulations.py) still checks structural information flow; [`run_semantic_evaluations.py`](../tools/run_semantic_evaluations.py) wraps it and adds semantic scoring plus persisted results.
- [`simulations/semantic-rubrics.json`](../simulations/semantic-rubrics.json) adds a separate per-workflow semantic oracle and explicit pass thresholds.
- A run persists replay and semantic results together in `simulations/results/latest.json` by default.
- These traces are implemented design-spike expectations; they are not yet evidence that a real model achieves the same judgments reliably.

Run the simulations:

```powershell
python tools/run_semantic_evaluations.py
```

Use `--verbose` to inspect every boundary crossing. Use `--no-results` for an ephemeral run.

## What the workflows currently expose

| Workflow | Primary case | Pressure case | Main finding |
| --- | --- | --- | --- |
| Record observation | `01-observation-normal` | `01-observation-missing-source` | Live observation must remain distinct from accepted policy, and source binding is required |
| Retrieve task context | `02-context-normal` | `02-context-incomplete-coverage` | Relevance is not enough; missing or truncated safety coverage must remain explicit |
| Correct a reading | `03-correction-normal` | `03-correction-ambiguous-target` | Qualify the exact current target; ambiguity must stop semantic target selection |
| Preserve conflict | `04-conflict-normal` | `04-conflict-unsupported-winner` | Preserve competing evidence unless decisive evidence or an explicit precedence rule supports a winner |
| Retry a submission | `05-retry-prior-outcome` | `05-retry-indeterminate` | Retry classification depends on durable outcome evidence, not semantic guesswork |
| Link and reorganize | `06-link-normal` | `06-link-ambiguous-context` | Reuse one knowledge piece; ambiguous relationship targets must not be guessed |
| Handle partial effects | `07-invalid-target-no-effects` | `07-interrupted-partial-outcome` | Combined effects and unknown partial outcomes must remain separately observable |
| Answer erase safety | `08-erase-not-established` | `08-erase-supported-no-action` | Evaluate the stored precondition from exact evidence and do not turn an answer into a world action |
| Discover organization | `09-auto-organize-normal` | `09-auto-organize-ambiguous-subject` | Direct and inferred organization need different standing; unresolved subjects stop organization |

## Structural replay vs. semantic evaluation

The structural replay remains schema-blind. It verifies actor holdings, legal boundary crossings, durable event order, forbidden durable effects, and the single terminal response.

The semantic layer deliberately stays just as small:

- The rubric names the tokens a workflow judgment must produce or must not produce.
- `mode: semantic` criteria can also declare `allowed_produce`, the exact set of tokens semantic steps may emit.
- This catches a wrong-but-legal trace that has all required information but classifies an observation as a decision, selects a correction target under ambiguity, forces a conflict winner, or emits another unreviewed semantic judgment.
- Some pressure fixtures intentionally contain a bad proposal to exercise store-side rejection; those criteria score the rejection/result rather than pretending the proposal itself is correct.

This is an oracle over the declared trace semantics. It is not a text classifier and does not introduce a second ontology.

## T061 decision gate

T061 asked for workflows and mini-simulations to be enshrined before architectural choices are made. The harness now has a concrete gate for that point:

1. Every required workflow case must be present in the run.
2. Every case must pass structural replay.
3. Every case must have a semantic rubric result.
4. Each workflow's aggregate score must meet its explicit `pass_threshold`; all nine thresholds are currently `1.0`.
5. Only then does the persisted report mark `T061` as evaluated and passed.

A selected/subset run never opens the gate; it reports that T061 was not evaluated. This prevents a narrow happy-path run from being mistaken for architecture-decision evidence.

## What remains unproven

- Whether a real translation model makes these semantic distinctions reliably across repeated executions and unseen inputs.
- Whether each fixture author identified every real semantic dependency.
- Whether real retrieval finds the required material with useful latency and coverage.
- Whether the candidate knowledge organization generalizes outside these N5-grounded examples.
- The correct source-retention behavior when interpretation fails.
- Authorization, concurrency, durability, atomicity, idempotency, and recovery mechanisms.
- Whether any candidate state names deserve to become a state machine.

## Review loop

1. Review each [interaction trace](interaction-traces.md) against the verbatim transcript.
2. Correct the trace before correcting its fixture.
3. Change the fixture to match the reviewed trace.
4. Change its semantic rubric when—and only when—the reviewed semantic expectation changed.
5. Run the full harness and inspect both structural and semantic results.
6. Add a new case only when it exposes behavior the existing primary and pressure cases do not.
7. Test a real translation model by normalizing its observable events to the same fixture tokens and scoring those events against the same rubrics.
8. Compare architecture candidates only after the full T061 gate passes.

## Candidate implementation comparison

A future candidate can emit the same observable information transfers, semantic decisions, and durable outcomes. An adapter can normalize those events to the opaque fixture tokens, then run both replay and semantic scoring against the reviewed trace. This keeps the behavioral oracle stable while allowing the database, retrieval method, model, tool surface, and deployment shape to change.

The fixtures and runner are disposable. Their purpose is to expose hidden context and expected outcomes, not to become the production data model.
