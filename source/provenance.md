# Transcript provenance

## Source

- Session ID: `019f746d-2d62-7c90-9326-fd89d3be29f7`
- Source file: `rollout-2026-07-18T03-52-20-019f746d-2d62-7c90-9326-fd89d3be29f7.jsonl`
- Cutoff timestamp: `2026-07-18T11:43:41.673Z`
- Raw user/assistant message records through cutoff: 98
- Rolled-back conversation entries excluded from the canonical conversation: 2
- Interactive prompt/response records included: 2
- Canonical transcript entries: 98

## Inclusion rules

- Include every `response_item` message whose role is `user` or `assistant`.
- Include `request_user_input` prompts and their matching user responses because they contain visible conversation decisions.
- Preserve message text exactly as stored. Add only transcript headings and timestamps.
- When one message record contains several text parts, concatenate those parts in source order with one LF; the transcript does not otherwise mark the part boundary.
- Generate transcript framing with LF while preserving any line-ending characters inside source message bodies; the transcript is marked non-normalizing in `.gitattributes`.
- Exclude entries belonging to a turn that the session records as rolled back.

## Exclusions

- System and developer instructions
- Hidden reasoning
- Ordinary shell, web, and collaboration tool calls and outputs
- Subagent traffic
- Event-stream bookkeeping other than rollback evidence

These records are implementation plumbing rather than human/assistant conversation. The interactive questionnaire is the exception because the user supplied decisions through it.

## Rollback and replay evidence

- Source line 356, User, SHA-256 `be5d288ed2756cfbf84beb3e384ee2e3882560ff98ebf804b54db4c02a5c63b0`; replayed at source line 369.
- Source line 669, User, SHA-256 `9d4eca07d13e161a4368f619f36d20bbb0af84f871ac5519f977762e693eb1dc`; replayed at source line 680.
- Turn `019f749b-f6e7-7ba0-a325-fee8a4773c1a` was aborted as `interrupted` at source line 360.
- Turn `019f74b5-8ce4-7de2-ba72-0645c289f904` was aborted as `interrupted` at source line 673.
- `thread_rolled_back` removed 1 turn(s) at source line 362.
- `thread_rolled_back` removed 1 turn(s) at source line 675.

Each rolled-back duplicate is omitted once from the canonical transcript because the event stream proves that its first turn was rolled back before the same user content was replayed. The underlying text and both source locations remain auditable here.

## Reproduction

Run from the repository root:

~~~powershell
./tools/export-origin-transcript.ps1 `
  -SessionPath '<path-to-session-jsonl>' `
  -CutoffTimestamp '2026-07-18T11:43:41.673Z'
~~~
