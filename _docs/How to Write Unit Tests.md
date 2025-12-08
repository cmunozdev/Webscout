# How to Write Unit Tests

Tooling
- This project uses `pytest` for testing (`pyproject.toml` includes pytest in dev dependencies).

Running tests
- Run all tests: `python -m pytest`.
- Run tests in a single file: `python -m pytest path/to/test_file.py`.
- Run a subset: `pytest -k "pattern"` to match test names.
- Use `-q` for quiet output and `-x` to stop after the first failure.

Writing tests
- Name test files `test_*.py` and place them under a `tests/` directory or next to the module under test.
- Use `def test_xxx():` function names for `pytest` discovery (or `unittest` style with `class` derived from `unittest.TestCase`).
- For network-bound code (many Provider clients), use mocking to avoid external API calls. Prefer `pytest` fixtures and `monkeypatch` or specialized mocking libraries (e.g., `pytest-mock`, `requests-mock`).
- When testing async code, use `pytest.mark.asyncio` or `anyio` where appropriate.

Notes
- If you add tests that rely on environment variables or API keys, prefer using environment-based fixtures and avoid leaking real credentials in CI.
- Focus on small, deterministic unit tests that validate core logic rather than integration with external providers, unless an integration test is specifically requested.
