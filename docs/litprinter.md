# LitPrinter: Advanced Debug Printing Library
> Last updated: 2025-12-01
> Maintained by [OEvortex](https://github.com/OEvortex/litprinter)

**🔥 The Most Sophisticated Debug Printing Library for Python with Rich Formatting, Syntax Highlighting, and Beautiful Tracebacks**

**🎨 Beautiful Output • Context-Aware • Syntax Highlighted • Traceback Enhanced**

## 📋 Overview

LitPrinter is a sophisticated debugging and logging library designed for Python developers who want elegant, informative terminal output. Built with developer experience in mind, LitPrinter provides beautiful syntax highlighting, context-aware output, smart formatting, and powerful traceback handling. It transforms mundane debugging from tedious to magnificent with color themes, variable inspection, and rich formatting capabilities.

<details open>
<summary><b>🌟 Why LitPrinter is the Ultimate Debugging Choice</b></summary>

- **🎨 Rich Syntax Highlighting**: Beautiful, color-coded output for all data types using Pygments
- **🔍 Context-Aware Output**: Automatically shows file path, line number, and function name
- **📊 Smart Formatting**: Intelligent pretty-printing for dictionaries, lists, and complex objects
- **💥 Enhanced Tracebacks**: Replace Python's default tracebacks with beautiful, informative displays
- **🧵 Inline Usage**: Use as both a debugging tool and value returner without disrupting code flow
- **🎯 Variable Inspection**: Automatically displays variable names alongside their values
- **🛠️ Highly Customizable**: Register custom formatters and configure output styles
- **⚙️ Performance Optimized**: Built-in style caching system for improved performance
- **🌐 Cross-Platform**: Full support for Windows, macOS, and Linux
- **📝 Logging Support**: Integrated logging with level support (debug, info, warning, error)
- **🎪 Theme Support**: Multiple built-in color themes (JARVIS, RICH, MODERN, NEON, CYBERPUNK, DRACULA, MONOKAI)

</details>

## 📑 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Features](#-features)
- [Debug Printing](#-debug-printing)
- [Logging](#-logging)
- [Traceback Enhancement](#-traceback-enhancement)
- [Advanced Usage](#-advanced-usage)
- [API Reference](#-api-reference)
- [Dependencies](#-dependencies)
- [Supported Python Versions](#-supported-python-versions)
- [Contributing](#-contributing)
- [License](#-license)

## 📦 Installation

Install LitPrinter using pip:

```bash
pip install litprinter
```

Or install the latest version from GitHub:

```bash
pip install git+https://github.com/OEvortex/litprinter.git
```

## 🚀 Quick Start

### Basic Debug Printing

```python
from litprinter import lit

# Print variables with their names and values
x, y = 10, 20
lit(x, y)
# Output: LIT| [script.py:4] in <module>() >>> x: 10, y: 20
```

### Using Aliases

```python
from litprinter import litprint, ic

# All three are equivalent - choose your preference
lit("Debug message")        # Primary function
litprint("Debug message")   # Alias
ic("Debug message")         # Icecream-style alias
```

### Inline Usage

```python
from litprinter import lit

# Use inline - both prints and returns the value
def get_user(user_id):
    user = database.find(user_id)
    return lit(user)  # Prints the value AND returns it
```

### Context-Aware Output

```python
from litprinter import lit

def calculate_total(a, b):
    lit(a, b)  
    # Output: LIT| [script.py:3] in calculate_total() >>> a: 10, b: 20
    return a + b
```

## ✨ Features

### 🎨 Rich Syntax Highlighting

LitPrinter uses Pygments to provide beautiful syntax highlighting for all data types:

```python
from litprinter import lit

my_complex_object = {
    "name": "LitPrinter",
    "version": 1.0,
    "features": ["debugging", "formatting", "tracebacks"],
    "active": True,
    "nested": {
        "deep": [1, 2, 3],
        "color": "#ff00ff"
    }
}

# Output will be color-coded with proper formatting
lit(my_complex_object)
```

**Supported Syntax Highlighting:**
- Dictionary and JSON-like structures
- Lists and tuples
- Strings with escape sequences
- Numbers and booleans
- Custom objects and class instances
- Code and function definitions

### 📊 Smart Object Formatting

LitPrinter automatically detects and formats different data types intelligently:

```python
# Complex nested structures
data = {
    "users": ["alice", "bob", "charlie"],
    "active": True,
    "settings": {
        "theme": "dark",
        "notifications": True,
        "limits": {"requests": 100, "timeout": 30}
    }
}
lit(data)  # Formatted with proper indentation and syntax highlighting

# Lists and tuples
lit([1, 2, 3, 4, 5])
lit(("a", "b", "c"))

# Sets and frozensets
lit({1, 2, 3})
lit(frozenset([4, 5, 6]))

# Custom classes
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

user = User("John", 30)
lit(user)  # Shows: User(name='John', age=30)
```

### 🔍 Context-Aware Output

LitPrinter automatically captures and displays execution context:

```python
from litprinter import lit

def process_data(items):
    # Shows file path, line number, and function name
    lit(items)
    # Output: LIT| [data.py:3] in process_data() >>> items: [1, 2, 3, 4, 5]
    
class DataProcessor:
    def handle(self, data):
        # Also works in class methods
        lit(data)
        # Output: LIT| [processor.py:8] in DataProcessor.handle() >>> data: {...}
```

**Context Information Includes:**
- File path (relative or absolute)
- Line number
- Function or method name
- Module context

### 📝 Logging Support

LitPrinter includes integrated logging with multiple levels:

```python
from litprinter import log

# Different log levels
log("System starting...", level="info")
log("Debug information: processing started", level="debug")
log("Warning: disk space low", level="warning")
log("Critical error occurred", level="error")

# Timestamps and file logging
log("Important event", log_timestamp=True, log_file="app.log")
```

**Log Levels:**
- `debug`: Detailed information for debugging
- `info`: Informational messages
- `warning`: Warning messages for potentially problematic situations
- `error`: Error messages for serious problems

### 💥 Enhanced Traceback Handling

Replace Python's default traceback with beautiful, informative displays:

```python
from litprinter.traceback import install

# Basic installation with defaults
install()

# Now any exceptions will display with beautiful formatting
def example():
    x = {"test": [1, 2, 3]}
    y = x["not_found"]  # KeyError with beautiful traceback
```

#### Advanced Traceback Configuration

```python
from litprinter.traceback import install

# Customize traceback appearance
install(
    theme="cyberpunk",        # Use any theme: JARVIS, RICH, MODERN, NEON, CYBERPUNK, DRACULA, MONOKAI
    show_locals=True,         # Show local variables in each frame
    extra_lines=3,            # Show extra context lines around error
    locals_max_length=150,    # Limit local variable display length
    locals_max_depth=3,       # How deep to format nested structures
    locals_hide_dunder=True,  # Hide __dunder__ variables
    width=120                 # Terminal width for formatting
)
```

#### One-Time Traceback Handling

```python
from litprinter.traceback import PrettyTraceback

try:
    risky_operation()
except Exception as e:
    tb = PrettyTraceback(
        type(e), e, e.__traceback__,
        theme="neon",
        show_locals=True
    )
    tb.print()
```

**Available Themes:**
- `JARVIS`: Iron Man's JARVIS-inspired theme
- `RICH`: Rich library's default theme
- `MODERN`: Modern, clean design
- `NEON`: Bright neon colors
- `CYBERPUNK`: Cyberpunk aesthetic
- `DRACULA`: Dracula dark theme
- `MONOKAI`: Monokai color scheme

### ⚙️ Highly Customizable

Register custom formatters for your types and customize output format:

```python
from litprinter import lit, argumentToString

# Register custom formatter for your class
class MyCustomClass:
    def __init__(self, id, name):
        self.id = id
        self.name = name

@argumentToString.register(MyCustomClass)
def format_my_class(obj):
    return f"MyClass(id={obj.id}, name='{obj.name}')"

# Now custom class instances will use your formatter
obj = MyCustomClass(1, "Test")
lit(obj)  # Output: MyClass(id=1, name='Test')
```

#### Customize Output Format

```python
from litprinter import lit

lit(
    my_object,
    prefix="DEBUG >>> ",        # Custom prefix
    includeContext=True,        # Show file/line/function
    contextAbsPath=True,        # Use absolute paths
    disable_colors=False        # Enable/disable colors
)
```

### 🛠️ Install as Builtins

Make LitPrinter available globally without importing:

```python
from litprinter.builtins import install, uninstall

# Install as builtins
install()  # Now 'litprint' and 'ic' are available globally

# Use anywhere in your code
litprint("Available globally!")
ic("Also available!")

# Uninstall when done
uninstall()
```

### 💻 Integration with VS Code

LitPrinter creates clickable links in supported terminals and editors:

```python
from litprinter import lit

# With absolute paths, create clickable links to source
lit(data, contextAbsPath=True)
# Click the file path in VS Code to jump to that line
```

**For Tracebacks:**
```python
from litprinter.traceback import install

install(show_locals=True)

# When exceptions occur, file paths in traceback are clickable
# Click to jump directly to the error location in VS Code
```

### ⚡ Performance and System Utilities

Manage performance and system capabilities:

```python
from litprinter.core import clearStyleCache, getStyleCacheInfo, isTerminalCapable

# Check cache status
cache_info = getStyleCacheInfo()
print(f"Cache size: {cache_info['cache_size']}")
print(f"Cached styles: {cache_info['cached_styles']}")

# Clear cache for memory management
clearStyleCache()

# Check terminal capabilities (respects NO_COLOR)
if isTerminalCapable():
    print("Terminal supports colors")
else:
    print("Terminal does not support colors")
```

### 🌐 Cross-Platform Support

LitPrinter automatically handles platform differences:

```python
import os

# Windows terminal capabilities are automatically detected
# Colorama is initialized on Windows
# NO_COLOR environment variable is respected
os.environ['NO_COLOR'] = '1'  # Disable colors globally
lit("This will be plain text")  # No colors applied

# Proper path normalization across platforms
lit(file_path, contextAbsPath=True)  # Works on Windows, macOS, Linux
```

## 🔬 Advanced Usage

### Multiple Variable Inspection

```python
from litprinter import lit

# Inspect multiple variables at once
name = "Alice"
age = 30
email = "alice@example.com"

lit(name, age, email)
# Output: LIT| [app.py:8] in main() >>> name: 'Alice', age: 30, email: 'alice@example.com'
```

### Integration with Error Handling

```python
from litprinter import lit

try:
    result = risky_operation()
except Exception as e:
    lit(e)  # Pretty-prints the exception
    raise
```

### Log to File and Console

```python
from litprinter import lit

# Log to both console and file
lit("System initialization", log_file="app.log", log_timestamp=True)
lit("Processing batch", log_file="app.log", log_timestamp=True)
```

### Working with Different Data Types

```python
from litprinter import lit

# Strings
lit("Hello, World!")

# Numbers
lit(42, 3.14, -10)

# Collections
lit([1, 2, 3], {"key": "value"}, {1, 2, 3})

# Booleans
lit(True, False)

# None
lit(None)

# Functions and classes
def my_function():
    pass

lit(my_function)

# Complex nested structures
lit({
    "data": [1, 2, 3],
    "info": {"nested": True},
    "active": False
})
```

### Performance Management

```python
from litprinter.core import clearStyleCache, getStyleCacheInfo

# Monitor cache performance
for item in large_list:
    lit(item)

# Check cache statistics
cache_info = getStyleCacheInfo()
if cache_info['cache_size'] > 1000:  # If cache grows too large
    clearStyleCache()  # Clear for memory management
```

## 📚 API Reference

### Core Functions

| Function | Description | Return |
|----------|-------------|--------|
| `lit(*args, **kwargs)` | Primary debug printing function | Returns first argument |
| `litprint(*args, **kwargs)` | Alias for `lit` | Returns first argument |
| `ic(*args, **kwargs)` | Icecream-style alias | Returns first argument |
| `log(*args, level="debug", **kwargs)` | Logging with level support | None |

### Traceback Module

| Function | Description |
|----------|-------------|
| `traceback.install(**kwargs)` | Replace default Python traceback with pretty version |
| `traceback.uninstall()` | Restore original Python traceback handler |
| `PrettyTraceback(exc_type, exc_value, tb, **kwargs)` | Create traceback formatter instance |

### Builtin Installation

| Function | Description |
|----------|-------------|
| `builtins.install(name='litprint', ic='ic')` | Install functions as builtins |
| `builtins.uninstall(name='litprint', ic='ic')` | Remove from builtins |

### Core Utilities

| Function | Description |
|----------|-------------|
| `core.clearStyleCache()` | Clear the style formatter cache |
| `core.getStyleCacheInfo()` | Get cache statistics |
| `core.isTerminalCapable()` | Check terminal color support |

### Key Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prefix` | str | "LIT\|" | Custom prefix for output lines |
| `color_style` | str/dict | Auto | Color theme or custom colors |
| `includeContext` | bool | True | Show file/line/function context |
| `contextAbsPath` | bool | False | Use absolute paths in context |
| `disable_colors` | bool | False | Turn off syntax highlighting |
| `log_file` | str | None | File to write output to |
| `log_timestamp` | bool | False | Include timestamps in output |
| `level` | str | "debug" | Log level (debug, info, warning, error) |

### Custom Formatter Registration

```python
from litprinter import argumentToString

@argumentToString.register(YourClass)
def format_your_class(obj):
    return f"YourClass(...)"
```

## 🔧 Dependencies

- `Pygments`: Syntax highlighting library (required)
- `colorama`: Cross-platform terminal color support (Windows)
- Standard library modules (used internally)

## 🌈 Supported Python Versions

- Python 3.6+
- Python 3.7, 3.8, 3.9, 3.10, 3.11, 3.12+

## 🆕 Recent Improvements

### Code Quality & Performance (v0.2.0)
- **90% Code Duplication Eliminated**: Consolidated implementations for better maintainability
- **Enhanced Cross-Platform Support**: Improved Windows terminal detection and colorama integration
- **Performance Optimizations**: Added style caching system for improved performance
- **Memory Management**: New cache control functions for production environments
- **Standards Compliance**: Full NO_COLOR environment variable support
- **Robust Error Handling**: Graceful fallbacks for invalid styles and edge cases
- **Import Fixes**: Resolved module import issues for better package compatibility

## 📚 Examples

### Example 1: Debugging Function Parameters

```python
from litprinter import lit

def process_user_data(user, options):
    lit(user, options)  # See both parameters with names
    
    name = user.get('name', 'Unknown')
    age = user.get('age', 0)
    
    lit(name, age)  # Inspect extracted values
    
    return {"processed": True}

# Usage
process_user_data(
    {"name": "John", "age": 30},
    {"verbose": True}
)
```

### Example 2: Beautiful Tracebacks in Production

```python
from litprinter.traceback import install

# Install at application startup
install(
    theme="dracula",
    show_locals=True,
    extra_lines=2
)

def calculate(x, y):
    result = x / y  # Potential ZeroDivisionError
    return result

# When error occurs, traceback displays beautifully with local variables
calculate(10, 0)
```

### Example 3: Logging with Timestamps

```python
from litprinter import log

log("Application started", level="info", log_timestamp=True, log_file="app.log")
log("Processing request #1234", level="debug", log_timestamp=True, log_file="app.log")
log("Database connection failed", level="error", log_timestamp=True, log_file="app.log")
```

### Example 4: Custom Formatter for Domain Objects

```python
from litprinter import lit, argumentToString

class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

@argumentToString.register(User)
def format_user(user):
    return f"User(id={user.id}, name='{user.name}', email='{user.email}')"

# Usage
users = [
    User(1, "Alice", "alice@example.com"),
    User(2, "Bob", "bob@example.com")
]
lit(users)  # Custom formatting applied
```

### Example 5: Global Installation as Builtins

```python
from litprinter.builtins import install

# Once installed, functions available everywhere
install()

def main():
    data = {"status": "running", "progress": 45}
    litprint(data)  # No import needed!
    
    ic("Process complete")  # Works globally!

main()
```

## 🤝 Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See the [CONTRIBUTING.md](https://github.com/OEvortex/litprinter/blob/main/CONTRIBUTING.md) file for more details.

## 📄 License

LitPrinter is released under the MIT License. See [LICENSE](https://github.com/OEvortex/litprinter/blob/main/LICENSE) for details.

---

<div align="center">
  <p>Made with ❤️ by OEvortex</p>
  <p>
    <a href="https://github.com/OEvortex/litprinter">GitHub</a> •
    <a href="https://pypi.org/project/litprinter/">PyPI</a> •
    <a href="https://github.com/OEvortex/litprinter/issues">Report Bug</a> •
    <a href="https://github.com/OEvortex/litprinter/issues">Request Feature</a>
  </p>
</div>
