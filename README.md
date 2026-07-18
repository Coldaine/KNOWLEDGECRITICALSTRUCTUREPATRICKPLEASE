# KNOWLEDGECRITICALSTRUCTUREPATRICKPLEASE

The name is intentionally hard to ignore. This repository gets a critical knowledge-system idea out of one conversation and into durable material that can be inspected, corrected, simulated, and eventually implemented. ([T063](source/origin-conversation-verbatim.md#t063---user), [T066](source/origin-conversation-verbatim.md#t066---user---interactive-response))

This is not a software architecture yet. It preserves the source, states the intent, and works from concrete behavior toward a design. ([T061](source/origin-conversation-verbatim.md#t061---user), [T063](source/origin-conversation-verbatim.md#t063---user))

## Read in this order

1. [Verbatim origin conversation](source/origin-conversation-verbatim.md), its [provenance](source/provenance.md), and the [checksum manifest](source/SHA256SUMS)
2. [Overview](docs/overview.md)
3. [Intent and corrections](docs/intent-and-corrections.md)
4. [Goals and working requirements](docs/goals-and-requirements.md)
5. [Knowledge structure under test](docs/knowledge-structure.md)
6. [Information flow across the knowledge boundary](docs/information-flow.md)
7. [Workflow catalog](docs/workflows.md)
8. [Candidate interaction traces](docs/interaction-traces.md)
9. [Trace-derived behavior model](docs/behavior-model.md)
10. [Simulation status and next review](docs/simulation-plan.md)
11. [Research basis](docs/research-basis.md)

## Current phase

- The source conversation is captured verbatim through the latest workflow correction and checksummed in the [manifest](source/SHA256SUMS). ([T096](source/origin-conversation-verbatim.md#t096---user), [T098](source/origin-conversation-verbatim.md#t098---user))
- User intent is separated from assistant proposals and rejected directions. ([T061](source/origin-conversation-verbatim.md#t061---user), [T063](source/origin-conversation-verbatim.md#t063---user))
- The [knowledge-structure document](docs/knowledge-structure.md) makes reusable pieces, sparse shape, organization, provenance, history, and retrieval paths the project's center rather than treating N5 scenarios as the product.
- Eight [workflow stories](docs/workflows.md) name the behaviors to investigate; the [interaction traces](docs/interaction-traces.md) now expose the information carried across every boundary and the hidden prerequisites for each intermediate step.
- The [information-flow model](docs/information-flow.md) separates semantic work a bounded model can perform from retrieval, persistence, and protocol behavior that tools must supply.
- Sixteen [schema-blind fixtures](simulations/README.md) replay the eight primary flows and their first pressure variations; they currently validate 86 explicit steps without selecting a production schema.
- Candidate states and lifecycles remain provisional. ([T061](source/origin-conversation-verbatim.md#t061---user))
- No database, ontology, graph model, API, framework, or permanent component name has been selected. ([T061](source/origin-conversation-verbatim.md#t061---user), [T063](source/origin-conversation-verbatim.md#t063---user))
