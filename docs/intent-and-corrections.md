# Intent and Corrections

The user's statements and corrections define the current intent. Assistant proposals below remain examples or hypotheses unless the user explicitly accepted them. ([T048](../source/origin-conversation-verbatim.md#t048---user), [T061](../source/origin-conversation-verbatim.md#t061---user))

## What prompted the work

- N5 storage knowledge did not fit cleanly into a host-specific architecture document. The user expected a general storage context cross-linked to N5 and questioned whether the documentation guide itself had become restrictive. ([T032](../source/origin-conversation-verbatim.md#t032---user), [T038](../source/origin-conversation-verbatim.md#t038---user))
- The underlying wish was for addressable knowledge pieces that could appear in several contexts without being copied. ([T043](../source/origin-conversation-verbatim.md#t043---user))

## Corrections that changed the direction

1. **Documents are not the primary unit.** The assistant first proposed cards and generated Markdown views. The user clarified that automatic linking, controlled mutations, and a managed knowledge backend are the real problem. ([T045](../source/origin-conversation-verbatim.md#t045---assistant), [T046](../source/origin-conversation-verbatim.md#t046---user))
2. **A large universal record is unwanted.** The user rejected a design in which every piece carries irrelevant fields or exposes all metadata to every reader. ([T046](../source/origin-conversation-verbatim.md#t046---user))
3. **Do not entrench an early storage or composition model.** After the assistant proposed minimal objects, facets, authored views, and tool names, the user asked to keep narrowing and warned that the invisible mediation was the difficult part. ([T047](../source/origin-conversation-verbatim.md#t047---assistant), [T048](../source/origin-conversation-verbatim.md#t048---user))
4. **Rendering is not the first product.** The assistant explored stable human-facing documents and two-sided GraphRAG; the user corrected the scope to something used by agents 99% of the time. ([T050](../source/origin-conversation-verbatim.md#t050---assistant), [T051](../source/origin-conversation-verbatim.md#t051---user))
5. **The working agent does not operate the knowledge structure.** The user moved the intelligence into a stateless internal layer that interprets all traffic into and out of the store. ([T055](../source/origin-conversation-verbatim.md#t055---user))
6. **The narrow internal role is deliberate.** It receives clean context and only knowledge-related tools, can use a fast model, reduces risk, and leaves the outside agent free to do its broader work. ([T057](../source/origin-conversation-verbatim.md#t057---user))
7. **“Translation layer” is closer than “agent.”** It may reason and make several tool calls, but it is bounded to translating and carrying out a knowledge interaction rather than running a long workflow. ([T059](../source/origin-conversation-verbatim.md#t059---user))
8. **“Knowledge agent” is misleading.** The role includes encoding, storing, organizing, reconciling, and retrieving knowledge; retrieval alone understates the uncertain half of the problem. ([T061](../source/origin-conversation-verbatim.md#t061---user))
9. **Behavior comes before design.** The user asked for an overview, distilled goals, fictional workflows, diagrams, mini simulations, candidate states, and a harness before architecture or code. ([T061](../source/origin-conversation-verbatim.md#t061---user))
10. **The actual transcript is the evidence.** A compacted summary is not an acceptable substitute for the complete conversation when deriving intent. ([T069](../source/origin-conversation-verbatim.md#t069---user))
11. **A workflow story is not yet a simulation.** Every intermediate step must expose the information supplied to the layer, what the layer can reason from it, what organized knowledge must be retrievable, and what information moves left and right. ([T096](../source/origin-conversation-verbatim.md#t096---user))
12. **The N5 examples serve the knowledge structure.** Operational recap or mock-test language must not displace the central work: discovering the reusable knowledge model and its bidirectional translation boundary. ([T098](../source/origin-conversation-verbatim.md#t098---user))

## Accepted direction

- Preserve the full conversation and keep every derived claim traceable to it. ([T061](../source/origin-conversation-verbatim.md#t061---user), [T069](../source/origin-conversation-verbatim.md#t069---user))
- Describe the desired interactions in plain steps before naming components or selecting technology. ([T061](../source/origin-conversation-verbatim.md#t061---user), [T063](../source/origin-conversation-verbatim.md#t063---user))
- Treat the internal translation layer and external work agent as different roles with different contexts and tools. ([T055](../source/origin-conversation-verbatim.md#t055---user), [T057](../source/origin-conversation-verbatim.md#t057---user), [T059](../source/origin-conversation-verbatim.md#t059---user))
- Test whether every intermediate action is possible with the exact information available, including what retrieval must return and what crosses each boundary. ([T096](../source/origin-conversation-verbatim.md#t096---user), [T098](../source/origin-conversation-verbatim.md#t098---user))
- Keep the documents concise, direct, and free of invented policy language. ([T063](../source/origin-conversation-verbatim.md#t063---user))

## Still hypotheses

- A graph database, GraphRAG, a Palantir-like ontology, or any specific storage engine may inform later work, but none is selected. ([T048](../source/origin-conversation-verbatim.md#t048---user), [T053](../source/origin-conversation-verbatim.md#t053---user), [T061](../source/origin-conversation-verbatim.md#t061---user))
- Cards, facets, truth lanes, authored views, deterministic rendering, and the assistant's proposed tool names are unaccepted examples. ([T045](../source/origin-conversation-verbatim.md#t045---assistant), [T047](../source/origin-conversation-verbatim.md#t047---assistant), [T052](../source/origin-conversation-verbatim.md#t052---assistant))
- The exact validation rules, states, transaction shape, and enforcement mechanisms will come from workflow simulations rather than the assistant's earlier lists. ([T059](../source/origin-conversation-verbatim.md#t059---user), [T060](../source/origin-conversation-verbatim.md#t060---assistant), [T061](../source/origin-conversation-verbatim.md#t061---user))
