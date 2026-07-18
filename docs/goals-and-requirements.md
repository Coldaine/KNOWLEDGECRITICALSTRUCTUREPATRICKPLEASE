# Goals and Working Requirements

## Goals

- **Make the intent durable.** Preserve the complete conversation and convert it into concise Markdown that can be reviewed after the original context is gone. ([T061](../source/origin-conversation-verbatim.md#t061---user), [T063](../source/origin-conversation-verbatim.md#t063---user), [T069](../source/origin-conversation-verbatim.md#t069---user))
- **Replace document-owned knowledge with reusable knowledge.** A fact or idea can support several contexts without being copied and maintained independently in each one. ([T043](../source/origin-conversation-verbatim.md#t043---user), [T046](../source/origin-conversation-verbatim.md#t046---user))
- **Make knowledge interaction agent-first.** Most consumers are agents; human rendering can wait until a workflow demonstrates that it matters. ([T051](../source/origin-conversation-verbatim.md#t051---user))
- **Separate task work from knowledge mediation.** External agents investigate and act; the internal layer interprets requests and handles knowledge interactions. ([T055](../source/origin-conversation-verbatim.md#t055---user), [T057](../source/origin-conversation-verbatim.md#t057---user))
- **Cover the entire knowledge lifecycle.** The internal role includes encoding, organizing, storing, correcting, and retrieving—not only search. ([T061](../source/origin-conversation-verbatim.md#t061---user))
- **Discover the behavior before designing the software.** Scenarios and simulations establish what the system needs to do before components, states, or code are committed. ([T061](../source/origin-conversation-verbatim.md#t061---user), [T063](../source/origin-conversation-verbatim.md#t063---user))

## Requirements for the design spike

- **Source:** Keep the verbatim conversation as the primary evidence; cite its `T###` anchors from every derived document. ([T061](../source/origin-conversation-verbatim.md#t061---user), [T069](../source/origin-conversation-verbatim.md#t069---user))
- **Derivation:** Separate user intent and corrections from assistant suggestions so an example does not silently become a decision. ([T048](../source/origin-conversation-verbatim.md#t048---user), [T061](../source/origin-conversation-verbatim.md#t061---user))
- **Expression:** Use short, clear bullets that explain what is wanted and why; avoid invented guardrails and inflated policy language. ([T063](../source/origin-conversation-verbatim.md#t063---user))
- **Workflow coverage:** Write fictional, primitive flows for information arriving, being interpreted, transformed, stored, linked, retrieved, corrected, conflicted, duplicated, or rejected. ([T061](../source/origin-conversation-verbatim.md#t061---user))
- **Workflow detail:** Record each interaction step by step, then diagram the same flow and identify what each participating part did. ([T061](../source/origin-conversation-verbatim.md#t061---user))
- **Progressive preservation:** Keep the source, distilled goals, workflow versions, diagrams, and simulation results as the spike develops. ([T061](../source/origin-conversation-verbatim.md#t061---user))
- **Simulation:** Exercise normal, ambiguous, conflicting, and failed interactions as mini simulations before accepting a design. ([T061](../source/origin-conversation-verbatim.md#t061---user))
- **State discovery:** Use observed workflow transitions to decide whether explicit states or one or more state machines are useful. Do not assume them in advance. ([T061](../source/origin-conversation-verbatim.md#t061---user))
- **Harness:** After the written simulations stabilize, define a harness that can drive the interactions and check their expected resulting states. ([T061](../source/origin-conversation-verbatim.md#t061---user))
- **Decision point:** Select architecture and begin implementation only after the expected interactions are concrete and reviewed. ([T061](../source/origin-conversation-verbatim.md#t061---user))

## Behavioral constraints to test

- An external agent can ask for relevant knowledge or submit new evidence without understanding the store's internal organization. ([T055](../source/origin-conversation-verbatim.md#t055---user), [T057](../source/origin-conversation-verbatim.md#t057---user))
- The internal layer can interpret the request, perform the needed sequence of knowledge operations, and return a useful result while remaining stateless between interactions. ([T055](../source/origin-conversation-verbatim.md#t055---user), [T059](../source/origin-conversation-verbatim.md#t059---user))
- The internal layer's tools are limited to moving, organizing, reading, and changing knowledge; the external agent keeps its broad task tools and context. ([T057](../source/origin-conversation-verbatim.md#t057---user))
- The narrow interaction supports stronger validation and enforcement without imposing that machinery on the external agent. The simulations will determine what enforcement is actually needed. ([T059](../source/origin-conversation-verbatim.md#t059---user), [T061](../source/origin-conversation-verbatim.md#t061---user))
- A knowledge piece can be reused and linked across relevant contexts without forcing every piece into the same set of fields. ([T043](../source/origin-conversation-verbatim.md#t043---user), [T046](../source/origin-conversation-verbatim.md#t046---user))
- Default results stay useful and concise rather than exposing every piece of metadata. ([T046](../source/origin-conversation-verbatim.md#t046---user))

## Deferred choices

- Database, graph technology, storage format, ontology, object classes, relation types, API, rendering system, and permanent component names remain open. ([T048](../source/origin-conversation-verbatim.md#t048---user), [T051](../source/origin-conversation-verbatim.md#t051---user), [T061](../source/origin-conversation-verbatim.md#t061---user))
- Exact states, validation rules, mutation rules, and enforcement behavior remain open until the workflows expose them. ([T059](../source/origin-conversation-verbatim.md#t059---user), [T061](../source/origin-conversation-verbatim.md#t061---user))
- Human-readable document assembly remains secondary unless later scenarios show a concrete need. ([T051](../source/origin-conversation-verbatim.md#t051---user))
