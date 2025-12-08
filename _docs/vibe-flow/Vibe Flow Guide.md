# Vibe Flow Guide

## TASK_DIR Location

`TASK_DIR` is the directory where work files related to a task are stored, usually `_plans/{TICKET_ID}/`. If no ticket ID is known, ask the user for it.

- Create TASK_DIR if it doesn't exist.
- Or list existing files.

## File Naming Convention

Format: `{CYCLE_LETTER}{FILE_NUMBER}-{FILE_TYPE}.md`.

Common file types:
- `spec` — technical specification
- `plan` — implementation plan
- `summary` — implementation summary

Example structure:

```text
_plans/
├── 123/
│   ├── A1-spec.md
│   ├── A2-plan.md
│   ├── A3-summary.md
│   └── B1-spec.md
```

## Notes

- TICKET_ID is a unique identifier for the task (issue or ticket number).
- Cycles identified by `CYCLE_LETTER` (A, B, C...). The user decides when to start a new one.
- Determine the next FILE_NUMBER from existing file names.
- Start `CYCLE_LETTER` with `A` if no existing cycle; `FILE_NUMBER` starts at 1.
- When starting a new cycle, bump the `CYCLE_LETTER` and reset `FILE_NUMBER`.
- File types are flexible.
