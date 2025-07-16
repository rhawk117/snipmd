# snipmd

A command-line tool that converts VSCode snippet files to beautifully formatted Markdown documentation.

## Features

- 🔍 **Auto-discovery**: Automatically finds VSCode snippets in your system
- 📝 **Markdown conversion**: Converts snippet JSON files to readable Markdown format
- 🎨 **Rich output**: Beautiful console output with syntax highlighting
- 📋 **List snippets**: View all available snippet files in your VSCode snippets directory
- 💾 **Export options**: Save to file or display in console
- 🌐 **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. Make sure you have Python 3.12+ installed.

```bash
# Clone the repository
git clone <repository-url>
cd snipmd

# Install dependencies
uv sync

# Run the tool
uv run python main.py --help
```

## Usage

### Basic Commands

```bash
# List all available snippet files
uv run python main.py --list

# Convert a snippet file and display in console
uv run python main.py --snippet python --print

# Convert and save to a file
uv run python main.py --snippet python --output python-snippets.md

# Specify a different language for code blocks
uv run python main.py --snippet shellscript --language bash --print
```

### Command Line Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `--snippet` | `-s` | Name of the snippet file to convert (without .json extension) |
| `--list` | `-ls` | List all available snippet files in your VSCode snippets directory |
| `--language` | `-l` | Language identifier for Markdown code blocks (defaults to snippet name) |
| `--output` | `-o` | Output file path (if not specified, use `--print` to display in console) |
| `--print` | | Print the Markdown output to console with rich formatting |

### Examples

```bash
# View available snippets
uv run python main.py --list

# Convert Python snippets and view in console
uv run python main.py --snippet python --print

# Convert shell snippets with bash syntax highlighting
uv run python main.py --snippet shellscript --language bash --output shell-snippets.md

# Convert TypeScript snippets and save to file
uv run python main.py --snippet typescript --output ts-snippets.md
```

## Output Format

The tool converts VSCode snippet JSON files into well-structured Markdown documents. Each snippet becomes a section with:

- **Snippet name** as a header
- **Prefix** (trigger text)
- **Description** (if available)
- **Code template** with proper syntax highlighting


## VSCode Snippets Location

The tool automatically detects your VSCode snippets directory based on your operating system:

- **Windows**: `%APPDATA%\Code\User\snippets`
- **macOS**: `~/Library/Application Support/Code/User/snippets`
- **Linux**: `~/.config/Code/User/snippets`

## Requirements

- Python 3.12+
- VSCode (for snippets directory)
- Dependencies listed in [pyproject.toml](pyproject.toml):
  - `rich>=14.0.0` (for beautiful console output)

## Error Handling

The tool provides helpful error messages for common issues:

- Missing snippet files
- Invalid JSON format
- Missing VSCode snippets directory
- File permission issues

## Example

For a complete example of the tool's output, see [example_output.md](example_output.md) which shows the converted Python snippets.