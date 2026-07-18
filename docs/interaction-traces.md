# Candidate interaction traces

These traces replace the hidden verbs in the original [workflow stories](workflows.md) with explicit information movement. They directly test the user's questions about intermediate feasibility, organization, retrieval, and left/right payloads. ([T096](../source/origin-conversation-verbatim.md#t096---user), [T098](../source/origin-conversation-verbatim.md#t098---user)) They are candidate golden traces, not accepted product behavior. Review can correct them before they guide architecture.

Direction labels come from the [information-flow model](information-flow.md):

- **L→T:** outside human or work agent to the translation layer.
- **T→R:** translation layer to the durable knowledge side.
- **R→T:** durable knowledge side to the translation layer.
- **T→L:** translation layer back outside.
- **T:** reasoning inside one short-lived invocation.

Every trace states what is already durable, what is absent, what crosses each boundary, what changes, and whether the model can perform the step with the information supplied.

## Trace 1: record an observed ARC setting without turning it into policy

**Question under test:** Can a structure-blind work agent submit evidence while the internal layer preserves the difference between observed configuration and accepted requirement?

**Starting durable state**

- N5 and ZFS ARC can be found from the names `N5` and `zfs_arc_max`.
- Earlier material says that ARC is configured at 2 GiB; one interpretation incorrectly presents that as the right inference-memory boundary.
- The new command output and its qualification are absent.

**Left input**

```text
Intent: record an observation
Target hints: N5, zfs_arc_max
Evidence: authenticated command output reports 2147483648
Source: command/session locator and observation time
Qualification: this is live configuration, not an accepted permanent sizing decision
```

| # | Direction | Information and reasoning | Durable effect |
| --- | --- | --- | --- |
| 1 | L→T | Send the exact evidence, source, time, target hints, intent, and qualification. No store IDs or record shape are supplied. | None |
| 2 | T | Parse `2147483648` as 2 GiB. Separate raw evidence, observed value, and non-policy qualification. | None |
| 3 | T→R | Ask for candidates matching N5 and `zfs_arc_max`; include only the submitted hints and source scope. | None |
| 4 | R→T | Return candidate references, aliases, distinguishing context, match basis, and whether either result is ambiguous or truncated. | None |
| 5 | T | Select only uniquely supported targets. Otherwise prepare a clarification and stop before proposing an operational claim. | None |
| 6 | T→R | For resolved targets, request current and historical configuration observations, sizing decisions, qualifications, conflicts, sources, and query limits. | None |
| 7 | R→T | Return the bounded related material, including the earlier mistaken reading and whether the result set is complete for the requested scope. | None |
| 8 | T | Compare the submission with existing material. Decide whether it is new, repeated, changed, or conflicting. Do not infer a sizing decision. | None |
| 9 | T→R | Propose separate effects: retain the submitted source; record the 2 GiB observation; preserve the explicit non-policy qualification; qualify a specific older reading only if the target and caller standing support it; create no sizing decision. | None until evaluated |
| 10 | R→T | Return accepted, rejected, unchanged, or indeterminate status for each proposed effect, plus resulting references and validation reasons. | Only the effects explicitly reported as accepted |
| 11 | T→L | Report the observed value and source, the standing of the qualification, whether an older reading changed, and that no permanent sizing decision was created. | None |

**Expected ending state**

- The source remains traceable.
- One live configuration observation is associated with the resolved N5/ARC subject.
- The qualification remains distinguishable from a sizing decision.
- Only an unambiguous, supported older reading is qualified.
- No `2 GiB is required` decision is created.

**Feasibility ledger**

- A small model can parse the value, distinguish observation from policy, compare bounded candidates, and draft the proposed effects.
- Tools must supply identity candidates, related history, source standing, query limits, and per-effect persistence outcomes.
- Neither side can infer that the output truly came from N5 if the evidence is not bound to the host and time.

**Pressure variation:** If the source or N5 identity is insufficient, no current observation is accepted. The response states whether the raw submission was retained and what evidence would resolve the ambiguity. Whether unusable source material is retained is still an open behavior question.

**Candidate states exposed:** received → identity resolved or clarification needed → related state loaded → effects proposed → applied, partial, rejected, or indeterminate → returned.

## Trace 2: retrieve bounded context for an N5 investigation

**Question under test:** Can the layer return enough current, safety-relevant context without dumping the store or silently omitting a critical constraint?

**Starting durable state**

- N5, its pools, disks, and known operations are linked through some retrievable paths.
- Current and historical observations coexist.
- At least one unfinished operation and one storage safety constraint are present.

**Left input**

```text
Task: diagnose current N5 disk activity
Wanted: topology, active safety constraints, unfinished operations, and source pointers
Scope: N5 storage
As of: supplied request time
Limit: bounded context budget
```

| # | Direction | Information and reasoning | Durable effect |
| --- | --- | --- | --- |
| 1 | L→T | Send the task, wanted categories, N5 scope, as-of time, and response limit. | None |
| 2 | T | Decompose the request into identity, topology, activity, safety, operation, time, and source questions. | None |
| 3 | T→R | Resolve N5 and request current material for each named category, plus conflicting and superseded material that changes the reading. | None |
| 4 | R→T | Return candidate identity, bounded pieces, relation paths, standing, time, sources, and coverage for each requested category. Mark missing, truncated, unsearched, or inaccessible categories separately. | None |
| 5 | T | Select material that answers the task. Keep operational identifiers, active constraints, unresolved conflicts, and material freshness; omit unrelated metadata. | None |
| 6 | T→R | Drill into any source or relationship needed to distinguish current activity from an old plan or completed operation. | None |
| 7 | R→T | Return the requested source-level detail and the limits of that drill-down. | None |
| 8 | T | Assemble a capsule whose claims are supported by returned material. State any coverage or freshness gap instead of filling it. | None |
| 9 | T→L | Return the bounded context, source pointers, uncertainty, and any category that could not be covered within the request. | None |

**Expected ending state:** No durable knowledge changes. The returned capsule is task context, not automatically a new canonical piece.

**Feasibility ledger**

- A model can interpret the task, rank bounded candidates, and write the capsule.
- Retrieval must support identity, relation, time, history, conflict, source, and task paths. It must report coverage limits.
- The model cannot prove that no safety constraint exists merely because none appeared in a result page.

**Pressure variation:** If current topology conflicts or the context budget cannot include required safety material, the result says the task is not fully covered and identifies the omitted or conflicting category.

**Candidate states exposed:** received → scope decomposed → material retrieved → coverage sufficient or incomplete → context returned.

## Trace 3: correct an earlier interpretation without erasing its history

**Question under test:** Can a correction change the current reading while preserving the source and reason for the earlier one?

**Starting durable state**

- The live 2 GiB setting and the assistant's earlier `already protects inference memory` interpretation are individually retrievable.
- Their sources and current standing are available.

**Left input**

```text
Intent: correct an earlier interpretation
Statement: the 2 GiB ARC cap is live configuration, not an accepted hardware requirement
Target hint: the earlier claim that the cap already protects inference memory
Supporting context: the live measurement and the human correction
```

| # | Direction | Information and reasoning | Durable effect |
| --- | --- | --- | --- |
| 1 | L→T | Send the correction, target hint, supporting material, and whether this is an explicit human decision or a work-agent interpretation. | None |
| 2 | T→R | Resolve the target claim and return candidate texts, sources, current standing, relationships, and version or change status. | None |
| 3 | R→T | Return one or more candidate targets and enough context to distinguish them; report ambiguity. | None |
| 4 | T | If one target is established, classify the new meaning as qualification, correction, coexistence, or a new observation. If not, stop for clarification. | None |
| 5 | T→R | Propose the new interpretation and its relationship to the exact earlier target; preserve both source histories. Include the target state used to form the proposal. | None until evaluated |
| 6 | R→T | Report whether the target still matches, whether the relationship is accepted, and the resulting current reading. | Accepted effect only |
| 7 | T→L | Return the new current reading, what changed, what remained historical, and any rejected or ambiguous part. | None |

**Expected ending state**

- Retrieval no longer uses the live value as proof of an accepted requirement.
- The earlier source and mistaken interpretation remain auditable.
- The observed value remains current until later evidence changes it.

**Feasibility ledger**

- A model can compare the two meanings and propose a qualification when one target is clearly supplied.
- The durable side must provide stable targets, history, source standing, current change state, and the observable outcome.
- Concurrency and history preservation are not model judgments.

**Pressure variation:** If two earlier statements could be the target, no target is changed. The response returns the candidates and asks for the missing distinction.

**Candidate states exposed:** received → target unique or ambiguous → relation proposed → accepted, rejected, or changed underneath → returned.

## Trace 4: retain conflicting evidence without inventing a winner

**Question under test:** Can useful contradictory material remain retrievable while the layer avoids converting source comparison into unsupported truth?

**Starting durable state**

- One sourced statement says the fourth disk is still the independent migration source.
- A stored safety rule says destructive reuse requires the source role and verification preconditions to be established.
- No later source has resolved the disk role.

**Left input**

```text
Intent: record new evidence
Claimed meaning: the fourth disk has already joined tank
Evidence: exact source, time, scope, and raw content
Target hints: N5, tank, fourth migration disk
```

| # | Direction | Information and reasoning | Durable effect |
| --- | --- | --- | --- |
| 1 | L→T | Send the new source and claimed meaning without asking the outside agent to encode a conflict record. | None |
| 2 | T→R | Resolve the disk, pool, and migration context; request the current role, competing claims, their sources/times, and the applicable safety condition. | None |
| 3 | R→T | Return bounded identity candidates, competing material, source descriptors, current standing, safety condition, and coverage limits. | None |
| 4 | T | Compare scope, time, directness, and identity. Apply no unstated source-precedence rule. Determine only whether the new material clearly resolves, clearly repeats, or remains in conflict. | None |
| 5 | T→R | If unresolved, propose retaining the new source, its interpretation, and an explicit conflict with the existing interpretation. Propose a resolution question as a question, not as knowledge. | None until evaluated |
| 6 | R→T | Report each retained effect, current conflict standing, and any effect rejected for identity or provenance reasons. | Accepted effects only |
| 7 | T→L | Return the conflict, why no winner was selected, the stored safety consequence if one exists, and the observation needed to resolve it. | None |

**Expected ending state:** Both sources and interpretations remain available; their disagreement is discoverable; no unsupported winner is current; a proposed follow-up remains distinguishable from an observation.

**Feasibility ledger**

- A model can compare bounded sources and explain why they do or do not settle the same claim.
- Identity, source details, conflict representation, stored safety policy, and durable effects must come from tools.
- The model cannot invent source authority or decide that one source wins without an applicable rule or decisive evidence.

**Pressure variation:** A later authenticated topology observation may resolve the conflict only if its identity, scope, time, and standing actually cover the disputed disk role. `Later` alone is not sufficient.

**Candidate states exposed:** source received → identities resolved → repeated, resolving, or conflicting → effects applied or rejected → uncertainty returned.

## Trace 5: retry after the first response was lost

**Question under test:** Can the system avoid duplicating a prior effect when a stateless invocation does not know whether the first call completed?

**Starting durable state**

- A prior request identity and its exact durable outcome are available for the normal case.
- The new invocation has no conversational memory of it.

**Left input**

```text
Intent: repeat the earlier submission
Request identity: same caller-supplied operation identity
Content: same evidence and qualification
Reason: first response timed out
```

| # | Direction | Information and reasoning | Durable effect |
| --- | --- | --- | --- |
| 1 | L→T | Send the prior request identity, repeated content, and retry intent. | None |
| 2 | T→R | Ask for the durable outcome bound to that request identity and whether the submitted content matches it. | None |
| 3 | R→T | Return prior effect, response data, and exact-match, mismatch, absent, or indeterminate status. | None |
| 4 | T | If prior success and content match are established, do not propose another mutation. Semantic similarity alone is not enough. | None |
| 5 | T→L | Return the prior outcome and say that no new effect was created. | None |

**Expected ending state:** The store is unchanged; the outside caller receives the established earlier result.

**Feasibility ledger**

- The model can explain and route the returned status.
- Request identity, exact content binding, outcome durability, and any atomic relationship between effect and receipt are protocol behavior.
- A stateless model cannot reliably infer retries from similar prose.

**Pressure variation:** If no request identity exists or the prior outcome is indeterminate, the layer returns `indeterminate` or requests reconciliation. It does not blindly replay. This is a candidate safety behavior, not yet an accepted protocol.

**Candidate states exposed:** retry received → prior outcome established, absent, mismatched, or indeterminate → prior result returned, new proposal allowed, or reconciliation required.

## Trace 6: make one piece discoverable from several contexts

**Question under test:** Can organization change without copying the knowledge content or forcing the outside agent to author graph structure?

**Starting durable state**

- One existing piece describes `tank` storage geometry and has source material.
- N5, storage, RAIDZ migration, and inference-resource planning are discoverable contexts.
- Some requested relationships may already exist.

**Left input**

```text
Intent: make the existing tank fact discoverable from four named contexts
Knowledge hint: quoted content or ordinary-language description
Contexts: N5, storage, RAIDZ migration, inference-resource planning
Standing: explicit human organization request
```

| # | Direction | Information and reasoning | Durable effect |
| --- | --- | --- | --- |
| 1 | L→T | Send the content hint, context names, and whether the relationships are asserted or merely suggested. No relation syntax is supplied. | None |
| 2 | T→R | Resolve the existing piece and each context; retrieve current relationships, source, and any context-specific qualification. | None |
| 3 | R→T | Return candidate endpoints, match basis, existing paths, and ambiguity for each requested context. | None |
| 4 | T | Confirm that the same meaning can be reused. If a context changes its time, scope, or qualification, do not pretend one piece is identical there. | None |
| 5 | T→R | Propose only supported missing relationships, each referencing the resolved piece and context. | None until evaluated |
| 6 | R→T | Return per-relationship accepted, unchanged, provisional, rejected, or indeterminate outcomes. | Accepted relationships only |
| 7 | T→L | Return one content reference, every confirmed discovery path, and each unresolved context. | None |

**Expected ending state:** The content remains one durable piece; only organization changes; retrieval through each accepted context reaches the same source and content.

**Feasibility ledger**

- A model can compare bounded endpoint candidates and detect obvious scope or qualification differences.
- Tools must provide stable endpoints, existing organization, relation standing, and observable outcomes.
- Automatic linking quality is not proven by one successful trace.

**Pressure variation:** If one context is ambiguous, that relationship is not silently accepted. Whether unambiguous relationships in the same request may still apply remains a partial-effect question for Trace 7.

**Candidate states exposed:** request received → endpoints resolved or ambiguous → reuse valid or split needed → relationships proposed → per-effect outcomes returned.

## Trace 7: expose an invalid target before or during a multi-effect change

**Question under test:** What must be observable when one semantic intent implies several effects and one target is invalid?

**Starting durable state**

- N5, ARC, the earlier interpretation, and the submitted evidence can be resolved.
- The named migration operation cannot be resolved.
- The store's all-or-nothing, partial-effect, and source-retention behavior has not been selected.

**Left input**

```text
Intent: record an ARC observation, qualify the old reading, and connect it to a named migration operation
Evidence and targets: sufficient except for the migration operation
```

| # | Direction | Information and reasoning | Durable effect |
| --- | --- | --- | --- |
| 1 | L→T | Send the combined intent, evidence, and target hints. | None |
| 2 | T→R | Resolve every affected target and request the current state needed for all proposed effects. | None |
| 3 | R→T | Return resolved observation/correction targets and an explicit unresolved-operation result. | None |
| 4 | T | Describe the complete intended effect set and mark the link effect as impossible with current information. | None |
| 5 | T→R | Request evaluation of the whole effect set before claiming any change. Ask for per-effect outcomes and whether evaluation itself can change durable state. | None unless the right side reports otherwise |
| 6 | R→T | Return the actual contract and outcome: no effects, explicit partial effects, or indeterminate effects. Identify source retention separately from accepted interpretation. | Only effects explicitly reported |
| 7 | T→R | If the outcome is partial or unknown, inspect the affected references or operation journal needed to establish current state. | None |
| 8 | R→T | Return observed effects and anything still indeterminate. | None |
| 9 | T→L | Report every applied, rejected, unchanged, and unknown effect. Do not collapse them into one success flag. | None |

**Candidate oracle for the first simulation:** A validate-all-before-apply right side rejects the semantic mutation because the operation target is unresolved; no interpreted claim or link changes. Whether the raw source is retained is reported separately. This oracle is a hypothesis to compare, not an architecture decision.

**Feasibility ledger**

- A model can identify that the combined intent has several effects and explain returned outcomes.
- Preview, journaling, atomicity, failure injection, source-retention behavior, and reconciliation are store/protocol capabilities.
- This workflow is not executable against a right side that exposes only a generic `write succeeded/failed` response.

**Pressure variation:** If the process stops after an effect may have occurred, the result remains indeterminate until an inspection mechanism establishes each effect.

**Candidate states exposed:** intent received → effect set formed → validation rejected, applied, partial, or interrupted → inspection if needed → exact outcome returned.

## Trace 8: decide whether the fourth disk may be erased

**Question under test:** Can the layer assemble a safety-relevant answer from reusable pieces without treating missing verification evidence as success?

**Starting durable state**

- N5, `tank`, disk identities, current and historical topology, migration/copy facts, and a destructive-boundary constraint are retrievable.
- A checksum verification attempt is known to have read data.
- Retained successful output and exit status or equivalent success evidence are absent or not yet established.
- No erase or pool-add action is requested in this trace.

**Left input**

```text
Question: Can the fourth disk now be erased and added to tank?
Wanted: answer, blockers, and supporting evidence
Scope: N5 migration
As of: request time
Limit: bounded context budget
```

| # | Direction | Information and reasoning | Durable effect |
| --- | --- | --- | --- |
| 1 | L→T | Send the destructive-boundary question, N5 migration scope, as-of time, wanted response, and budget. | None |
| 2 | T | Decompose `fourth disk` and `now` into identity, current-state, intended-action, precondition, and evidence questions. | None |
| 3 | T→R | Resolve `tank` and the relative disk phrase within N5/migration context; request candidates, match basis, current role hints, and ambiguity. | None |
| 4 | R→T | Return candidate disk/pool references and whether one pair is uniquely established. | None |
| 5 | T | Select only a unique pair. Otherwise return an identity clarification without a safety conclusion. | None |
| 6 | T→R | Retrieve current topology, disk role, copy/migration state, destructive preconditions, verification attempts/results, history/conflicts, sources, currentness, and coverage limits. | None |
| 7 | R→T | Return bounded task material and state which categories were searched, truncated, inaccessible, absent, or not searched. | None |
| 8 | T | Form the evidence chain actually required by the stored precondition: correct disk/source, correct target/scope, completed copy state, applicable erase rule, qualifying verification method, and retained successful result. | None |
| 9 | T→R | Drill into the exact verification attempt and rule: command or method, source/target/scope, start/end, retained output/result, exit state or equivalent success proof, and source for each. | None |
| 10 | R→T | Return source-level evidence and distinguish `no retained result` from `not indexed`, `not searched`, `inaccessible`, or `truncated`. | None |
| 11 | T | Compare only explicit evidence with the explicit precondition. Process absence, elapsed time, bytes read, or a completed read do not establish retained verification success. | None |
| 12 | T→L | Return `supported`, `not established`, or `identity ambiguous`; list every prerequisite as supported, unsupported, or unknown; cite the blocking source gap and next evidence. | None |

**Expected ending state:** No knowledge mutation and no world action. The generated answer is not automatically stored as canonical knowledge.

**Expected left response for the current scenario**

```text
Not established. The stored material shows that a verification read ran, but it does not retain a successful result and exit status or equivalent proof covering the identified source and target. That missing success evidence blocks the precondition for erasing the independent source. No erase or pool-add action was performed.
```

**Feasibility ledger**

- A model can parse the question, choose among bounded candidates, follow an explicit prerequisite chain, and compare source evidence with an explicit verification criterion.
- Tools must supply identity, current topology, preconditions, operation identity and scope, source-level results, and retrieval coverage.
- The model cannot infer success from elapsed time, process absence, or bytes read. It cannot infer global absence from an unqualified empty result.

**Pressure variation:** If retained evidence later establishes the exact verification method, scope, completion, and successful outcome, the answer may become `supported` with citations and remaining risks. The layer still does not erase the disk; that is outside its capabilities.

**Candidate states exposed:** received → identity unique or ambiguous → task state loaded → evidence chain complete, conflicted, or gapped → supported or not established → returned.

## Cross-trace findings

- The model is useful for semantic decomposition, bounded comparison, candidate selection, and explanation.
- Identity, source binding, currentness, retrieval coverage, authority, persistence, retries, and failure recovery cannot be supplied by semantic confidence.
- Reads and writes use the same translation boundary, but their proof obligations differ.
- The write side is the less established part: it must preserve source, interpretation, organization, history, and exact effects without asking the outside agent to shape records.
- Retrieval is easy only when the durable side supports several paths and reports the limits of every result.
- The traces expose several candidate lifecycles; they do not yet prove one universal state machine.

The machine-readable fixtures replay these information dependencies without selecting a production schema. A later real translation-layer candidate can be judged against the same externally visible traces.
