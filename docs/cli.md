# Webscout CLI Reference
> Last updated: 2025-12-20
> Source of truth: [`webscout/cli.py`](../webscout/cli.py)

The Webscout CLI wraps the same search providers that are exposed through the Python API and `webscout.__init__`. Commands are registered with the `swiftcli` framework and share a consistent option style (`-k` for keywords, `-r` for region, etc.). This document captures every command, its parameters, defaults, and the underlying provider call.

## 🧭 Getting Started

```bash
# List commands and global help
webscout --help

# Show CLI version
webscout version

# Run without installation (using uv)
uv run webscout --help
```

All commands support `--timeout` (default `10` seconds) and DuckDuckGo commands allow `--proxy` for network tunneling.

## 🦆 DuckDuckGo Command Group (Default Backend)

| Command | Description | Underlying Call |
|---------|-------------|-----------------|
| `text` | General search with region/safesearch/timelimit filters | `DuckDuckGoSearch.text()` |
| `answers` | Instant answers (calculator, facts, conversions) | `DuckDuckGoSearch.answers()` |
| `images` | Image search with advanced filters (size, color, type, layout, license) | `DuckDuckGoSearch.images()` |
| `videos` | Video search with resolution, duration, license filters | `DuckDuckGoSearch.videos()` |
| `news` | News articles | `DuckDuckGoSearch.news()` |
| `maps` | POI/geo search with address or lat/lon inputs | `DuckDuckGoSearch.maps()` |
| `translate` | Text translation | `DuckDuckGoSearch.translate()` |
| `suggestions` | Query suggestions/autocomplete | `DuckDuckGoSearch.suggestions()` |
| `weather` | Rich weather report printed via `_print_weather` | `DuckDuckGoSearch.weather()` |

### Common Options

```text
-k, --keywords      (required) Search query
-r, --region        Region code (default varies by command)
-s, --safesearch    on / moderate / off (default: moderate)
-t, --timelimit     d / w / m / y (varies by command)
-m, --max-results   Integer cap (varies by command)
-p, --proxy         Optional proxy URL
--timeout           Request timeout in seconds (default: 10)
```

**Maps extras**: `--place`, `--street`, `--city`, `--county`, `--state`, `--country`, `--postalcode`, `--latitude`, `--longitude`, `--radius`.

**Images extras**: `--size`, `--color`, `--type-image`, `--layout`, `--license-image`.

**Videos extras**: `--resolution`, `--duration`, `--license-videos`.

**Translate extras**: `--from` (from language), `--to` (to language).

**Weather extras**: `--language` (language code, default: 'en').

## 🔍 Yep Command Group

| Command | Description | Options |
|---------|-------------|---------|
| `yep_text` | Yep text search | `-k`, `-r` (default `all`), `-s` (default `moderate`), `-m` (default: 10) |
| `yep_images` | Yep image search | Same as `yep_text` |
| `yep_suggestions` | Query suggestions | `-q` (query), `-r` (default `en-US`) |

## 🔎 Bing Command Group

| Command | Description | Options |
|---------|-------------|---------|
| `bing_text` | Bing text search (supports duplicate suppression) | `-k`, `-r` (default `us`), `-s`, `-m`, `-u/--unique` (default: true) |
| `bing_images` | Bing image search | `-k`, `-r`, `-s`, `-m` (default: 10) |
| `bing_news` | Bing news search | `-k`, `-r`, `-s`, `-m` (default: 10) |
| `bing_suggestions` | Bing suggestions | `-q` (query), `-r` (default `en-US`) |

## 📨 Yahoo Command Group

Mirrors DuckDuckGo features but routed through `YahooSearch`.

| Command | Description |
|---------|-------------|
| `yahoo_text` | Text search |
| `yahoo_images` | Image search |
| `yahoo_videos` | Video search |
| `yahoo_news` | News search |
| `yahoo_answers` | Q&A style answers |
| `yahoo_maps` | Maps/geocode search (same arguments as DuckDuckGo version) |
| `yahoo_translate` | Translation |
| `yahoo_suggestions` | Suggestions/autocomplete |
| `yahoo_weather` | Weather (prints via `_print_weather`) |

**Yahoo-specific options**:
- All commands support region parameter (default: `us`)
- `yahoo_text`, `yahoo_images`, `yahoo_videos`, `yahoo_news`: `-k`, `-r`, `-s`, `-m`
- `yahoo_translate`: `-k`, `--from`, `--to`
- `yahoo_maps`: same as DuckDuckGo maps
- `yahoo_weather`: `-l` (location)
- `yahoo_suggestions`: `-q` (query), `-r` (default: `us`)

## 🌦️ Weather Convenience Commands

The DuckDuckGo `weather` command formats current conditions + 5-day forecast using `_print_weather()`. Yahoo has a similar shortcut (`yahoo_weather`). Both leverage the same CLI formatting so you can quickly compare outputs by swapping commands.

## 🛠️ Tips for Using the CLI

1. **Search backends**: The CLI uses various search providers - DuckDuckGo (default), Bing, Yep, and Yahoo. Each has its own strengths and coverage.
2. **Common patterns**: Most search commands follow the pattern `-k` for keywords, `-r` for region, `-s` for safesearch, and `-m` for max results.
3. **Proxy and timeout**: For DuckDuckGo commands, you can use `--proxy` and `--timeout` to handle network issues.
4. **Provider-specific features**: Bing has unique duplicate suppression with `-u/--unique`, while different providers may have different regional coverage.

## 🧪 Command Examples

```bash
# Basic text search
webscout text -k "python programming"

# Image search with filters
webscout images -k "mountain landscape" --size large --type-image photo

# News search with time limit
webscout news -k "AI breakthrough" -t w  # last week

# Weather information
webscout weather -l "New York"

# Yahoo search alternative
webscout yahoo_text -k "machine learning" -r us

# Bing with duplicate suppression off
webscout bing_text -k "climate change" -u false
```

## 🔗 Related Documentation

- [docs/search.md](search.md) – deeper dive into the search module and Python usage.
- [docs/architecture.md](architecture.md) – how the CLI slots into the broader architecture.
- [docs/client.md](client.md) – if you need programmatic control beyond the CLI.
