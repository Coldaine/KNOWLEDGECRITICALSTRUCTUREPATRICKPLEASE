# Trace-derived behavior model

This document records only behavior repeated or exposed by the [candidate interaction traces](interaction-traces.md). It does not define an architecture, API, universal record, or accepted state machine.

The earlier version proposed one broad `receive → scope → resolve → inspect → interpret → plan → validate → apply → project` sequence before the information dependencies were explicit. The user challenged exactly that gap in [T096](../source/origin-conversation-verbatim.md#t096---user). The traces showed that this was too smooth: reads, writes, retries, conflicts, and interrupted effects have different proof obligations and cannot honestly share one simple lifecycle.

## Stable interaction shape

The traces consistently preserve this responsibility split from [T055–T061](../source/origin-conversation-verbatim.md#t055---user):

- **Outside human or work agent:** supplies task intent, evidence, target hints, and useful limits in ordinary language. It does not shape store records or relations.
- **Short-lived translation layer:** decomposes one request, makes bounded semantic judgments, uses only knowledge-side interactions, returns a result, and ends.
- **Durable knowledge side:** resolves stored identities, retrieves bounded material and its limits, evaluates proposed effects, preserves history, and reports observable outcomes.

One invocation may contain several right-side exchanges. The model is stateless between invocations; the durable side is the only continuity assumed.

## Repeated behavior across the candidate traces

Not every trace uses every behavior.

1. **Receive left input.** Intent, evidence or question, target hints, source/time, scope, and response limits arrive when that workflow needs them.
2. **Decompose the semantic problem.** The layer identifies the distinctions and retrieval questions required by this request.
3. **Resolve bounded candidates.** The durable side returns candidate identities or targets, their match basis, ambiguity, and query limits.
4. **Retrieve task material.** The durable side returns only relevant content, history, sources, time, standing, conflicts, relationships, and coverage.
5. **Make a semantic judgment.** The layer compares only supplied material and states any unsupported or ambiguous part.
6. **Propose effects when needed.** A write describes separate semantic effects. It does not claim they happened.
7. **Observe each durable outcome.** The durable side reports accepted, rejected, unchanged, or indeterminate effects separately.
8. **Return left.** The layer returns an answer, effect result, ambiguity, or next evidence and terminates.

Reads normally skip steps 6 and 7. Retry and interruption traces depend more on durable protocol inspection than semantic interpretation.

## Distinctions the traces require

- **Source versus interpretation:** Exact submitted material remains distinguishable from what the layer concluded from it.
- **Observation versus decision:** The live 2 GiB ARC setting is not evidence that 2 GiB is the accepted requirement.
- **Current versus historical:** A correction can change the current reading without erasing the earlier source or interpretation.
- **Direct support versus inference:** A proposed link, winner, or resolution question does not become established knowledge merely because the model produced it.
- **Content versus organization:** One piece can gain several discovery paths without copying its content.
- **Durable knowledge versus task response:** A context capsule or safety answer is not automatically stored as canonical knowledge.
- **Missing versus omitted:** `not found`, truncated, inaccessible, and not searched are different retrieval outcomes.
- **Semantic proposal versus durable effect:** A well-formed interpretation does not prove that any write persisted.
- **Repeated request versus similar request:** Retry identity and prior outcome cannot be reconstructed safely from semantic similarity alone.
- **Rejected versus indeterminate:** A known no-effect result differs from an interrupted result whose effects cannot yet be established.

## Separate candidate lifecycles

The traces expose several different changing things. They should not be collapsed into one state machine.

### Invocation

```text
received
  → needs clarification → returned
  → answerable → returned
  → effects proposed
      → outcomes observed → returned
      → outcome indeterminate → inspection or reconciliation → returned
```

This describes externally visible progress, not an implementation scheduler.

### Retrieval result

Two independent dimensions appear repeatedly:

```text
match: unique | ambiguous | conflicting | absent
coverage: complete-for-request | truncated | inaccessible | not-searched
```

Time and currentness remain attached to the returned material. `absent + complete-for-request` supports a stronger conclusion than `absent + truncated`.

### Proposed effect

```text
proposed → accepted | rejected | unchanged | indeterminate
```

This lifecycle applies to one effect. A multi-effect request can produce a different outcome for each effect unless a future durable contract establishes all-or-nothing behavior. Source retention is reported separately from accepted interpretation.

The invocation also needs an aggregate report derived from its per-effect outcomes:

```text
complete                 every effect has a known accepted or unchanged outcome
rejected                 no requested semantic effect was accepted
partial                  known outcomes are mixed; at least one effect applied and another did not
reconciliation required  one or more effect outcomes remain indeterminate
```

These are candidate response distinctions exposed by the partial-effect traces, not selected transaction states. The aggregate never replaces the per-effect results.

### Knowledge standing

The traces use these distinctions but do not yet define one lifecycle:

- Submitted source can be retained or rejected as unusable.
- An interpretation can be current, historical, qualified, conflicting, or unresolved.
- A relationship can be existing, proposed, accepted, provisional, rejected, or ambiguous.
- A question about missing evidence remains a question; it is not promoted to an observation.

## Behavior corrected by the simulations

- `Resolve` is not an LLM superpower. The layer chooses only among candidates whose distinguishers were returned.
- `Retrieve relevant knowledge` is not sufficient for a safety claim. The result needs category coverage and missing-versus-omitted status.
- `Compare sources` does not authorize a winner. Decisive evidence or an applicable source rule must exist.
- `Retry safely` is not semantic reasoning. It requires durable request identity and outcome inspection.
- `Validate and commit` cannot be one hidden step. Multi-effect and interrupted cases require per-effect outcomes and sometimes reconciliation.
- `Assemble an answer` does not permit the layer to fill source gaps. In the erase trace, a read event without retained success evidence remains `not established`.

## Candidate capabilities exposed on the durable side

These are behavioral needs, not selected tool names:

- Resolve candidates and return the match basis.
- Retrieve by identity, context/relation, time/currentness, history/conflict, source/provenance, and task/operation.
- Report coverage and access limits for every bounded retrieval.
- Drill from an interpretation to exact source material.
- Evaluate a proposed effect against current durable state.
- Return per-effect outcomes and resulting references.
- Inspect prior requests or interrupted effects when the workflow depends on them.

The traces do not say whether one service, several indexes, a graph, relational storage, or another design provides these capabilities.

## Questions still open

- Is unusable raw evidence retained when no interpretation can be accepted?
- What standing lets a work-agent submission change an accepted decision rather than record a competing interpretation?
- When can several supported effects apply even if one effect is ambiguous?
- What durable identity binds a retry to its prior effects and response?
- Which retrieval categories can report meaningful completeness, and within what declared scope?
- How are freshness requirements supplied or derived for different tasks?
- When does a generated response become useful source material for a later submission?
- Which distinctions repeat outside infrastructure and storage examples?

Architecture can target this behavior only after review decides which candidate oracles are correct. The current model is a map of the questions and observable outcomes that the first simulations exposed.
