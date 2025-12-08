# Discuss-Then-Do Protocol (DTDP)

## Pre-requisites

Before you start, read the `Vibe Flow Guide.md` entirely. You need the `TASK_DIR`, `CYCLE_LETTER`, and next `FILE_NUMBER`.

## Phases

When the user initiates a DTDP, follow this four-phase process:

1. Investigation: research codebase to understand implementation.
2. Discussion: collaborate with the user to explore problem/solutions (mandatory step).
3. Action: implement only after user approval.
4. Summary: write concise summary of what was discussed and done.

## Phase 1. Investigation

Investigate the codebase and confirm the current behavior and required change.

## Phase 2. Discussion Phase

Discuss problem/goal exploration, current implementation, approach evaluation, and edge cases with the user.

## Phase 3. Action Phase

Only after user approval, implement the agreed solution. Maintain code style and scope, and communicate progress.

## Phase 4. Summary Phase

Create a summary file named `{CYCLE_LETTER}{FILE_NUMBER}-summary.md` in TASK_DIR describing the topic, decisions, actions, and outcomes.

_Important_: Ignore markdown linter errors in these files.
