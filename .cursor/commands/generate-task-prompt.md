# Cursor Task Prompt Template

## Context

OpenSpec change: `<change-id>`
Task: `<task-id>`
Agent owner: `<agent>`

## Read first

- `openspec/changes/<change-id>/proposal.md`
- `openspec/changes/<change-id>/design.md`
- `openspec/changes/<change-id>/tasks.md`
- `openspec/changes/<change-id>/spec.md`
- `AGENTS.md`

## Implement

Implement only this task:

```text
<task description>
```

## Constraints

- No PII.
- No pictogram generation/modification.
- No export without human review.
- Visible attribution required.
- Tests required.

## Expected output

```text
summary:
files_changed:
tests_added:
tests_run:
risks:
```
