# Workflow simulations

These examples describe behavior to pressure-test before choosing an architecture. They do not select a database, schema, ontology, API, or permanent name for the internal layer.

References such as `T055` point to the stable entries in the [verbatim origin conversation](../source/origin-conversation-verbatim.md).

The participants are deliberately generic:

- **Work agent:** investigates, operates, or plans in the outside world.
- **Translation layer:** a short-lived, bounded interpreter for knowledge reads and writes.
- **Knowledge store:** durable source material, interpreted knowledge, links, history, and store-side enforcement.

The diagrams are interaction flows, not a proposed component diagram. The transcript asks for this behavior-first sequence in `T055–T061` and for explicit simulations before design in `T061`.

## 1. Ingest and store an N5 observation

**Input**

- A work agent reports authenticated output showing `zfs_arc_max=2147483648` on N5.
- It states that this is observed configuration, not an accepted permanent sizing decision.
- The submission includes the evidence, its source, observation time, and a retry identity.

**Steps**

1. The work agent submits the evidence and its plain-language meaning. It does not construct records or links.
2. The translation layer resolves N5, ARC, the observed value, and the distinction between live configuration and policy.
3. It inspects related current knowledge and any earlier statement that treated 2 GiB as settled.
4. It proposes a bounded change that preserves the source, records the observation, and keeps the policy qualification attached.
5. The knowledge store validates and applies the change as one accepted result.
6. The translation layer returns a receipt explaining what was recorded and what was not promoted to a decision.

**Expected result**

- A later retrieval can report both the observed 2 GiB value and the fact that its long-term suitability remains undecided. The original evidence remains traceable.

**Key failure variant**

- If “N5” cannot be resolved or the evidence lacks enough provenance, no current operational fact is silently invented. The response identifies the ambiguity and what would resolve it.

```mermaid
sequenceDiagram
    participant W as Work agent
    participant T as Translation layer
    participant K as Knowledge store
    W->>T: Submit observation, qualification, evidence, and retry identity
    T->>K: Resolve subjects and inspect related knowledge
    K-->>T: Current observations, decisions, and source references
    T->>K: Propose source preservation and interpreted change
    alt Change validates
        K-->>T: Commit result and receipt data
        T-->>W: Recorded observation with policy caveat
    else Identity or evidence is insufficient
        K-->>T: Validation failure
        T-->>W: No accepted change; explain ambiguity
    end
```

Transcript basis: `T040–T042`, `T055–T061`.

## 2. Retrieve bounded context for a task

**Input**

- A work agent asks: “I am diagnosing N5 disk activity. Give me the current storage topology, active safety constraints, and unfinished operations.”
- The request includes task scope, an as-of time, and a context budget.

**Steps**

1. The translation layer interprets the task rather than treating the request as a keyword search.
2. It resolves N5 and retrieves relevant topology, observations, decisions, constraints, operations, conflicts, and source references.
3. It prefers the knowledge relevant to this task and time instead of returning the whole neighborhood or every stored field.
4. It assembles a compact explanation with operational identifiers and provenance only where useful.
5. It returns the context capsule and ends the invocation.

**Expected result**

- The work agent receives enough current context to investigate safely without learning graph queries, storage shapes, or mutation rules.

**Key failure variant**

- If current state is missing, stale, or contradictory, the capsule says so and names the unresolved evidence instead of filling the gap with a confident answer.

```mermaid
sequenceDiagram
    participant W as Work agent
    participant T as Translation layer
    participant K as Knowledge store
    W->>T: Ask with task, scope, as-of time, and budget
    T->>K: Resolve task subjects and retrieve relevant knowledge
    K-->>T: Current, historical, conflicting, and sourced material
    T->>T: Select and assemble task-relevant context
    alt Evidence supports a current answer
        T-->>W: Bounded context capsule
    else State is missing or conflicted
        T-->>W: Bounded capsule with explicit uncertainty
    end
```

Transcript basis: `T046–T052`, `T055–T060`.

## 3. Correct or supersede an earlier belief

**Input**

- A human or work agent states: “The 2 GiB ARC cap is live configuration. It is not an accepted hardware requirement.”
- The submission identifies the earlier belief if known and includes supporting context.

**Steps**

1. The translation layer resolves the correction target and retrieves its history and sources.
2. It distinguishes a correction, a qualification, and a newly observed change.
3. It preserves the earlier statement and proposes the smallest relationship between old and new meanings: replacement, qualification, or coexistence.
4. The knowledge store checks that the target has not changed underneath the request.
5. On success, it records the new interpretation and its relationship to the old one without erasing history.
6. The translation layer returns the new current reading and a receipt describing the history change.

**Expected result**

- Retrieval no longer presents “configured at 2 GiB” as proof that “2 GiB is the accepted requirement,” while an audit can still explain how the mistaken reading arose.

**Key failure variant**

- If several earlier claims could be the target, or the target changed concurrently, the layer returns the candidates or conflict rather than overwriting one by guesswork.

```mermaid
sequenceDiagram
    participant W as Human or work agent
    participant T as Translation layer
    participant K as Knowledge store
    W->>T: Submit correction and supporting context
    T->>K: Resolve target and inspect history
    K-->>T: Candidate target, revisions, and sources
    T->>K: Propose correction, qualification, or supersession
    alt Target is unambiguous and current
        K-->>T: Commit history-preserving change
        T-->>W: Return corrected reading and receipt
    else Target is ambiguous or changed
        K-->>T: Reject proposed change
        T-->>W: Return conflict without overwrite
    end
```

Transcript basis: `T040–T042`, `T050`, `T055–T061`.

## 4. Preserve ambiguity or conflicting evidence

**Input**

- Two credible sources disagree about whether the fourth N5 disk is still an independent migration source or has already joined the pool.

**Steps**

1. The translation layer preserves both submissions and resolves the entities each source appears to describe.
2. It compares source time, scope, directness, and the claims already treated as current.
3. If the evidence cannot settle the question, it represents both interpretations and the conflict between them.
4. It records what observation could resolve the conflict, without assigning that work to itself.
5. A read request receives the conflict and its operational consequence: do not assume the independent copy exists.

**Expected result**

- Useful but unresolved evidence remains available. Neither source is discarded merely because it does not fit a single current story.

**Key failure variant**

- If the translation layer proposes one winner without sufficient evidence, store-side validation or review leaves the conflict unresolved and reports the unsupported conclusion.

```mermaid
sequenceDiagram
    participant W as Work agent
    participant T as Translation layer
    participant K as Knowledge store
    W->>T: Submit evidence that conflicts with current knowledge
    T->>K: Preserve source and inspect competing claims
    K-->>T: Sources, times, scopes, and current interpretation
    alt Evidence resolves the conflict
        T->>K: Propose sourced correction or supersession
        K-->>T: Commit resolved history
        T-->>W: Return resolution and receipt
    else Evidence remains ambiguous
        T->>K: Record competing interpretation and unresolved conflict
        K-->>T: Preserve both without forced winner
        T-->>W: Return uncertainty and needed evidence
    end
```

Transcript basis: `T022–T024`, `T046–T052`, `T055–T061`.

## 5. Retry the same submission safely

**Input**

- A work agent retries the same N5 observation because its first response timed out.
- The evidence and retry identity are unchanged.

**Steps**

1. The translation layer receives the retry as a clean invocation.
2. It asks the knowledge store whether that retry identity and content were already processed.
3. If they match an accepted transaction, it returns the earlier receipt without creating another source, fact, or link.
4. If the first attempt never committed, it evaluates the submission normally.
5. If the retry identity matches but the content differs, it returns a mismatch instead of guessing which request is authoritative.

**Expected result**

- Network retries do not multiply knowledge or change meaning, and the work agent receives a stable outcome.

**Key failure variant**

- Reusing an identity for different evidence produces a visible conflict; neither version silently replaces the other.

```mermaid
sequenceDiagram
    participant W as Work agent
    participant T as Translation layer
    participant K as Knowledge store
    W->>T: Retry submission with the same identity
    T->>K: Check prior processing and content identity
    alt Same submission already committed
        K-->>T: Existing receipt
        T-->>W: Return prior result as a no-op
    else No committed result exists
        T->>K: Validate and apply submission
        K-->>T: New commit receipt
        T-->>W: Return new result
    else Identity matches but content differs
        K-->>T: Identity conflict
        T-->>W: Reject ambiguous retry
    end
```

Transcript basis: `T057–T060`.

## 6. Link and reorganize knowledge across contexts

**Input**

- An existing fact about `tank` is relevant to N5, the storage domain, RAIDZ migration, and inference-resource planning.
- A human or work agent asks to make those relationships discoverable without copying the fact.

**Steps**

1. The translation layer resolves the existing knowledge piece and each requested context.
2. It inspects current relationships and checks whether the request is asserting a relationship or merely suggesting one.
3. It proposes only missing, supported relationships; the underlying content remains one durable piece.
4. The knowledge store validates the endpoints and applies the organizational change.
5. Retrieval through any linked context can now discover the same knowledge and provenance.

**Expected result**

- Reorganization changes how knowledge is found, not how many copies of the statement exist. Agents can approach the same material from host, domain, operation, or planning contexts.

**Key failure variant**

- An uncertain inferred relationship remains visibly provisional or uncommitted; it does not silently become an accepted link.

```mermaid
sequenceDiagram
    participant W as Human or work agent
    participant T as Translation layer
    participant K as Knowledge store
    W->>T: Ask to connect one knowledge piece to several contexts
    T->>K: Resolve piece, contexts, and existing relationships
    K-->>T: Canonical piece and relationship neighborhood
    T->>K: Propose supported missing relationships
    alt Endpoints and meaning validate
        K-->>T: Commit relationship changes
        T-->>W: Return one piece with multiple paths
    else Relationship is uncertain or invalid
        K-->>T: Keep provisional or reject
        T-->>W: Explain unresolved organization
    end
```

Transcript basis: `T043–T048`, `T051–T052`, `T055–T061`.

## 7. Reject or recover from an invalid partial mutation

**Input**

- One submission asks to record an observation, supersede an older statement, and link the result to a migration operation.
- The observation is interpretable, but the proposed operation target cannot be resolved.

**Steps**

1. The translation layer interprets the whole request and inspects every affected item.
2. It prepares a bounded set of related changes rather than applying each semantic step immediately.
3. The knowledge store validates the complete set and detects the invalid target.
4. No partial accepted state remains: either the full interpreted change is rejected or a separately defined source-capture step remains clearly distinct from accepted knowledge.
5. The response identifies the failed part, the unchanged accepted state, and whether the original evidence was retained for another attempt.

**Expected result**

- A failed multi-step interpretation cannot leave a new observation accepted while its correction or required relationship is missing without saying so explicitly.

**Key failure variant**

- A process failure after validation yields a failed or indeterminate receipt that can be inspected and retried; it never reports success without a durable commit result.

```mermaid
sequenceDiagram
    participant W as Work agent
    participant T as Translation layer
    participant K as Knowledge store
    W->>T: Submit one intent requiring several related changes
    T->>K: Inspect all affected knowledge
    K-->>T: Current state and unresolved target
    T->>K: Propose bounded multi-part change
    alt Entire change validates and commits
        K-->>T: Commit receipt
        T-->>W: Return accepted result
    else Any required part is invalid
        K-->>T: Reject or roll back accepted-state changes
        T-->>W: Return failure, unchanged state, and evidence status
    end
```

Transcript basis: `T055–T061`.

## 8. Assemble task-specific context from stored pieces

**Input**

- A work agent asks: “Can the fourth disk now be erased and added to `tank`?”
- It asks for the answer, blockers, and supporting evidence within a bounded context size.

**Steps**

1. The translation layer resolves the disk, pool, migration, verification attempt, and destructive boundary.
2. It retrieves current and superseded observations, relevant safety constraints, the verification result, and the source evidence behind each.
3. It recognizes that a completed read is not equivalent to retained successful verification when output or exit status is missing.
4. It assembles a task-specific narrative: current topology, what is known, what remains unproven, and why erasure is or is not supported.
5. It returns the answer and compact citations without storing the generated narrative as a new canonical document.

**Expected result**

- The work agent receives a coherent operational explanation assembled from reusable knowledge pieces, without raw front matter or an entire repository dump.

**Key failure variant**

- If verification completion is unknown, the answer remains “not established” even when an older plan or partial progress estimate implies an expected finish time has passed.

```mermaid
sequenceDiagram
    participant W as Work agent
    participant T as Translation layer
    participant K as Knowledge store
    W->>T: Ask destructive-boundary question with context budget
    T->>K: Resolve subjects and retrieve task-relevant knowledge
    K-->>T: Topology, verification, constraints, history, and sources
    T->>T: Reconcile status and assemble a bounded explanation
    alt Evidence establishes the preconditions
        T-->>W: Supported answer with evidence and remaining risks
    else A critical precondition is unproven
        T-->>W: Not established; identify blocker and source gap
    end
```

Transcript basis: `T013–T024`, `T043–T052`, `T055–T061`.

## Questions these workflows leave open

- Does raw evidence commit independently when its interpreted mutation fails?
- What distinguishes an accepted relationship from a useful inferred one?
- Which submissions need explicit human acceptance, and which can record direct observations immediately?
- What makes two retries the same: caller identity, supplied identity, evidence content, or some combination?
- How are conflicts declared resolved without losing the competing source history?
- How much provenance belongs in a normal context capsule versus an on-demand audit response?

These are inputs to the simulation harness. They are not decisions hidden inside these examples.
