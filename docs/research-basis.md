# Research basis

## Short answer

This spike is not copied from one established “knowledge agent” pattern. It deliberately composes a few small, useful ideas from requirements discovery, traceability, behavioral modeling, testing, and safety analysis. That is appropriate because the uncertain layer here does more than retrieve: it interprets incoming intent and evidence, encodes and organizes knowledge, preserves provenance and corrections, and returns bounded context. The transcript explicitly warns against collapsing that work into the familiar retrieval-agent category and asks for corpus preservation, requirements distillation, workflows, simulations, state discovery, and only then design. ([T061](../source/origin-conversation-verbatim.md#t061---user), [T062](../source/origin-conversation-verbatim.md#t062---assistant), [T063](../source/origin-conversation-verbatim.md#t063---user), [T064](../source/origin-conversation-verbatim.md#t064---assistant))

No source below is adopted wholesale. Each contributes one technique to the [simulation plan](simulation-plan.md).

## Techniques being borrowed

| Borrowed idea | Primary or official source | Use here | Not imported |
| --- | --- | --- | --- |
| Preserve the chain from source material to derived assertions and revisions | [W3C PROV-O](https://www.w3.org/TR/prov-o/) | Keep submitted evidence distinct from interpretation, correction, and derived context; make every derived artifact traceable | RDF, the full PROV ontology, or a chosen storage representation |
| Describe stakeholder behavior before implementation, including nominal and off-nominal cases | [NASA Systems Engineering Handbook](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf) (Concept of Operations) | Write backend-neutral normal, degraded, ambiguous, and failure workflows before components | A full ConOps package or NASA lifecycle |
| Start with concrete stories and only then collect abstractions and rules | [Domain Storytelling quick-start guide](https://domainstorytelling.org/quick-start-guide) | Use numbered, primitive stories to discover responsibilities and meaningful alternatives | Its notation as a mandatory diagram format or a complete domain-design process |
| Organize a behavior around a rule, concrete examples, and unresolved questions | [Cucumber Example Mapping](https://cucumber.io/docs/bdd/example-mapping/) | Keep scenario purpose, examples, acceptance signals, and open questions connected | Card ceremonies, Gherkin, or BDD as the implementation method |
| Represent legal state configurations and transitions when the examples justify them | [W3C SCXML](https://www.w3.org/TR/scxml/) | Give later state-machine work a precise reference vocabulary | SCXML documents, event transports, or one universal state machine selected in advance |
| State preconditions, postconditions, and invariants as observable contracts | [Eiffel Design by Contract](https://www.eiffel.org/doc/eiffel/ET-_Design_by_Contract_%28tm%29%2C_Assertions_and_Exceptions) | Turn checks and expected diffs into harness assertions | Eiffel, class contracts, or language-specific runtime machinery |
| Explore sequences of actions against a reference model | [Hypothesis stateful testing](https://hypothesis.readthedocs.io/en/latest/stateful.html) and [NIST on model-based software testing](https://www.nist.gov/publications/model-checkers-software-testing) | After handwritten traces stabilize, generate repeats, reorderings, invalid transitions, and fault sequences against the in-memory model | A committed testing library, formal verification claim, or generated examples before behavior is understood |
| Ask which action, omission, timing, or ordering could create an unacceptable result | [MIT Partnership for Systems Approaches to Safety and Security, STPA handbooks](https://psas.scripts.mit.edu/home/books-and-handbooks/) | Pressure-test semantic writes, conflict handling, deletion, partial completion, and stale context with a small set of hazard questions | A full STPA program, safety certification, or its complete terminology |
| Compare architectural candidates using scenarios and quality tradeoffs | [Carnegie Mellon SEI ATAM](https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/) | Later, compare candidate architectures against the accepted traces and quality concerns they expose | A formal multi-day ATAM exercise during this behavior-discovery phase |

This is intentionally a light composition: traceability keeps the derivation honest; concrete scenarios make behavior reviewable; contracts and state models make accepted behavior executable; adversarial and model-based tests probe sequences; architecture comparison waits for evidence.

## Why there is no single settled pattern to adopt

Adjacent systems establish important pieces, but their documented boundaries do not settle the whole semantic write path:

- [Microsoft GraphRAG](https://microsoft.github.io/graphrag/index/overview/) documents a pipeline that extracts structured knowledge for graph-based query. It is strong evidence for indexing and retrieval patterns, not a complete contract for governed correction, organization, and multi-step semantic writes.
- [Graphiti's official MCP server](https://github.com/getzep/graphiti/blob/main/mcp_server/README.md) exposes temporal episode ingestion and entity/relationship search and management. It is closer to incremental knowledge handling, but it does not by itself establish the desired separation between an outside work agent, an interpretive mediation layer, and deterministic acceptance behavior.
- [Palantir Agents](https://www.palantir.com/docs/foundry/agents/overview) and the [Palantir Ontology](https://www.palantir.com/docs/foundry/ontology/overview) demonstrate scoped tools, semantic objects, relationships, and governed actions at organizational scale. They are useful reference points, not a small-system specification or proof that their object/action model fits this problem.

The inference from those official boundaries is narrow: there is no single settled, product-neutral pattern among them for a small, stateless LLM-mediated layer that accepts free-form intent and evidence and is responsible for interpretation, encoding, organization, correction, retrieval, and traceable results. That absence is why this repository starts with behavioral traces instead of selecting a product category.

## Private prototypes are question sources, not inheritance

Earlier private experiments were inspected for useful failure questions: whether shaped graph imports push interpretation outside the desired boundary, whether a model survives concrete task pressure, and whether declared structure matches observed query behavior. They are intentionally not linked or used as required evidence in this public repository. This spike inherits no database, entity model, schema, importer contract, or lifecycle assumption from them.

## Resulting method for this repository

1. Preserve the complete source corpus and cite it from every derived claim.
2. Distill goals and corrections without promoting prior assistant suggestions into decisions.
3. Write concrete normal and adversarial workflows, then normalize them into reviewable Markdown golden traces.
4. Derive candidate distinctions, states, transitions, and contracts only from those traces.
5. Replay accepted traces in a disposable in-memory reference harness and pressure-test retries, reordering, conflict, and partial failure.
6. Compare databases, schemas, models, tools, and component boundaries only after that behavior survives review and replay.

This method is a design-spike process, not the architecture it may eventually justify.
