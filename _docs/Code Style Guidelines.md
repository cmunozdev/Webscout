# Code Style Guidelines

This repository uses Python 3.9+ and follows a minimal set of style rules observed in the codebase rather than general best practices.

- Formatting and linting
  - `ruff` is the configured linter (see `pyproject.toml`). Run `ruff check .` to lint and `ruff format .` to autoformat where supported.
  - Line length: 100 characters.
  - Target Python version: 3.9 (`pyproject.toml` target-version = "py39").
  - Ruff `select`: E,F,W,I; ignored rules include E501 (long lines are allowed up to 100 chars in this repo).

- Typing
  - Use explicit `typing` annotations in public functions and classes where present (e.g., `def func(arg: str) -> None`). Many files use `typing` consistently.

- Indentation and style
  - Use 4 spaces for indentation.
  - Use meaningful docstrings for public functions.
  - Use f-strings for formatted output where present (e.g., `f"..."`).

- Concurrency and JSON
  - Prefers `asyncio` in code that needs concurrency; follow existing patterns of `async def` or `.chat()`/`.stream()` style in provider modules.
  - For serialization performance, the project depends on `orjson`. Where JSON is used heavily, prefer using `orjson.dumps`/`orjson.loads`.

- Compatibility
  - Maintain backward compatible interfaces for provider clients in `webscout/Provider/`. New provider code should match existing method signatures (e.g. `.chat()`, `stream`, `timeout` param patterns).

If a rule is not obvious in the code, prefer asking a reviewer rather than introducing sweeping style changes.
