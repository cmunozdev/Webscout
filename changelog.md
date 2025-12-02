# Changelog

All notable changes to this project will be documented in this file.

## [2025.12.02] - 2025-12-02

### ✨ Added
 - **feat**: webscout/search/engines/__init__.py - Updated auto-discovery logic to register all search engine classes with `name` and `category` attributes, not just BaseSearchEngine subclasses
 - **feat**: webscout/server/routes.py - Enhanced `/search` endpoint to support all available search engines and additional search types (answers, maps, translate, weather, videos)
 - **feat**: webscout/server/routes.py - Added new query parameters to `/search` endpoint: `place`, `street`, `city`, `county`, `state`, `country`, `postalcode`, `latitude`, `longitude`, `radius`, `from_`, `to`, `language`
 - **feat**: added all engines to cli.py 
 - **feat**: cli.py - Added CLI commands for Bing search (text, images, news, suggestions)
 - **feat**: cli.py - Added CLI commands for Yahoo search (text, images, videos, news, answers, maps, translate, suggestions, weather)

### 🔧 Maintenance
 - **refactor**: Added `name` and `category` attributes to all DuckDuckGo search engine classes (text, images, videos, news, suggestions, answers, maps, translate, weather)
 - **refactor**: Added `name` and `category` attributes to Bing search engine classes (text, images, news, suggestions)
 - **refactor**: Added `name` and `category` attributes to Yep search engine classes (text, images, suggestions)
 - **refactor**: Updated webscout/search/engines/bing/__init__.py to import and expose Bing search engine classes
 - **refactor**: Updated `/search` endpoint description to reflect support for all available search engines and search types
 - **refactor**: prompt_manager.py - Removed unused imports, redundant code, and cleaned up class for clarity and minimalism
 - **chore**: prompt_manager.py - Minor optimizations and code style improvements
 - **refactor**: cli.py - Cleaned up incomplete command stubs and fixed inconsistencies in option decorators
 - **removed**: cli.py - Removed unused imports and broken command implementations

### 📝 Documentation
 - **docs**: Updated changelog for prompt_manager.py maintenance changes

## [2025.12.01] - 2025-12-01
### ✨ Added
 - **feat**: sanitize.py - Added `output_formatter` parameter to `sanitize_stream()` for custom output transformation
 - **feat**: sanitize.py - Users can now define custom formatter functions to transform each output item into any desired structure before yielding

### 🚮 Removed
 - **removed**: sanitize.py - Removed built-in response formatters (`ResponseFormatter`, `OutputFormat`, `create_openai_response`, `create_openai_stream_chunk`, `create_anthropic_response`, `create_anthropic_stream_chunk`, `format_output`) in favor of user-defined `output_formatter` functions
 - **removed**: sanitize.py - Removed `output_format` and `format_options` parameters from `sanitize_stream()` - use `output_formatter` instead

### 📝 Documentation
 - **docs**: sanitize.md - Updated documentation with `output_formatter` parameter and usage examples
 - **docs**: sanitize.md - Removed references to removed built-in formatters

## [2025.11.30] - 2025-11-30

### 🔧 Maintenance
 - **refactor**: Added missing `# type: ignore` to imports for optional dependencies (trio, numpy, tiktoken, pandas) in multiple modules for better compatibility and linting
 - **refactor**: Improved type hints and error handling in `scout/core/crawler.py` and `scout/core/scout.py`
 - **refactor**: Updated `oivscode.py` to generate and use a unique ClientId (UUID) in headers
 - **refactor**: Updated CLI group import in `swiftcli/core/cli.py` to avoid circular dependency
 - **refactor**: Minor docstring and comment cleanups in AISEARCH providers
 - **chore**: Removed unfinished providers: `Aitopia.py`, `VercelAIGateway.py`, `puterjs.py`, `scira_search.py`, `hika_search.py` from Provider/UNFINISHED and Provider/AISEARCH

### 🐛 Fixed
 - **fix**: Fixed error handling in `sanitize.py` async stream processing (removed logger usage in extractor error branch)
 - **fix**: Fixed import and type hint issues in `duckduckgo/base.py`, `search/http_client.py`, `Provider/cerebras.py`, and others
 - **fix**: Fixed streaming output and test code in `genspark_search.py`, `PERPLEXED_search.py`, and `iask_search.py` for more robust CLI testing
 - **fix**: Fixed YahooSearch import for Dict type in `search/yahoo_main.py`

### 🚮 Removed
 - **removed**: Deleted unfinished provider files: `Aitopia.py`, `VercelAIGateway.py`, `puterjs.py`, `scira_search.py`, `hika_search.py` for codebase cleanup

### 🐛 Fixed
 - **fix**: TogetherAI.py - Updated API endpoint from `https://chat.together.ai/api/chat-completion` to `https://api.together.xyz/v1/chat/completions` for compatibility with the public Together API
 - **fix**: TogetherAI.py - Fixed payload parameters to use OpenAI-compatible format (`model`, `max_tokens`, `top_p` instead of `modelId`, `maxTokens`, `topP`)
 - **fix**: OPENAI/TogetherAI.py - Removed self-activation endpoint logic that auto-fetched API keys from external service

### ✨ Added
 - **feat**: TogetherAI.py - Implemented dynamic model loading from `https://api.together.xyz/v1/models` API, similar to Groq provider
 - **feat**: TogetherAI.py - Added `get_models()` and `update_available_models()` class methods for automatic model discovery
 - **feat**: OPENAI/TogetherAI.py - Added dynamic model loading support with automatic model list updates on initialization
 - **feat**: OPENAI/TogetherAI.py - Now requires user-provided API key via `api_key` parameter, following Groq provider pattern

### 🔧 Maintenance
 - **refactor**: TogetherAI.py - Changed `AVAILABLE_MODELS` from hardcoded dictionary to dynamically populated list
 - **refactor**: TogetherAI.py - Updated model validation to handle empty model lists gracefully when API fetch fails
 - **refactor**: OPENAI/TogetherAI.py - Removed `activation_endpoint` and `get_activation_key()` method for better security practices
 - **refactor**: OPENAI/TogetherAI.py - Updated `__init__` to accept `api_key` parameter and conditionally update models if key is provided

## [2025.11.21] - 2025-11-21

### 🐛 Fixed
 - **fix**: FreeGemini.py - Fixed `TypeError: Session.request() got an unexpected keyword argument 'impersonate'` by overriding the parent class's `requests.Session` with `curl_cffi.requests.Session` to support browser impersonation for bypassing bot detection
 - **fix**: IBM.py - Fixed typo in `refresh_identity` method where `s-elf.headers` was incorrectly used instead of `self.headers`
 - **fix**: AIauto.py - Fixed critical bug where `chat` method could return a generator when `stream=False`, causing `AssertionError` in providers like AI4Chat
 - **fix**: AIauto.py - Added proper handling for providers that return generators even in non-streaming mode by consuming the generator to extract the return value

### ✨ Added
 - **feat**: AIauto.py - Enhanced provider failover mechanism to "peek" at the first chunk of streaming responses, allowing automatic failover to next provider if current one fails immediately
 - **feat**: AIauto.py - Split `chat` method into `_chat_stream` and `_chat_non_stream` helper methods for clearer separation of streaming vs non-streaming logic
 - **feat**: OPENAI/ibm.py - Added OpenAI-compatible IBM Granite provider in `webscout/Provider/OPENAI/` with support for `granite-chat` and `granite-search` models
 - **feat**: OPENAI/ibm.py - Implemented using `format_prompt()` and `count_tokens()` utilities from utils.py for proper message formatting and accurate token counting
 - **feat**: OPENAI/ibm.py - Manual SSE (Server-Sent Events) stream parsing without sanitize_stream dependency, consistent with other OPENAI providers

### 🔧 Maintenance
 - **refactor**: AIauto.py - Improved robustness of AUTO provider to work seamlessly with all providers in webscout.Provider package
 - **refactor**: AIauto.py - Added generator type checking and handling to prevent type mismatches between streaming and non-streaming responses

## [2025.11.20] - 2025-11-20

### 🐛 Fixed
 - **fix**: sanitize.py - Fixed critical async stream processing logic error where variable `idx` was used outside its conditional scope, causing potential `UnboundLocalError`
 - **fix**: sanitize.py - Fixed Python 3.9+ compatibility issue by replacing `Pattern` from typing with `re.Pattern` for proper isinstance() checks

### 🔧 Maintenance
 - **refactor**: sanitize.py - Reorganized imports for better structure (moved chain, functools, asyncio to top level)
 - **chore**: sanitize.py - Added `__all__` export list for explicit public API definition
 - **docs**: sanitize.py - Added comprehensive module docstring
 - **refactor**: sanitize.py - Updated all type hints to use modern syntax with `re.Pattern[str]`
 - **refactor**: Apriel.py - Simplified raw mode streaming logic for better performance

## [2025.11.19] - 2025-11-19

### 🔧 Maintenance
 - **chore**: Bard - added `gemini-3-pro` model with appropriate headers to `BardModel` enum
 - **GEMINI** - added `gemini-3-pro` model support in `GEMINI` class
 - **feat**: Updated search engines to use dataclass objects from results.py for better type safety and consistency
 - **refactor**: Updated all Providers to use `raw` flag of sanatize_stream for easy debugging
 - **removed**: Removed Cloudflare Provider

### 🐛 Fixed
 - **fix**: ChatGPT provider - Fixed OpenAI compatibility issues in `webscout/Provider/OPENAI/chatgpt.py` by updating streaming and non-streaming implementations to properly handle Server-Sent Events format and match OpenAI's response structure exactly
 - **fix**: ChatGPT provider - Enhanced error handling and parameter validation to follow OpenAI conventions
 - **fix**: AkashGPT provider - Fixed authentication issue in `webscout/Provider/akashgpt.py` by updating API key handling to use cookies for authentication

### ✨ Added
 - **feat**: ChatGPT provider - Added new models to AVAILABLE_MODELS including `gpt-5-1`, `gpt-5-1-instant`, `gpt-5-1-thinking`, `gpt-5`, `gpt-5-instant`, `gpt-5-thinking`
 - **feat**: New Provider: Algion with `gpt-5.1`and other models
## [2025.11.17] - 2025-11-17

### 🔧 Maintenance
 - **fix**: swiftcli - improved argument parsing: support `--key=value` and `-k=value` syntax; handle repeated flags/options (collected into lists)
 - **fix**: swiftcli - `convert_type` now handles boolean inputs and list-typed values robustly
 - **feat**: swiftcli - added support for option attributes: `count`, `multiple`, and `is_flag`; option callbacks supported; `choices` validation extended to multiple options
 - **fix**: swiftcli - option decorator uses a sentinel for unspecified defaults to avoid overriding function defaults with `None`
 - **feat**: swiftcli - CLI and `Group` now support the `@pass_context` decorator to inject `Context` and can run `async` coroutine commands
 - **fix**: swiftcli - help output deduplicates commands and displays aliases clearly; group help deduplicated and improved formatting
 - **test**: swiftcli - added comprehensive unit tests covering parsing, option handling (count/multiple/choices), `pass_context`, async behavior, group commands, and plugin manager lifecycle
 - **chore**: swiftcli - updated README with changelog, improved examples, and removed temporary debug/test helper files
 - **testing**: All swiftcli tests added in this change pass locally (14 tests total)

## [2025.11.16] - 2025-11-16
- **feat**: added `moonshotai/Kimi-K2-Thinking` and `MiniMaxAI/MiniMax-M2` models to DeepInfra provider AVAILABLE_MODELS in both `webscout/Provider/Deepinfra.py` and `webscout/Provider/OPENAI/deepinfra.py`
- **feat**: 

###  Maintenance
- **feat**: fixed formating issue in HeckAI replaced `strip_chars=" \n\r\t",`  with `strip_chars=""`
- **chore**: updated CHANGELOG.md to changelog.md in MANIFEST.in for consistency
- **chore**: updated release-with-changelog.yml to handle multiple version formats in changelog parsing
- **feat**: Updated changelog parsing to recognize multiple version formats (e.g., "vX.Y.Z", "X.Y.Z") for improved release automation.
- **feat**: updated `sanitize_stream` to support both `extract_regexes` and `content_extractor` at same time
- **chore**: updated `release-with-changelog.yml` to normalize version strings by stripping leading 'v' or 'V'
- **chore**: updated `sanitize_stream` docstring to clarify usage of `extract_regexes` and `content_extractor`
- **chore**: removed deprected models from venice provider
- **chore**: updated venice provider model list in AVAILABLE_MODELS
- **chore**: updated models list in textpollionations provider
- **chore**: replaced `anthropic:claude-3-5-haiku-20241022` with `anthropic:claude-haiku-4-5-20251001` in typefully provider 

### Added
- **feat**: added `anthropic:claude-haiku-4-5-20251001` to typefully provider AVAILABLE_MODELS
- **feat**: New IBM provider with `granite-search` and `granite-chat` models 

## [2025.11.06] - 2025-11-06

### 🔧 Maintenance
- **chore**: Remove GMI provider (a8928a0) — Cleaned up provider roster by removing GMI to simplify maintenance and reduce duplicate or deprecated provider support.

## [2025.10.22] - 2025-10-22

### ✨ Added
- **feat**: Add `claude-haiku-4.5` model to Flowith provider (3a80249) — Flowith now supports additional Claude variants for creative text generation.
- **feat**: Add `openai/gpt-oss-20b` and `openai/gpt-oss-120b` models to GMI provider (3a80249) — Added support for larger OSS GPT models via GMI.

### 🔧 Maintenance
- **refactor**: Change `DeepAI` `required_auth` to `True` (3a80249) — Ensure DeepAI provider requires authentication for API access.
- **chore**: Add import error handling for `OLLAMA` provider (3a80249) — Graceful degradation when optional dependencies are missing.
- **chore**: Remove deprecated `FalconH1` and `deepseek_assistant` providers (3a80249) — Reduced clutter and removed unsupported providers.
- **chore**: Update `OPENAI`, `flowith`, and `gmi` providers with new model lists and aliases (3a80249) — Keep model availability up-to-date and consistent.

## [2025.10.18] - 2025-10-18

### 🚀 Major Enhancements
- **🤖 AI Provider Expansion**: Integrated SciRA-AI and SciRA-Chat providers, adding robust model mapping and aliasing to unify behavior across providers.

### 📦 Package Structure
- **🛠️ Model Mapping System**: Introduced `MODEL_MAPPING` and `SCI_RA_TO_MODEL` dictionaries and updated `AVAILABLE_MODELS` lists to keep model names consistent and avoid duplication.

### ⚡ Improvements
- **🔄 Enhanced Model Resolution**: Improved `convert_model_name` and `_resolve_model` logic to better handle aliases, fallbacks, and unsupported names with clearer error messages.
- **🧪 Test and Example Updates**: Updated provider `__main__` blocks to list available models and print streaming behavior for easier local testing.
- **📝 Documentation**: Improved docstrings and comments clarifying model resolution and provider behavior.

### 🔧 Refactoring
- **⚙️ Provider Interface Standardization**: Refactored provider base classes and initialization logic to standardize how models are selected and aliases are resolved.

## [2025.10.17] - 2025-10-17

### ✨ Added
- **feat**: Add `sciRA-Coding` and `sciRA-Vision` providers (7e8f2a1)
- **feat**: Add `sciRA-Reasoning` and `sciRA-Analyze` providers (7e8f2a1)

### 🔧 Maintenance
- **chore**: Update provider initialization logic to more robustly support new sciRA families (7e8f2a1)
- **chore**: Add comprehensive model listings for newly added providers (7e8f2a1)

## [2025.10.16] - 2025-10-16

### ✨ Added
- **feat**: Add `sciRA-General` and `sciRA-Assistant` providers (9c4d1b3)
- **feat**: Add `sciRA-Research` and `sciRA-Learn` providers (9c4d1b3)

### 🔧 Maintenance
- **chore**: Refactor provider base classes for improved extensibility (9c4d1b3)
- **chore**: Add model validation logic to avoid exposing unsupported names (9c4d1b3)

## [2025.10.15] - 2025-10-15

### ✨ Added
- **feat**: Introduce SciRA provider framework and initial model mappings (5a2f8c7)

### 🔧 Maintenance
- **chore**: Set up SciRA provider infrastructure and basic authentication handling (5a2f8c7)

## [2025.10.10] - 2025-10-10

### ✨ Added
- **feat**: Add Flowith provider with multiple model support (b3d8a21)
- **feat**: Add GMI provider with advanced model options (b3d8a21)

### 🔧 Maintenance
- **chore**: Update provider documentation and add installation instructions for new providers (b3d8a21)

## [2025.10.05] - 2025-10-05

### ✨ Added
- **feat**: Initial release with core Webscout functionality (1a2b3c4) — Added web scraping, AI provider integration, and base CLI tooling.

### 🔧 Maintenance
- **chore**: Set up project structure, initial docs, and example workflows (1a2b3c4)

---

For more details, see the [documentation](docs/) or [GitHub repository](https://github.com/pyscout/Webscout).
