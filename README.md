# KNOWLEDGECRITICALSTRUCTUREPATRICKPLEASE

This repository preserves a hard-won product understanding: build an agent-native personal-scale knowledge-and-decision service whose normal agent-facing semantic interface is a narrow, stateless LLM translation layer inside the knowledge boundary. Broad work agents remain free and structure-blind; the internal layer mediates interpretation, encoding, automatic organization, storage, correction, retrieval, and useful return context through controlled knowledge-side tools. ([T055](source/origin-conversation-verbatim.md#t055---user), [T057](source/origin-conversation-verbatim.md#t057---user), [T059](source/origin-conversation-verbatim.md#t059---user), [T061](source/origin-conversation-verbatim.md#t061---user))

The graph, documents, workflows, state vocabulary, and harness are not the product. The transcript records why this boundary exists; the derived material should preserve and pressure-test that understanding without replacing it with process.

## Core understanding

1. [What we are building and why](docs/overview.md)
2. [Verbatim origin conversation](source/origin-conversation-verbatim.md), its [provenance](source/provenance.md), and the [checksum manifest](source/SHA256SUMS)
3. [Accepted synthesis, intent, and corrections](docs/intent-and-corrections.md)
4. [Knowledge structure: accepted core and candidate implications](docs/knowledge-structure.md)
5. [Goals and working requirements](docs/goals-and-requirements.md)

## Design-spike evidence

These are probes and durable design-spike evidence, not the identity of the project:

1. [Information-flow probe across the semantic boundary](docs/information-flow.md)
2. [Workflow catalog](docs/workflows.md)
3. [Candidate interaction traces](docs/interaction-traces.md)
4. [Simulation status and next review](docs/simulation-plan.md)
5. [Candidate behavior vocabulary](docs/behavior-model.md)
6. [Research basis](docs/research-basis.md)

## Current phase

- The [complete 98-entry conversation](source/origin-conversation-verbatim.md) is preserved verbatim and checksummed in the [manifest](source/SHA256SUMS).
- [The overview](docs/overview.md) now states the transcript-grounded product thesis and why each part of the boundary exists.
- Nine [workflow stories](docs/workflows.md) and 18 [fixtures](simulations/README.md) are candidate design probes. Their 97 declared steps are checked by the [replay tool](tools/run_simulations.py), not proof of semantic intelligence or accepted product behavior.
- [Automatic organization, semantic writeback, correction, conflict handling, and contextual retrieval](docs/simulation-plan.md#what-remains-unproven) remain the central unproven capabilities.
- The [current synthesis](docs/overview.md#current-truth) selects no database, graph model, ontology, runtime API, permanent component name, or production architecture.
