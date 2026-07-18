# Simulation plan

## Purpose

The simulations turn the current workflow stories into concrete examples we can challenge before choosing components or writing production code. They are a way to discover behavior, vocabulary, and possible states—not a contract invented in advance. ([T061](../source/origin-conversation-verbatim.md#t061---user), [T063](../source/origin-conversation-verbatim.md#t063---user))

## Order of work

1. Start with one [workflow](workflows.md) and write the interaction step by step.
2. Run the same interaction with one changed condition: missing, incorrect, duplicated, reordered, conflicting, repeated, or interrupted input.
3. Review what we expected to happen, what remains unclear, and whether the workflow itself needs correction.
4. Compare several traces before naming operations, states, or invariants in the [provisional behavior model](behavior-model.md).
5. Preserve each reviewed trace and the questions it exposed.
6. Encode the traces in a small reference harness only after their useful shape becomes clear.

## Starting trace shape

Use this small shape for the first traces. Change it when the examples show that another distinction is needed.

```yaml
trace:
source:
starting_knowledge:
input:
steps:
result:
  stored:
  returned:
questions:
```

- `source` points back to the transcript and workflow that motivated the trace.
- `steps` records what the outside agent, translation layer, and knowledge store each do.
- `stored` describes the visible before-and-after knowledge state without assuming a schema.
- `returned` records the answer, change result, clarification, or failure visible to the caller.
- `questions` keeps undecided behavior explicit instead of filling it in with policy.

## First simulations

| Workflow | Normal example | First pressure variation | What it should help us discover |
| --- | --- | --- | --- |
| Store an observation | Submit the observed N5 ARC setting with its source and qualification | The subject or source is incomplete | What is retained, interpreted, or left unresolved |
| Retrieve context | Ask for the storage knowledge relevant to one N5 task | Relevant sources conflict or the requested context is too broad | How selection, uncertainty, and context limits behave |
| Correct knowledge | Correct an earlier statement while preserving why it existed | The correction arrives before the statement it names | What correction, history, and unresolved reference mean |
| Handle ambiguity or conflict | Submit two plausible interpretations or disagreeing sources | One source later changes or becomes more authoritative | Whether the behavior is clarification, coexistence, correction, or something else |
| Repeat a submission | Retry after the first response is lost | The first outcome is unknown or the repeated content differs | What makes two requests the same and how uncertainty is reconciled |
| Link and reorganize | Make one knowledge piece discoverable from several contexts | One proposed relationship is uncertain | What changes in organization without copying content |
| Handle partial failure | Attempt one interaction that implies several related changes | Failure occurs before the final result is known | Which intermediate states are visible and recoverable |
| Assemble an answer | Build an N5 storage explanation from several pieces | One required fact is missing or stale | What belongs in the returned narrative versus durable knowledge |

Add a scenario only when it exposes behavior that these examples do not. A pressure variation records the result we currently expect and the reason; it does not silently turn that expectation into permanent policy.

## What review should leave behind

- The trace and its source links.
- Any correction to the written workflow.
- Candidate words, distinctions, operations, or states that the trace actually required.
- Questions the trace could not settle.
- A concrete behavior that future architecture candidates can demonstrate or fail.

## Later reference harness

After the Markdown traces stabilize enough to repeat:

- Give each accepted trace a faithful machine-readable counterpart.
- Hold only enough in-memory state to replay the trace; do not treat it as the production schema.
- Record the proposed actions, resulting state change, and returned result.
- Repeat, reorder, or interrupt actions where the written pressure variations call for it.
- Compare the observed result with the reviewed trace and report the first meaningful difference.
- Keep model interpretation tests separable from state-transition tests when that separation helps explain a failure.

The harness is disposable. Its job is to make the expected interactions executable, not to choose the database, ontology, API, component names, or deployment shape.

## Decision point

Architecture work can begin when the reviewed traces make the expected interactions concrete enough to compare candidate designs against them. There is no fixed trace count or preselected state model. Unresolved questions become explicit tests for the candidate designs rather than being hidden by a technology choice. ([T061](../source/origin-conversation-verbatim.md#t061---user))
