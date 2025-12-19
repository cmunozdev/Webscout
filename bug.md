# AISEARCH Providers Bug Report

This report lists the AISEARCH providers that have bugs or issues identified by linting and runtime testing.

## Test Results (Running main blocks)

- **Genspark**: Working - Gave clean answer
- **Perplexity**: Not working - Gave raw JSON data instead of formatted answer
- **Monica**: Not working - No output (possibly API issue or auth required)
- **Stellar**: Not working - No output (possibly API issue or auth required)
- **webpilotai**: Not working - No output (possibly API issue or auth required)
- **IAsk**: Not working - Crashed with UnicodeEncodeError on print
- **PERPLEXED**: Not working - Crashed with UnicodeEncodeError on print

## Providers with Issues

### All Providers
All providers have linting issues (style, unused imports, whitespace, etc.) that should be fixed.

### Perplexity
**Status:** Not working - Critical bugs

**Bugs:**
- Method `search` signature incompatible with base class `AISearch`:
  - Parameter 3 name mismatch: base has `stream`, override has `mode`
  - Return type mismatch: returns `List[Any]` which is not allowed by base class
- `SearchResponse` is not iterable (missing `__iter__` method), but code tries to iterate over it in `__main__` block
- `_extract_answer` can return non-string types, causing issues in delta calculation and SearchResponse initialization
- Multiple bare `except` clauses (should catch specific exceptions)
- No newline at end of file
- Main block outputs raw data instead of clean answer

### Other Providers
**PERPLEXED, Genspark, IAsk, Monica, Stellar, webpilotai:**
- Various linting issues: unused imports, whitespace problems, import sorting
- Some have interactive main blocks requiring user input
- Encoding issues on Windows causing UnicodeEncodeError when printing responses
- No critical functional bugs identified beyond API access issues

## Recommendations
- Fix Perplexity search method signature to match base class
- Add `__iter__` method to `SearchResponse` if iteration is intended, or fix usage
- Ensure `_extract_answer` always returns string
- Replace bare `except` with specific exception handling
- Fix main blocks to use fixed prompts instead of input()
- Handle Unicode encoding issues for cross-platform compatibility
- Run `ruff check --fix` to auto-fix style issues
- Investigate API requirements for providers with no output