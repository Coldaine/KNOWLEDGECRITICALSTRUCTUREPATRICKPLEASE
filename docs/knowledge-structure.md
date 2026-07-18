# Knowledge structure: accepted core and candidate implications

## Accepted core

Durable knowledge is made of addressable, reusable pieces and relationships, not facts owned by one document. The same piece can be discovered from N5, storage, a migration, or inference planning without four maintained copies. Pieces can have different shapes, metadata need not appear in normal context, and outside agents interact through the internal semantic boundary rather than manipulating the structure directly. ([T043](../source/origin-conversation-verbatim.md#t043---user), [T046](../source/origin-conversation-verbatim.md#t046---user), [T055](../source/origin-conversation-verbatim.md#t055---user))

That is accepted product intent. The useful granularity, storage representation, and detailed distinctions below remain to be discovered.

## Candidate distinctions to test

The N5 discussion and current assistant-authored traces suggest four concerns that may need to remain distinguishable. They are hypotheses to pressure-test, not a selected schema or user-accepted decomposition.

### 1. Source material

What was actually supplied:

- Command output, document passage, conversation statement, issue, decision, or other evidence.
- Where it came from and when, when those facts matter.
- Enough identity to inspect the source again.

Source material is not automatically true merely because it was retained.

### 2. Interpreted meaning

What the submitted material appears to say in the current context:

- Observation, decision, correction, proposal, relationship, unresolved question, or another useful distinction.
- Subject, scope, time, and qualification only where the meaning needs them.
- Direct support versus inference.

The exact categories remain open. The important behavior is that interpretation does not overwrite the source it came from.

### 3. Organization

How one piece becomes discoverable from several useful contexts:

- Subjects and identities it concerns.
- Operations, decisions, capabilities, or domains where it matters.
- Relationships to other pieces.
- Suggested relationships kept separate from established ones when that difference matters.

Organization can change without copying or rewriting the underlying content.

### 4. Standing and history

How the current reading relates to what came before:

- Current, historical, uncertain, conflicting, qualified, or superseded meaning.
- Corrections that preserve the earlier source and explain the change.
- Competing interpretations that remain visible until evidence or an explicit decision resolves them.
- Observable durable outcomes for proposed changes.

These are not one universal lifecycle. Different knowledge and relationship kinds may need different histories.

## Sparse shape, not universal front matter

Every piece does not need every possible field. A live observation may need time and evidence. A human decision may need standing and rationale. A contextual link may need only two resolved endpoints and why the relationship is supported. ([T046](../source/origin-conversation-verbatim.md#t046---user))

The durable system may maintain revision, indexing, or operational metadata internally. Normal agent reads should receive the content and task-relevant distinctions, not a complete storage record.

Sparse does not mean unfindable. The store and its indexes collectively need to answer the questions the workflows actually ask.

## Candidate retrieval paths exposed by the probes

- **Identity and aliases:** What does `N5`, `tank`, `zfs_arc_max`, or `fourth disk` refer to in this scope?
- **Context and relationships:** What knowledge matters to this host, domain, operation, decision, or task?
- **Time and currentness:** What was true at the requested time, and what is stale or historical?
- **Standing and conflict:** Which meanings are observed, decided, proposed, qualified, or unresolved?
- **Source and provenance:** What exact material supports this interpretation?
- **History and correction:** What changed, what did it replace or qualify, and why did the earlier reading exist?
- **Operation and outcome:** What was proposed, what became durable, and what remains indeterminate?

The current safety-oriented probes suggest that some bounded retrievals may also need to distinguish complete, truncated, inaccessible, and unattempted scopes. Whether that belongs in the general contract remains open.

These paths are behavioral needs, not a choice of graph, relational database, search engine, or ontology.

## Accepted management boundary

Outside work agents should not construct these pieces or relationships directly. They report what they observed, decided, corrected, or need in ordinary task language. ([T055](../source/origin-conversation-verbatim.md#t055---user), [T057](../source/origin-conversation-verbatim.md#t057---user))

The internal translation layer operates with clean context, remains stateless between interactions, uses only knowledge-side tools, and mediates both the write and read sides. Its write-side responsibility includes interpreting, encoding, storing, and organizing knowledge rather than only retrieving it. ([T055](../source/origin-conversation-verbatim.md#t055---user), [T057](../source/origin-conversation-verbatim.md#t057---user), [T059](../source/origin-conversation-verbatim.md#t059---user), [T061](../source/origin-conversation-verbatim.md#t061---user))

## Candidate internal capabilities exposed by the probes

The short-lived internal translation layer:

- Receives one clean request.
- Resolves bounded candidates through knowledge-side tools.
- Interprets evidence and intent with the relevant stored context.
- Proposes encoding, correction, organization, or retrieval effects.
- Receives observable durable outcomes.
- Returns useful language, source pointers, ambiguity, or next evidence.
- Ends without conversational memory.

The layer is not merely a retrieval agent. Its distinctive responsibility includes encoding, storing, organizing, and carrying meaning across the durable boundary in both directions. ([T059](../source/origin-conversation-verbatim.md#t059---user), [T061](../source/origin-conversation-verbatim.md#t061---user))

## Motivating example of why the distinctions matter

```text
Source: authenticated output contains zfs_arc_max=2147483648.
Observation: N5 had a 2 GiB ARC cap at the observation time.
Decision: no permanent ARC allocation has been accepted from that evidence alone.
Diagnosis: the value does not prove why the workload was slow.
Correction: an earlier statement treated live configuration as the accepted resource boundary.
Organization: the observation matters to N5, storage behavior, and inference-resource planning.
```

Flattening those into one `ARC = 2 GiB` fact reproduces the exact failure that prompted this design. ([T040](../source/origin-conversation-verbatim.md#t040---user), [T042](../source/origin-conversation-verbatim.md#t042---assistant))

## Candidate default reading behavior

- Return ordinary task-relevant language rather than raw front matter.
- Include stable operational identifiers, time, standing, uncertainty, and sources when they change the task answer.
- Allow deeper history, relationships, and provenance on demand.
- Do not store every generated answer as a new canonical piece.
- Treat human document rendering as secondary; most consumers are agents. ([T051](../source/origin-conversation-verbatim.md#t051---user))

## Questions still being discovered

- What is the useful granularity of a piece?
- When is shared content truly one piece, and when do context-specific time, scope, or qualification require separate meanings?
- What source material is retained when interpretation fails?
- Which inferred relationships may influence normal retrieval before acceptance?
- What establishes caller standing for an observation, correction, or decision?
- Which retrieval scopes can make meaningful completeness claims?
- What repeated distinctions survive examples outside infrastructure and storage?

The [information-flow model](information-flow.md) shows what crosses the boundary. The [interaction traces](interaction-traces.md) pressure-test whether the knowledge described here is actually available, organized, and sufficient at each intermediate step.

## Not selected

- A database, graph technology, ontology, universal object envelope, relation vocabulary, API, renderer, or permanent component name.
- A requirement that every piece contain the same metadata.
- A claim that automatic linking or semantic mutation is solved.
- A state machine inferred before the traces are reviewed.
