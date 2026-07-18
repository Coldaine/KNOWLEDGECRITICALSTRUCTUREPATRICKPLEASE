# KNOWLEDGECRITICALSTRUCTUREPATRICKPLEASE

The name is intentionally hard to ignore. This repository gets a critical knowledge-system idea out of one conversation and into durable material that can be inspected, corrected, simulated, and eventually implemented. ([T063](source/origin-conversation-verbatim.md#t063---user), [T066](source/origin-conversation-verbatim.md#t066---user---interactive-response))

This is not a software architecture yet. It preserves the source, states the intent, and works from concrete behavior toward a design. ([T061](source/origin-conversation-verbatim.md#t061---user), [T063](source/origin-conversation-verbatim.md#t063---user))

## Read in this order

1. [Verbatim origin conversation](source/origin-conversation-verbatim.md), its [provenance](source/provenance.md), and the [checksum manifest](source/SHA256SUMS)
2. [Overview](docs/overview.md)
3. [Intent and corrections](docs/intent-and-corrections.md)
4. [Goals and working requirements](docs/goals-and-requirements.md)
5. [Information flow across the knowledge boundary](docs/information-flow.md)
6. [Workflow catalog](docs/workflows.md)
7. [Candidate interaction traces](docs/interaction-traces.md)
8. [Provisional behavior model](docs/behavior-model.md)
9. [Simulation and harness plan](docs/simulation-plan.md)
10. [Research basis](docs/research-basis.md)

## Current phase

- The source conversation is frozen and checksummed in the [manifest](source/SHA256SUMS).
- User intent is separated from assistant proposals and rejected directions. ([T061](source/origin-conversation-verbatim.md#t061---user), [T063](source/origin-conversation-verbatim.md#t063---user))
- Eight [workflow stories](docs/workflows.md) name the behaviors to investigate; the [interaction traces](docs/interaction-traces.md) now expose the information carried across every boundary and the hidden prerequisites for each intermediate step.
- The [information-flow model](docs/information-flow.md) separates semantic work a bounded model can perform from retrieval, persistence, and protocol behavior that tools must supply.
- Candidate states and lifecycles remain provisional. ([T061](source/origin-conversation-verbatim.md#t061---user))
- No database, ontology, graph model, API, framework, or permanent component name has been selected. ([T061](source/origin-conversation-verbatim.md#t061---user), [T063](source/origin-conversation-verbatim.md#t063---user))
