# How to Write a Technical Specification

## Pre-requisites

Before you start, read the `Vibe Flow Guide.md` entirely. You need:

- the TASK_DIR – if you don't have it, ask the user for a ticket ID
- the current CYCLE_LETTER and the next FILE_NUMBER - deduce them; by default, start a new cycle

## Phases

When the user asks for a SPEC, follow this process:

1. Investigation Phase: research the codebase to understand the current implementation and identify the problem.
2. Discussion Phase: collaborate with the user to explore the problem space and potential solutions BEFORE writing the specification.
3. Specification Phase: after user approval, write the final specification file.

The Discussion Phase is MANDATORY. You're a newcomer; ask the user for clarifications and confirm architectural choices.

## Phase 1. Investigation

Investigate the codebase, find relevant source code, and determine the minimal changes needed to implement the requested behavior.

## Phase 2. Discussion

Engage in a collaborative discussion covering problem exploration, current implementation analysis, multiple solution approaches, sub-subject identification, design decisions, and edge cases.

## Phase 3. Specification Phase

After the user approves your proposal, write the specification in a markdown file in TASK_DIR, named using the CYCLE_LETTER and FILE_NUMBER (e.g., `A1-spec.md`). Usually a specification is around 40–60 lines and focuses on the problem and the solution.

Do not include large code blocks; refer to existing files and functions by path/name rather than line numbers.

_Important_: Do not add backward compatibility unless requested, and ignore markdown linter errors in spec files.
