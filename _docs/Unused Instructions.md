# Unused Instructions

This file is generated to help AI agents and contributors become productive quickly in this codebase. Read the files below as needed and prefer short, targeted reads instead of broad changes.

- Project: Webscout — a Python package providing search, AI provider integrations, TTS/TTI helpers, and a CLI/server wrapper.
- Important entry points:
  - `webscout/` — primary Python package; `webscout/Provider/` contains AI provider integrations.
  - `webscout/cli.py` — CLI app entry point. Use `python -m webscout.cli` or the console scripts (`webscout`, `WEBS`).
  - `webscout/server/server.py` — start the OpenAI-compatible web server via `webscout-server` script.
  - `pyproject.toml` — project configuration; dependency and scripts are defined here.

Developer workflows and tools:
- Tests: `pytest` is the test runner (see `pyproject.toml`). Use `python -m pytest` to run all tests, `pytest -k "pattern"` for a subset.
- Linting/formatting: `ruff` is configured in `pyproject.toml` (`line-length=100`). Run `ruff check .` to lint; `ruff format .` to autoformat if configured.
- To run the main CLI locally: `pip install -e .` then `webscout` on the command line or `python -m webscout.cli`.

Repository structure recommendations:
- Focus changes in the `webscout` package unless the task explicitly suggests otherwise.
- Preserve backward compatibility with provider modules in `webscout/Provider/` as many integrations depend on consistent interfaces.

Code review notes and common patterns:
- Provider classes often implement `.chat()` and `.stream()` interfaces. Follow existing patterns when adding new provider modules.
- Prefer `orjson` for JSON serialization where used and follow existing use of `asyncio` where present.

Important policies for agent assistants:
- Always prefer reading `_docs/Code Style Guidelines.md` (to be added) before making style-related changes.
- Never modify the `_plans` directory; it is ignored in search and for diffs.

If you find gaps in these instructions, propose minimal, testable changes to update this file.
