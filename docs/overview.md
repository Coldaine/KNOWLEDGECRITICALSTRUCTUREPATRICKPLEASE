# Overview

## Why this repository exists

- The N5 storage discussion exposed a documentation problem: storage knowledge was organized around one host and one document type when it belonged in several useful contexts. ([T032](../source/origin-conversation-verbatim.md#t032---user), [T038](../source/origin-conversation-verbatim.md#t038---user))
- The desired model is reusable knowledge pieces that can be linked automatically and used wherever they matter, rather than facts copied between document owners. ([T043](../source/origin-conversation-verbatim.md#t043---user), [T046](../source/origin-conversation-verbatim.md#t046---user))
- Large records and front matter are not the answer. Different pieces need different information, and agents do not receive every field by default. ([T046](../source/origin-conversation-verbatim.md#t046---user))
- This repository moves the idea out of one conversation and one person's head into durable, concise Markdown. ([T061](../source/origin-conversation-verbatim.md#t061---user), [T063](../source/origin-conversation-verbatim.md#t063---user))
- The complete conversation remains the source. Derived documents focus on the knowledge-system problem; N5 remains the motivating example. ([T066](../source/origin-conversation-verbatim.md#t066---user---interactive-response), [T069](../source/origin-conversation-verbatim.md#t069---user))

## Current intent

- This is primarily for agents. Human document rendering is not the problem to solve first. ([T051](../source/origin-conversation-verbatim.md#t051---user))
- External work agents remain focused on their actual tasks instead of learning the knowledge store's structure and mutation rules. ([T055](../source/origin-conversation-verbatim.md#t055---user), [T057](../source/origin-conversation-verbatim.md#t057---user))
- A narrow layer inside the knowledge boundary interprets requests, retrieves knowledge, and handles encoding, organization, storage, and correction. ([T055](../source/origin-conversation-verbatim.md#t055---user), [T061](../source/origin-conversation-verbatim.md#t061---user))
- The layer is stateless between requests, has only knowledge-transfer and knowledge-manipulation tools, and can therefore operate with small, clean context while the outside agent remains unrestricted in its own work. ([T055](../source/origin-conversation-verbatim.md#t055---user), [T057](../source/origin-conversation-verbatim.md#t057---user))
- “Translation layer” describes the intended role better than “knowledge agent.” It may reason across several tool calls, but it does not pursue an open-ended mission. ([T059](../source/origin-conversation-verbatim.md#t059---user), [T061](../source/origin-conversation-verbatim.md#t061---user))
- Its narrow role creates room for stronger enforcement around knowledge changes without constraining the long-running external agent. The exact enforcement behavior remains to be discovered through examples. ([T059](../source/origin-conversation-verbatim.md#t059---user), [T061](../source/origin-conversation-verbatim.md#t061---user))

## How the design will be discovered

- Preserve the source conversation, then distill its goals, requirements, and reasons. ([T061](../source/origin-conversation-verbatim.md#t061---user))
- Write primitive fictional workflows showing information arriving, being interpreted, transformed, stored, retrieved, corrected, or rejected. ([T061](../source/origin-conversation-verbatim.md#t061---user))
- Turn those workflows into diagrams and mini simulations, preserving each useful artifact as the model becomes clearer. ([T061](../source/origin-conversation-verbatim.md#t061---user))
- Use the simulations to discover components, distinctions, and possible states instead of assuming them first. ([T061](../source/origin-conversation-verbatim.md#t061---user))
- Design software only after the expected behavior is concrete enough to target. ([T061](../source/origin-conversation-verbatim.md#t061---user), [T063](../source/origin-conversation-verbatim.md#t063---user))

## Not decided

- No database, graph model, ontology, API, state machine, or permanent name has been selected. Earlier assistant examples are hypotheses to test, not adopted design. ([T048](../source/origin-conversation-verbatim.md#t048---user), [T061](../source/origin-conversation-verbatim.md#t061---user))
- This first phase explains the intent and tests behavior. It is not a software architecture. ([T061](../source/origin-conversation-verbatim.md#t061---user), [T063](../source/origin-conversation-verbatim.md#t063---user))
