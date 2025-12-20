# LitPrinter: Advanced Terminal Output & Debugging Library
> Last updated: 2025-12-20
> Maintained by [OEvortex](https://github.com/OEvortex/litprinter)

**🔥 The Most Sophisticated Terminal Output & Debugging Library for Python**

**🎨 Rich Formatting • IceCream Debugging • Beautiful Panels • Syntax Highlighting • Enhanced Tracebacks**

## 📋 Overview

LitPrinter is a comprehensive terminal output library that combines the power of IceCream-style debugging with Rich-style formatting and UI components. It provides a sophisticated set of tools for creating beautiful, informative, and highly readable terminal applications and debug logs.

<details open>
<summary><b>🌟 Key Features</b></summary>

- **🍦 IceCream-Compatible Debugging**: Powerful `ic()` function for effortless variable inspection.
- **🖥️ Rich Console**: Advanced `Console` class with markup support, logging, and JSON highlighting.
- **🖼️ Beautiful Panels**: Professional bordered content areas with multiple styles, shadows, and alignment.
- **💥 Enhanced Tracebacks**: Syntax-highlighted, informative tracebacks with local variable inspection.
- **🎨 Sophisticated Styling**: Support for multiple themes (TokyoNight, Cyberpunk, Dracula, etc.) and custom styles.
- **📊 Layout Management**: `PanelGroup` for vertical, horizontal, and grid-based layouts.
- **🛠️ Highly Customizable**: Configure prefixes, output functions, and register custom formatters.

</details>

## 📑 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [IceCream Debugging (`ic`)](#-icecream-debugging-ic)
- [Rich Console (`Console`)](#-rich-console-console)
- [Panels & Layouts (`Panel`)](#-panels--layouts-panel)
- [Traceback Enhancement](#-traceback-enhancement)
- [Themes & Styles](#-themes--styles)
- [API Reference](#-api-reference)
- [License](#-license)

## 📦 Installation

Install LitPrinter using pip:

```bash
pip install litprinter
```

## 🚀 Quick Start

```python
from litprinter import ic, Console, Panel, TokyoNight

# 1. IceCream-style debugging
x = {"a": 1, "b": [1, 2, 3]}
ic(x)  # Output: ic| x: {'a': 1, 'b': [1, 2, 3]}

# 2. Rich-style console output
console = Console()
console.print("[bold cyan]Welcome to [magenta]LitPrinter[/magenta]![/bold cyan]")
console.rule("Section Header")

# 3. Beautiful Panels
print(Panel("This is a panel", title="Info", border_style="rounded"))
```

---

## 🍦 IceCream Debugging (`ic`)

LitPrinter provides a drop-in replacement for the popular `icecream` library with added formatting capabilities.

### Basic Usage
```python
from litprinter import ic

def add(a, b):
    return a + b

ic(add(10, 20))
# Output: ic| add(10, 20): 30
```

### Configuration
You can customize the behavior of `ic` globally:
```python
from litprinter import ic

ic.configureOutput(
    prefix="DEBUG| ",
    includeContext=True,  # Shows file, line, and function
    contextAbsPath=False  # Use relative paths
)

ic.disable() # Disable output
ic.enable()  # Enable output
```

### Aliases
```python
from litprinter import lit, litprint, LIT
# All are aliases for ic
```

---

## 🖥️ Rich Console (`Console`)

The `Console` class provides a high-level API for styled terminal output.

### Markup Support
Use Rich-style markup for easy styling:
```python
from litprinter import Console
console = Console()

console.print("[red]Red text[/red], [bold green]Bold Green[/bold green], [on_blue]Blue Background[/on_blue]")
console.print("Hex colors: [#ff5555]Custom Red[/#ff5555]")
```

### Logging
`console.log()` adds timestamps and the calling location:
```python
console.log("Processing started", log_locals=True)
```

### JSON Highlighting
```python
data = {"name": "LitPrinter", "version": "0.3.3", "active": True}
console.print_json(data)
```

### Other Console Methods
- `console.rule("Title")`: Draws a horizontal line.
- `console.status("Working...")`: Displays a status message with a spinner.
- `console.input("[bold yellow]Enter name: [/bold yellow]")`: Styled input.
- `console.clear()`: Clears the terminal.
- `console.capture()`: Context manager to capture output.

---

## 🖼️ Panels & Layouts (`Panel`)

Panels allow you to wrap content in beautiful borders.

### Basic Panel
```python
from litprinter import Panel

p = Panel(
    "Content goes here",
    title="Main Title",
    subtitle="v1.0",
    border_style="double",
    border_color="cyan"
)
print(p)
```

### Panel Features
- **Border Styles**: `rounded`, `double`, `thick`, `single`, `ascii`, `dashed`, `dotted`, `heavy`.
- **Alignment**: `align="center"`, `vertical_align="middle"`.
- **Padding & Margin**: Control spacing around and inside the panel.
- **Shadows**: `shadow=Shadow(enabled=True, color="gray")`.
- **Fitted Panels**: `Panel.fit("Content")` creates a panel that doesn't expand to full width.

### Layouts with `PanelGroup`
Stack panels vertically or horizontally:
```python
from litprinter import Panel, PanelGroup

group = PanelGroup(
    Panel("Left Panel", width=20),
    Panel("Right Panel", width=20),
    layout="horizontal",
    spacing=2
)
print(group.render())
```

---

## 💥 Traceback Enhancement

Replace standard Python tracebacks with beautiful, syntax-highlighted versions.

### Global Installation
```python
from litprinter.traceback import install

install(show_locals=True, theme="tokyonight")
```

### Manual Usage
```python
from litprinter.traceback import PrettyTraceback

try:
    1 / 0
except Exception as e:
    PrettyTraceback.from_exception(*sys.exc_info()).print()
```

---

## 🎨 Themes & Styles

LitPrinter comes with many built-in themes for both the console and tracebacks.

### Built-in Themes
- `TokyoNight` (Default)
- `Cyberpunk`
- `Dracula`
- `Monokai`
- `SolarizedDark`
- `Nord`
- `Jarvis`
- `Neon`

### Using Styles
```python
from litprinter import TokyoNight, set_style

set_style(TokyoNight)
```

---

## 📚 API Reference

### Core Functions
- `ic(*args)`: Debug print arguments.
- `cprint(text)`: Print with markup support.
- `install()`: Install `ic` to builtins.

### Classes
- `Console()`: Main output class.
- `Panel(content, **kwargs)`: Bordered container.
- `PanelGroup(*panels, **kwargs)`: Layout manager.
- `PrettyTraceback(...)`: Enhanced traceback formatter.

---

## 📄 License

LitPrinter is released under the MIT License. See [LICENSE](https://github.com/OEvortex/litprinter/blob/main/LICENSE) for details.

---

<div align="center">
  <p>Made with ❤️ by OEvortex</p>
  <p>
    <a href="https://github.com/OEvortex/litprinter">GitHub</a> •
    <a href="https://pypi.org/project/litprinter/">PyPI</a>
  </p>
</div>
