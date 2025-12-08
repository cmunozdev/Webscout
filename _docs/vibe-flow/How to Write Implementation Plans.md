# How to Write Implementation Plans

## Pre-requisites

Before you start, read the `Vibe Flow Guide.md` entirely.
- Determine `TASK_DIR`, `CYCLE_LETTER`, and `FILE_NUMBER`.
- Ensure you have a spec file in `_plans/{TASK_DIR}/`.

If any required information is missing, STOP AND ASK THE USER.

## Phases

1. Investigation: Explore the codebase and validate the spec.
2. Analysis: Decide if the work is a single plan or multiple plans and assign subagents.
3. Designing: Create plan(s). If multiple plans, create an orchestrator plan too.
4. Writing: Write the plan file(s).
5. Review: Critically review plans and ensure they are self-contained and coherent.

### Common guidelines
- The plan must be a self-explanatory prompt for a coding agent.
- Include a 'Prerequisites' section listing relevant `_docs` files, always include `Code Style Guidelines.md`.
- Mention important source files by path or by function name.
- For multiple plans, add an orchestrator plan coordinating execution and a handover step for each plan.
- Don't add backward compatibility unless requested. Prefer clean code and remove unused code.
- Investigate tests first; don't assert to write tests if they won't integrate well.

### Plan structure
- Single plan: `_plans/{TASK_DIR}/{CYCLE_LETTER}{FILE_NUMBER}-plan.md` (e.g., `_plans/123/A2-plan.md`)
- Orchestrator: `_plans/{TASK_DIR}/{CYCLE_LETTER}{FILE_NUMBER}-plan-orchestrator.md`
- Specialized plans: `_plans/{TASK_DIR}/{CYCLE_LETTER}{FILE_NUMBER}-plan-{descriptor}.md`
- Each plan must end with a handover writing step and a final footer: "Do not trust this plan blindly..."

_Important_: Ignore markdown lint errors in spec and plan files.
