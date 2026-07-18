# Simulation plan

## Purpose

This is the gate between the initial workflow stories and any software architecture. The source asks us to preserve the conversation, write primitive step-by-step examples, pressure-test them, and derive possible states from what happens before choosing components or writing production code. ([T061](../source/origin-conversation-verbatim.md#t061---user), [T062](../source/origin-conversation-verbatim.md#t062---assistant), [T063](../source/origin-conversation-verbatim.md#t063---user), [T064](../source/origin-conversation-verbatim.md#t064---assistant))

The first simulations are reviewable Markdown **golden traces**. A later phase may replay accepted traces in an in-memory reference harness. Neither phase chooses a database, graph model, ontology, API, framework, permanent component name, or production implementation.

## Order of work

1. Convert each [workflow simulation](workflows.md) into one normal golden trace and the applicable adversarial variants.
2. Review each trace for the intended behavior, not for implementation realism.
3. Compare traces and extract provisional distinctions, invariants, operations, and candidate states. Every candidate points back to the trace that required it.
4. Revise the traces when the [provisional behavior model](behavior-model.md) cannot explain an outcome cleanly. The traces are evidence for the model, not generated examples forced to conform to it.
5. Once the traces stabilize, encode them as fixtures for a small in-memory reference harness.
6. Compare architecture and backend options only after the gate at the end of this document is met.

## Golden trace format

Every trace uses these exact top-level fields. Values may be prose, bullets, or small tables; the field names remain stable so that traces can later become fixtures.

```yaml
trace_id:
purpose:
source_anchors:
starting_knowledge:
submission:
  actor:
  intent:
  evidence:
  scope:
  request_id:
interpretation:
  understood:
  resolved_references:
  unresolved_references:
  uncertainty:
proposed_changes:
checks:
outcome:
resulting_knowledge_diff:
returned_result:
observable_acceptance_signals:
open_questions:
```

Field meanings:

- `trace_id`: stable fixture identity, not a production identifier.
- `purpose`: the single behavior or risk the trace is intended to expose.
- `source_anchors`: transcript, evidence, or prior-trace references from which the example was derived.
- `starting_knowledge`: only the durable facts, interpretations, links, history, and request results relevant before this interaction.
- `submission`: what crossed the boundary. `request_id` is present when retry or concurrency behavior matters and is otherwise `not supplied`.
- `interpretation`: what the mediation behavior believes the submission means, including unresolved identity and uncertainty. It is separate from the submitted evidence.
- `proposed_changes`: abstract changes such as retain, add, link, supersede, or leave unchanged. It contains no database syntax or assumed schema.
- `checks`: the preconditions, ambiguities, conflicts, retry checks, and invariants evaluated before the outcome.
- `outcome`: exactly one of `commit`, `reject`, `no_op`, or `needs_clarification`. Here `commit` means the logical all-or-nothing outcome of the trace, not a chosen database mechanism.
- `resulting_knowledge_diff`: the observable before/after change, including retained history. Use `none` when accepted knowledge does not change.
- `returned_result`: bounded context, receipt, clarification request, or error returned to the caller.
- `observable_acceptance_signals`: facts a reviewer or harness can check without inspecting a future implementation.
- `open_questions`: undecided behavior exposed by the trace. An empty list means the trace is understood, not that a product design is complete.

Trace-writing rules:

- Preserve submitted material and derived interpretation as separate entries.
- Show every durable change; do not hide cleanup, replacement, or linking in prose.
- Describe knowledge behavior without product nouns, table names, node labels, or transport details.
- Keep uncertainty, conflict, and missing information visible rather than inventing a resolution.
- For deterministic cases, the same starting knowledge and same submission produce the same logical outcome.
- A correction may change what is current without erasing the earlier source or how the earlier interpretation arose.
- A trace may reveal several lifecycles. Do not force request handling, source retention, interpreted claims, organization, and returned context into one state machine.

## Scenario and adversarial matrix

The normal cases establish the desired utility. Their adversarial variants test whether that utility survives missing, misleading, duplicated, reordered, conflicting, or interrupted input.

| ID | Input pressure | Expected observable result | What the trace teaches us |
| --- | --- | --- | --- |
| S01 | Submit a new N5 observation that ARC is currently capped at 2 GiB | The observation and its source are retained; it is not silently promoted into a hardware requirement or permanent policy | How evidence, interpretation, and decision differ |
| S02 | Ask for only the storage facts needed for an N5 tuning task | The result is bounded to the task, includes relevant uncertainty and provenance, and does not expose unrelated metadata | How retrieval scope and context projection work |
| S03 | Correct a previously accepted but wrong belief | The current answer changes while the prior belief, source, and correction chain remain traceable | What correction and supersession mean |
| S04 | Submit evidence whose subject could be either of two similarly named entities | No entity is guessed; the result asks for the minimum useful clarification or safely retains unresolved evidence | Where resolution ends and clarification begins |
| S05 | Submit two credible sources that disagree | Both sources and the disagreement remain visible; no false single truth is manufactured | How conflict differs from correction |
| S06 | Retry an identical submission with the same request identity | No duplicate durable change is created and the prior logical result can be returned | What idempotency requires |
| S07 | Reuse a request identity with different content | The mismatch is rejected or surfaced; it is not treated as the earlier request | How identity and semantic content interact |
| S08 | Deliver a correction before the evidence or assertion it refers to | The result is safe and explicit: defer, clarify, or retain an unresolved relation without fabricating the missing target | Which order dependencies are real |
| S09 | Fail after some proposed changes but before the logical operation is complete | Accepted knowledge is unchanged, or an explicit recoverable/indeterminate result is observable; no hidden partial state appears | What atomicity and recovery behavior are required |
| S10 | Link one knowledge piece into N5, general storage, and inference contexts | One piece remains authoritative while several contexts can reach it; no copied claims drift apart | How content differs from organization |
| S11 | Assemble a task-specific explanation from several stored pieces | The result is useful and traceable, while the assembled narrative is not silently stored as a new canonical fact | How projections differ from durable knowledge |
| S12 | Submit evidence with no usable source or provenance | The missing basis is visible and the outcome follows an explicit rule; confidence is not invented | What minimum traceability is needed |
| S13 | Supply plausible evidence that invites an incorrect interpretation | The source survives unchanged; the bad interpretation is rejected by checks or can later be corrected without rewriting the source | Which semantic checks can be observed |
| S14 | Submit contradictory facts with different dates and authority | The outcome retains time and authority distinctions and does not flatten them into arrival order | What “current” can legitimately mean |
| S15 | Read while a concurrent correction changes the relevant knowledge | The response identifies a coherent revision or explicitly reports a stale/conflicting result | Whether revision awareness is required |
| S16 | Use the same words for different scopes or entities | Scope is resolved from supplied context or clarification is requested; accidental cross-linking does not occur | What context is necessary for interpretation |
| S17 | Request deletion that would erase the only source or correction history | The source/history-preservation consequence is surfaced and the resulting behavior is explicit | Which history is non-discardable and why |
| S18 | Request an unsupported classification or state transition | No invented type or illegal transition becomes accepted knowledge; the reason is returned | Whether explicit contracts or state constraints are needed |

Each row becomes at least one trace. Rows may be combined only when the resulting trace still has one clear purpose and every acceptance signal remains independently observable.

## Acceptance signals across the trace set

The trace set is ready for mechanization when reviewers can observe all of the following without assuming a backend:

- A reader can reconstruct what entered, how it was interpreted, what was proposed, and what changed.
- Original evidence is distinguishable from derived interpretation and later correction.
- No accepted mutation, loss, or reorganization is silent.
- An exact retry does not create a second durable result; a mismatched retry is not mistaken for the first.
- Conflict and uncertainty remain visible until an explicit rule or later evidence resolves them.
- Reordered input has a safe, defined result instead of depending accidentally on arrival timing.
- A failed multi-step change leaves either the starting accepted state or an explicit recoverable/indeterminate status.
- Context returned to a caller is bounded to the request and preserves the basis for important claims.
- Ambiguous identity, scope, or intent produces an explicit clarification path rather than a guess.
- Every proposed state, transition, invariant, and abstract operation cites the trace that made it necessary.
- Reviewers can state why the normal outcome is useful and why each adversarial outcome is safe enough to continue the spike.

## Later in-memory reference harness

The first harness is an executable behavior model, not a product prototype. It is designed to:

- Load the accepted Markdown traces as fixtures or faithful machine-readable counterparts.
- Hold only enough in-memory reference state to express submitted sources, derived knowledge, organization, history, revisions, and request results. These are testing distinctions, not a production schema.
- Replay abstract operations against that state and compare both the resulting diff and returned result with the golden trace.
- Inject failures between abstract steps, reorder submissions, repeat requests, and vary starting revisions.
- Begin with recorded interpretations or deterministic interpreter stubs so that storage and lifecycle behavior can be tested independently of model variability.
- Evaluate optional LLM interpretations separately against the same accepted intent, uncertainty, and proposed-change expectations.
- Add generated action sequences or stateful/model-based tests only after the handwritten traces establish the vocabulary and useful properties.
- Produce a compact replay report that points failures back to the trace field and source anchor involved.

The harness stays disposable. If it starts deciding the database, public API, ontology, or deployment shape, it has crossed the boundary of this phase.

## Gate before architecture or production code

Architecture comparison may begin only when:

- The core and applicable adversarial traces have been written and reviewed.
- Their open behavior questions are either answered or explicitly classified as architecture-independent unknowns for candidate designs to test.
- The provisional behavior model can explain every accepted trace without silently changing the trace.
- Candidate states, transitions, invariants, and operations are trace-derived and still labeled provisional.
- The in-memory harness, once begun, faithfully replays the accepted traces and fault cases.
- The cross-trace acceptance signals above pass, with failures recorded rather than waived by choosing a technology.

The gate produces an approved trace set, a revised behavior model, a list of unresolved questions, and scenario-based criteria for comparing architectures. It does **not** approve a graph database, relational database, document store, ontology, agent framework, model, or API.
