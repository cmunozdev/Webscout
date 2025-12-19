# Webscout Architecture Overview
> Last updated: 2025-01-29  
> Relates to: `webscout/cli.py`, `webscout/client.py`, `webscout/server/`, `webscout/search/`, `webscout/Provider/`, `webscout/Extra/`

Webscout bundles multiple user-facing entry points (CLI, Python client, and an OpenAI-compatible API server) on top of a shared set of engines, providers, and utilities. This document maps how these layers interact so you can reason about changes confidently.

## 🧱 Layered View

```mermaid
flowchart TD
    subgraph EntryPoints
        CLI[CLI (webscout/cli.py)]
        Client[Python Client (webscout/client.py)]
        Server[OpenAI-Compatible Server (webscout/server)]
    end

    subgraph Core
        Search[Search Engines (webscout/search)]
        Providers[Providers (webscout/Provider)]
        Extras[Extras & Toolkits (webscout/Extra)]
        Utilities[Utilities (sanitize.py, AIutel.py, etc.)]
        Models[Model Registry (webscout/models.py)]
    end

    CLI --> Search
    CLI --> Providers
    Client --> Providers
    Client --> Extras
    Client --> Models
    Server --> Providers
    Server --> Utilities
    Search --> Providers
    Extras --> Providers
```

- **Entry Points** convert user intent (commands/API calls) into provider requests.
- **Core Modules** encapsulate the heavy lifting: crawling websites, calling remote LLMs, handling audio/image generation, sanitizing streams, and enumerating models.

## 🔌 Entry Points

### Command Line Interface (`webscout/cli.py`)
- Built on `swiftcli` with separate command groups for DuckDuckGo, Yep, Bing, Yahoo, and weather utilities.
- Uses `_print_data` / `_print_weather` helpers to keep terminal output consistent.
- Relies on the same search/provider classes exported in `webscout/__init__.py`, so CLI behavior matches the Python API.

### Unified Python Client (`webscout/client.py`)
- Provides auto-failover chat and image APIs through `Client.chat.completions.create()` and `Client.images.generate()`.
- Dynamically discovers OpenAI-compatible providers (`webscout/Provider/OPENAI`) and TTI providers, caches instances, and performs fuzzy model resolution.
- Shares provider cache with the server, so runtime cost of imports stays low.

### OpenAI-Compatible Server (`webscout/server/`)
- FastAPI app that exposes `/v1/*` routes mirroring OpenAI's schema.
- Uses `providers.py` to map model names like `ProviderName/model-id` back to actual provider classes.
- Pulls configuration from `config.py` plus environment variables documented in `docs/openai-api-server.md` and `docs/DOCKER.md`.

## 🔍 Core Modules

### Search Stack (`webscout/search/`)
- Houses protocol-specific engines (See `webscout/search/engines/*`) plus shared HTTP client and result serializers.
- DuckDuckGo/Yep/Bing/Yahoo commands import from here, so adding new CLI options usually starts with an engine update.

### Providers (`webscout/Provider/`)
- Normal providers live alongside OpenAI-compatible wrappers (`webscout/Provider/OPENAI`).
- Specialty directories: `AISEARCH`, `TTI`, `TTS`, `STT`, `UNFINISHED`.
- The matrix in `Provider.md` maps every provider to its implementation file.

### Extras (`webscout/Extra/`)
- Optional toolkits packaged with Webscout (GGUF converter, weather clients, temp mail, YT toolkit, Git API helper, etc.).
- Exported through `webscout/Extra/__init__.py` so they become part of the public API when you `import webscout`.

### Utilities
- `webscout/sanitize.py` – SSE/stream sanitization for server + client streaming paths.
- `webscout/AIutel.py` – Decorators for retry/timing (documented in `docs/decorators.md`).
- `webscout/update_checker.py` – Optional PyPI update notifier executed in `webscout/__init__.py`.

### Models Registry (`webscout/models.py`)
- Enumerates LLM, TTS, and TTI models exposed by providers.
- Used by documentation examples (README, docs/models.md) and can power custom tooling (e.g., provider dashboards).

## 🔄 Typical Data Flows

1. **CLI ➜ Search Engine ➜ Provider**
   - `webscout images -k "python"` → `DuckDuckGoSearch.images()` (HTTP scraping) → results printed via `_print_data`.
2. **Client ➜ Provider Failover**
   - `Client().chat.completions.create(model="gpt-4o")` → resolves provider & model → tries preferred provider → falls back through fuzzily-matched providers if necessary.
3. **Server ➜ Provider ➜ sanitize_stream**
   - `/v1/chat/completions` request hits FastAPI → provider resolved → streaming responses run through `sanitize_stream()` before being sent to clients.
4. **Extras ➜ Providers**
   - GGUF converter uses huggingface + llama.cpp builders and is fully independent, but still exported to users alongside the main modules.

## 🧩 When Adding New Functionality

| Task | Touch Points |
|------|--------------|
| Add a CLI command | `webscout/cli.py` + corresponding engine/provider + update `docs/cli.md` |
| Add a provider | Implement in `webscout/Provider/` (and optionally `OPENAI/`), update `Provider.md`, consider `models.py` exposure |
| Add server capability | Update `webscout/server/*`, document in `docs/openai-api-server.md`, ensure CLI/Client can hit the new route if needed |
| Extend Extras | Implement under `webscout/Extra/`, export in `__init__.py`, add documentation entry under `docs/README.md` |
| Add new registry info | Update `webscout/models.py` or referencing docs (`docs/models.md`) |

## 🧪 Testing & Debugging Hooks

- CLI commands can be run locally with `uv run webscout ...` to ensure option parsing remains correct.
- Client failover prints last provider when `print_provider_info=True` – useful when debugging provider availability.
- The server exposes `/health` (see Docker docs) to monitor deployments.
- `sanitize_stream` and decorators have dedicated docs you can reference when debugging streaming issues or retries.

## 📚 Related Documents

- [docs/cli.md](cli.md) – exhaustive CLI reference.
- [docs/client.md](client.md) – deep dive into the unified client.
- [docs/models.md](models.md) – using the model registry helpers.
- [docs/openai-api-server.md](openai-api-server.md) – server configuration & endpoints.
- [Provider.md](../Provider.md) – provider matrix you can cross-reference while navigating the codebase.
