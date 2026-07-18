# Provisional behavior model

This model extracts testable behavior from the [workflow simulations](workflows.md). It is not a settled architecture or one universal state machine. The state names below are working language for simulations and can be replaced when examples expose better distinctions.

References such as `T055` point to the stable entries in the [verbatim origin conversation](../source/origin-conversation-verbatim.md).

The source conversation asks for a narrow, stateless translation layer inside the knowledge boundary (`T055–T060`), warns that encoding and organization matter as much as retrieval (`T061`), and asks that states be discovered through step-by-step simulations rather than selected in advance (`T061`).

## Provisional roles

- **Human:** supplies intent, decisions, corrections, questions, and approval where needed.
- **Work agent:** operates in the outside world and submits evidence or context requests. It does not need knowledge-store structure or credentials.
- **Translation layer:** interprets one bounded request, retrieves relevant durable state, performs the required semantic steps, returns a result, and terminates.
- **Store-side enforcement:** a possible place for stronger deterministic checks beneath the translation layer. Which checks belong there is a question for the traces, not a decision here.
- **Knowledge store:** retains original sources, interpreted knowledge, organization, and history. This describes responsibility, not a chosen product or data model.

`T057–T060` support the separation between a broadly capable work agent and a narrowly equipped internal layer. `T043–T052` support reusable knowledge, source retention, and agent-focused retrieval.

## Observable phases of one invocation

Not every request uses every phase.

1. **Receive:** take intent, evidence or question, scope, and caller context.
2. **Scope:** determine whether the invocation is a read, write, correction, organization request, or a combination.
3. **Resolve:** map plain-language references to existing subjects or expose ambiguity.
4. **Inspect:** load only the durable state needed to interpret this request.
5. **Interpret:** distinguish observation, decision, correction, inference, relationship, and question as the example requires.
6. **Plan:** form a bounded read or mutation operation.
7. **Validate:** check the proposed operation against current store state.
8. **Apply:** attempt the proposed operation and make its observable outcome available.
9. **Project:** return a bounded context capsule, change result, conflict, or failure explanation.
10. **End:** discard invocation context; continued state lives in the store.

This sequence is a starting hypothesis drawn partly from the assistant proposal in `T060`; it is retained only so simulations can challenge it. “Interpret” is intentionally broader than retrieval because `T061` calls out encoding, storage, organization, and reconciliation as the uncertain work.

## Persistent distinctions exposed by the workflows

- **Retained source versus interpretation:** when original evidence is retained, it stays referable even when a later interpretation changes; the traces still decide when retention occurs.
- **Observation versus decision:** live configuration does not automatically become accepted policy; the ARC example in `T040–T042` demonstrates the difference.
- **Current versus historical:** correction changes what is returned as current without deleting how the earlier belief arose.
- **Direct support versus inference:** knowledge grounded in submitted evidence or an explicit decision remains distinguishable from a relationship suggested by interpretation.
- **Content versus organization:** one knowledge piece can be reachable through several contexts without copying its content (`T043–T048`).
- **Durable knowledge versus context capsule:** the returned task narrative is a bounded projection, not automatically a new canonical fact (`T046–T052`).
- **Repeated request versus new request:** traces need to discover what evidence, if any, lets the layer distinguish a repeat from a new submission.
- **Accepted state versus retained input:** a failed interpretation may still leave its original evidence available, but the boundary between those outcomes remains an explicit design question.

## Separate candidate lifecycles

The workflows reveal several different things that change over time. Combining them into one state machine would hide important failure cases.

### Request invocation

```text
received
  → scoped
      → needs clarification → response returned → ended
      → resolved
          → answered → response returned → ended
          → proposed
              → applied → response returned → ended
              → unchanged → response returned → ended
              → rejected → response returned → ended
              → indeterminate → response returned → ended
```

- A read can move from `resolved` directly to `answered`.
- A write reaches `proposed` before any accepted change.
- A repeated request may return an earlier outcome without applying another change.
- `indeterminate` covers a lost or unclear earlier outcome that needs inspection, not blind replay.

### Source or evidence

```text
submitted
  → rejected as unusable
  → retained → interpreted → reinterpreted as later context improves
```

- Retention preserves what was supplied.
- Interpretation is derived and can change without rewriting the source.
- The simulations still need to decide whether retention and accepted interpretation happen together or separately.

### Interpreted claim

```text
candidate
  → rejected
  → accepted as current → qualified | superseded | reaffirmed
  → held as uncertain → qualified | accepted as current | rejected
  → in conflict → qualified | accepted as current | rejected
```

- “Candidate” prevents extraction from becoming truth merely because it was produced.
- Conflict can coexist with useful retrieval.
- Qualification handles “observed configuration, not accepted policy” without pretending the observed value disappeared.

### Relationship or organization

```text
suggested
  → rejected
  → accepted → revised or superseded
  → kept provisional → accepted | rejected | revised
```

- Organizational changes have their own evidence and history.
- Linking the same knowledge into another context does not create another copy of its content.

### Candidate change outcome

```text
proposed
  → rejected before change
  → applied → result returned
  → partially observed → inspection needed
  → outcome unknown → inspection or reconciliation needed
```

- The traces still need to decide whether related semantic changes are all-or-nothing or may have explicit intermediate outcomes.
- A reported success needs observable support, but its exact durable form remains open.
- Whether source retention and interpretation happen together or separately remains open.

### Context response

```text
requested
  → selected
  → assembled
  → returned
  → expired
```

- The response is tailored to a task, time, scope, and budget.
- Its prose can expire while the cited durable knowledge remains available.
- Missing or conflicting state survives assembly as uncertainty rather than disappearing from the answer.

## Candidate simulation checks

The future traces can test these hypotheses. They are not settled acceptance requirements:

- An outside agent can submit plain-language evidence without constructing store records.
- A bounded internal invocation ends after returning an answer or change result.
- A repeated submission exposes whether it created another durable result and why.
- A repeat with changed content exposes whether the layer recognized the difference and what evidence it used.
- A failed multi-part change exposes every observed effect and any remaining uncertainty.
- A correction preserves the earlier source and changes the current reading.
- Conflicting evidence remains visible until some later evidence or decision resolves it.
- Linking one piece into several contexts does not copy the piece.
- A context capsule fits its requested scope and still exposes material uncertainty.
- A destructive-boundary answer remains unproven when required verification evidence is missing.

## Questions to settle through traces

- Is evidence retention part of the same accepted change as interpreted knowledge, or a separate step?
- What exact event promotes a candidate interpretation to accepted current knowledge?
- How does an explicit human decision differ from a direct live observation at write time?
- Can provisional relationships affect normal retrieval, and how are they labeled when they do?
- Does repeat handling need an explicit identity, and if so, what creates and owns it?
- What inspection can resolve an unknown earlier outcome without duplicating it?
- When does an assembled answer become worth retaining as new source material?
- Which lifecycle distinctions survive several unrelated domains beyond N5?

Those answers emerge from golden traces and adversarial variants. Only then is there enough evidence to name components, select storage, or turn these provisional lifecycles into executable state machines.
