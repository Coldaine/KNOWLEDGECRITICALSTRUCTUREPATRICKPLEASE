# What we are building and why

## The thing to build

Build an agent-native personal-scale knowledge-and-decision service.

Broad work agents interact with it in ordinary task language. One narrow LLM-mediated semantic translation layer, conceptually inside the knowledge-service boundary, is their normal knowledge interface. It handles both directions: interpreting, encoding, organizing, and storing incoming knowledge; retrieving and assembling useful context on the way out. ([T055](../source/origin-conversation-verbatim.md#t055---user), [T057](../source/origin-conversation-verbatim.md#t057---user), [T059](../source/origin-conversation-verbatim.md#t059---user), [T061](../source/origin-conversation-verbatim.md#t061---user))

```text
Human or outside work agent
  broad tools, long and messy task context
                ⇅ ordinary request, evidence, or bounded result
Internal agentic semantic translation layer
  clean bounded context, knowledge-only tools, bounded multi-step reasoning
                ⇅ controlled knowledge operations and stored context
Durable linked knowledge backend
  reusable meaning, sources, relationships, organization, and history
```

The closest analogy is a personal-scale semantic operational layer like the useful center of Palantir's Ontology: raw evidence and systems below it, agent reasoning and decisions above it. That analogy explains the purpose; it does not select Palantir, an ontology, or a graph database. ([T053](../source/origin-conversation-verbatim.md#t053---user), [T054](../source/origin-conversation-verbatim.md#t054---assistant))

## Why this exists

- **Documents make the wrong thing authoritative.** One storage fact can matter to N5, the storage domain, a migration, performance work, and a later decision. Moving it between Markdown files only changes which other views become incomplete or duplicated. ([T032](../source/origin-conversation-verbatim.md#t032---user), [T043](../source/origin-conversation-verbatim.md#t043---user))
- **Text alone does not preserve meaning.** `N5 has a 2 GiB ARC cap` can be an observation without being a requirement, accepted decision, or diagnosis. Likewise, a running copy is not a completed or independently verified copy. The system must not launder evidence into a stronger claim. ([T013](../source/origin-conversation-verbatim.md#t013---user), [T017](../source/origin-conversation-verbatim.md#t017---assistant), [T040](../source/origin-conversation-verbatim.md#t040---user), [T042](../source/origin-conversation-verbatim.md#t042---assistant))
- **Every outside agent should not become a graph client.** Requiring each work agent to understand storage shape, entity resolution, links, mutation rules, and history duplicates difficult instructions and produces inconsistent interpretations. ([T055](../source/origin-conversation-verbatim.md#t055---user))
- **One universal record becomes metadata sludge.** Different knowledge needs different shape. Metadata can remain available without every read carrying every field or front-matter block. ([T046](../source/origin-conversation-verbatim.md#t046---user))
- **Retrieval is only half the problem.** The harder and less-established work is decoding evidence, encoding meaning, organizing and linking it, handling corrections or conflicts, and making controlled writes. Calling this a retrieval-oriented “knowledge agent” hides the central problem. ([T061](../source/origin-conversation-verbatim.md#t061---user))

## Why the intelligence belongs inside the knowledge boundary

- Outside agents share one consistent interpreter instead of carrying separate graph-management instructions.
- Its context is clean: one request, relevant stored material, and the knowledge rules—not the outside agent's long task history.
- Its tools are narrow: move, inspect, organize, and change knowledge; outside-world action remains with the work agent.
- Durable state belongs to the backend, so the translation layer can end after each request.
- That narrow scope can support a small, fast model and stronger enforcement around knowledge changes.
- The outside agent remains broadly capable and free to investigate, code, browse, operate, and change direction. ([T055](../source/origin-conversation-verbatim.md#t055---user), [T057](../source/origin-conversation-verbatim.md#t057---user), [T059](../source/origin-conversation-verbatim.md#t059---user))

“Translation layer” describes the product role. It is agentic only because one bounded translation may require entity resolution, retrieval, interpretation, organization, and several tool calls. It does not receive an open-ended mission. ([T059](../source/origin-conversation-verbatim.md#t059---user))

## Ingress capabilities to prove

The accepted boundary implies the following semantic work. The exact sequence, tool calls, and write protocol remain open:

1. The outside agent submits ordinary evidence, a decision, a correction, an organizational intent, or another knowledge-bearing result from its work.
2. The internal layer finds the existing knowledge needed to understand that submission.
3. It resolves references and distinguishes source material from its interpreted meaning.
4. It determines how the meaning relates to existing knowledge, including several relevant contexts, corrections, conflicts, or uncertainty.
5. It uses controlled knowledge-side tools for the bounded interaction and observes what the durable side reports.
6. It returns what was recorded, organized, rejected, left ambiguous, or still needs evidence.

The caller does not manufacture nodes, fields, links, or mutation syntax. Automatic candidate discovery and organization are responsibilities of the knowledge service, not hidden work pushed onto every caller. ([T046](../source/origin-conversation-verbatim.md#t046---user), [T055](../source/origin-conversation-verbatim.md#t055---user), [T057](../source/origin-conversation-verbatim.md#t057---user))

## Egress capabilities to prove

The read side has the same status: the responsibility is clear, while the exact retrieval and assembly mechanics remain open.

1. The outside agent describes its actual task and asks for what matters.
2. The internal layer interprets the task rather than requiring a graph query.
3. It retrieves relevant pieces, relationships, sources, history, corrections, conflicts, and currentness from the durable side.
4. It selects a bounded result that preserves important uncertainty and safety context.
5. It returns readable task context, with identifiers, provenance, or deeper metadata available when useful.

The normal result is not graph rows, a universal object, or a dump of front matter. Most consumers are agents; a human document renderer or CMS is secondary. ([T046](../source/origin-conversation-verbatim.md#t046---user), [T048](../source/origin-conversation-verbatim.md#t048---user), [T051](../source/origin-conversation-verbatim.md#t051---user))

## Product behaviors inferred from the motivating failures

These are grounded design needs and examples to test, not a selected record taxonomy:

- One underlying piece can be discovered from several relevant contexts without several maintained copies.
- Pieces can have different shapes rather than one compulsory set of fields.
- Original source remains distinguishable from later interpretation.
- Semantically different claims remain distinguishable when a task depends on the difference—for example an observation versus a decision, requirement, or diagnosis.
- Organization and relationships can evolve without rewriting the underlying content.
- Metadata and provenance are available on demand without dominating ordinary context.
- Controlled interactions provide a place for validation and stronger enforcement, while the exact mechanics remain open.

The exact piece granularity, representation, relation vocabulary, database, model, tools, and enforcement rules have not been selected.

## What is not the product

- A graph database, GraphRAG pipeline, ontology, card format, or YAML schema.
- A document renderer, generated Markdown system, CMS, or reorganization of the current docs tree.
- A retrieval-only memory or “knowledge agent.”
- N5, ARC, backups, or storage management; those exposed the need and provide pressure cases.
- This transcript repository, the workflow diagrams, the state vocabulary, or the replay harness.

Those may become implementation choices, source material, examples, or design tools. None defines the thing being built.

## Why workflows and simulations exist

The workflows are design probes for this semantic boundary—not the product and not mock tests of a settled architecture. They ask:

- What ordinary information enters from the outside?
- What existing knowledge must the internal layer retrieve?
- Is that material organized well enough for identity resolution, interpretation, linking, correction, and contextual retrieval?
- What can a bounded model actually infer, and what must tools or stored rules supply?
- What becomes durable and discoverable afterward?
- What useful result crosses back to the outside agent?

The answers should expose the capabilities and possible states worth designing. Only then should the project choose architecture and build the service. ([T061](../source/origin-conversation-verbatim.md#t061---user), [T096](../source/origin-conversation-verbatim.md#t096---user), [T098](../source/origin-conversation-verbatim.md#t098---user))

## Current truth

- The transcript contains the user-stated direction, confirmed topology, and corrections that produced the current synthesis.
- The current workflows and fixtures are candidate probes written by the assistant; they are not user-accepted product behavior.
- The replay harness checks declared information flow. It does not prove that a model can perform the central semantic work or that retrieval and automatic organization are solved.
- No runtime knowledge backend or internal translation service exists yet.
