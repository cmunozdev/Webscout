# Webscout CLI Reference
> Last updated: 2025-01-29  
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

All commands support `--timeout` (default `10` seconds) and most DuckDuckGo commands allow `--proxy` for network tunneling.

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
-r, --region        Region code (default: wt-wt)
-s, --safesearch    on / moderate / off (default: moderate)
-t, --timelimit     d / w / m / y (varies by command)
-m, --max-results   Integer cap (varies by command)
-p, --proxy         Optional proxy URL
--timeout           Request timeout in seconds (default: 10)
```

**Maps extras**: `--place`, `--street`, `--city`, `--county`, `--state`, `--country`, `--postalcode`, `--latitude`, `--longitude`, `--radius`.

**Images extras**: `--size`, `--color`, `--type-image`, `--layout`, `--license-image`.

**Videos extras**: `--resolution`, `--duration`, `--license-videos`.

## 🔍 Yep Command Group

| Command | Description | Options |
|---------|-------------|---------|
| `yep_text` | Yep text search | `-k`, `-r` (default `all`), `-s` (default `moderate`), `-m` |
| `yep_images` | Yep image search | Same as `yep_text` |
| `yep_suggestions` | Query suggestions | `-q` (query), `-r` (default `en-US`)

## 🔎 Bing Command Group

| Command | Description | Options |
|---------|-------------|---------|
| `bing_text` | Bing text search (supports duplicate suppression) | `-k`, `-r` (default `us`), `-s`, `-m`, `-u/--unique` |
| `bing_images` | Bing image search | `-k`, `-r`, `-s`, `-m` |
| `bing_news` | Bing news search | `-k`, `-r`, `-s`, `-m` |
| `bing_suggestions` | Bing suggestions | `-q`, `-r`

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

All Yahoo commands re-use the same flags as their DuckDuckGo counterparts (`-k`, `-r`, `-s`, `-m`, etc.).

## 🌦️ Weather Convenience Command

The DuckDuckGo `weather` command formats current conditions + 5-day forecast using `_print_weather()`. Yahoo has a similar shortcut (`yahoo_weather`). Both leverage the same CLI formatting so you can quickly compare outputs by swapping commands.

## 🛠️ Tips for Extending the CLI

1. **Add imports** for new providers at the top of `webscout/cli.py`.
2. **Decorate a function** with `@app.command()` and chain `@option()` definitions (matching parameter order).
3. **Keep printing consistent** with `_print_data` (table style) or create a formatter similar to `_print_weather` if you need structured output.
4. **Surface provider-specific options** as CLI flags (see image/video/map commands for examples of many optional arguments).
5. **Document the new command** here and in `docs/README.md` so it appears in the navigation hub.

## 🧪 Debugging CLI Calls

- Use `--timeout` and `--proxy` args to replicate user environments.
- Wrap logic in `try/except` but re-raise the exception (as the current commands do) to keep stack traces visible during local testing.
- When comparing CLI results to Python usage, import the same class from `webscout` or `webscout.search` to ensure parity.

## 🔗 Related Documentation

- [docs/search.md](search.md) – deeper dive into the search module and Python usage.
- [docs/architecture.md](architecture.md) – how the CLI slots into the broader architecture.
- [docs/client.md](client.md) – if you need programmatic control beyond the CLI.
