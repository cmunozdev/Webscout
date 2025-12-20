# Webscout CLI Reference
> Last updated: 2025-12-20
> Source of truth: [`webscout/cli.py`](../webscout/cli.py)

The Webscout CLI provides a unified interface for multiple search engines. All commands now support an `--engine` (or `-e`) option to switch between providers, with DuckDuckGo (`ddg`) as the default.

## 🧭 Getting Started

```bash
# List all available commands
webscout --help

# Show CLI version
webscout version

# Run a simple search
webscout text -k "python programming"
```

The CLI uses **Rich** for beautiful, formatted table outputs and informative panels.

## 🔍 Core Commands

| Command | Description | Supported Engines |
|---------|-------------|-------------------|
| `text` | General web search | `ddg`, `bing`, `yahoo`, `brave`, `mojeek`, `yandex`, `wikipedia`, `yep` |
| `images` | Image search | `ddg`, `bing`, `yahoo`, `yep` |
| `videos` | Video search | `ddg`, `yahoo` |
| `news` | News search | `ddg`, `bing`, `yahoo` |
| `weather` | Weather information | `ddg`, `yahoo` |
| `answers` | Instant answers | `ddg`, `yahoo` |
| `suggestions`| Query autocomplete | `ddg`, `bing`, `yahoo`, `yep` |
| `translate` | Text translation | `ddg`, `yahoo` |
| `maps` | POI / Location search | `ddg`, `yahoo` |
| `search` | Shortcut for `text` | Use as a general unified command |

### Common Options

```text
-k, --keywords      (required) Search query or keywords
-e, --engine        Search engine to use (default: ddg)
-m, --max-results   Maximum number of results to display (default: 10)
-r, --region        Region code (e.g., us, uk, wt-wt)
-s, --safesearch    on / moderate / off (default: moderate)
-t, --timelimit     Time filter (d, w, m, y)
```

## 🌦️ Weather & Info

The `weather` command provides a current conditions panel and a 5-day forecast.

```bash
webscout weather -l "London" -e yahoo
```

## 🧪 Usage Examples

### 1. Multi-Engine Search
```bash
# Default (DuckDuckGo)
webscout text -k "fastapi tutorial"

# Using Brave Search
webscout text -k "fastapi tutorial" -e brave

# Using Wikipedia
webscout text -k "Quantum Physics" -e wikipedia
```

### 2. Media Search
```bash
# Find images on Bing
webscout images -k "cyberpunk art" -e bing

# Find news on Yahoo
webscout news -k "space exploration" -e yahoo
```

### 3. Utility Commands
```bash
# Translate text via Yahoo
webscout translate -k "Hola mundo" --to en -e yahoo

# Get suggestions from Yep
webscout suggestions -q "artificial i" -e yep
```

## 🛠️ Advanced Options

Certain commands have specific extras:
- **Maps**: `--place` and `--radius` are supported for refinement.
- **Translate**: `--from` (optional) and `--to` (default: `en`).

## 🔗 Related Documentation

- [docs/search.md](search.md) – Technical documentation for the Python Search API.
- [docs/architecture.md](architecture.md) – How the search module is structured.
- [docs/client.md](client.md) – Using the unified `Webscout` client.
