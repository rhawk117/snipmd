import argparse
import functools
import json
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.markdown import Markdown

console = Console()


@functools.lru_cache(maxsize=1)
def get_snippets_path() -> Path:
    if platform.system() == "Linux":
        return Path.home().joinpath(".config", "Code", "User", "snippets")
    elif platform.system() == "Darwin":  # macOS
        return Path.home().joinpath(
            "Library", "Application Support", "Code", "User", "snippets"
        )
    elif platform.system() == "Windows":
        return Path.home().joinpath(
            "AppData", "Roaming", "Code", "User", "snippets"
        )
    else:
        raise RuntimeError(
            "Unsupported operating system for VSCode snippets path."
        )


class SnippetError(Exception):
    pass


@dataclass
class VSCodeSnippet:
    name: str
    prefix: str
    body: list[str]
    description: str | None = None

    def to_markdown(self, language: str = "") -> str:
        header = f"### {self.name}\n **Prefix**: {self.prefix}\n"

        description_section = "n/a"
        if self.description:
            description_section = f"\n\n**Description**: {self.description}"

        body_text = "\n".join(self.body)
        code_block = f"\n\n#### Template\n\n```{language}\n{body_text}\n```"

        return f"{header}{description_section}{code_block}"

    def __str__(self) -> str:
        return self.to_markdown()

    @classmethod
    def create(cls, name: str, snippet_data: dict[str, Any]) -> "VSCodeSnippet":
        if not isinstance(snippet_data, dict):
            raise SnippetError(
                f"Invalid snippet data for '{name}': expected object"
            )

        prefix = snippet_data.get("prefix", "")
        body = snippet_data.get("body", [])
        description = snippet_data.get("description")

        if isinstance(body, str):
            body = [body]
        elif not isinstance(body, list):
            raise SnippetError(
                f"Invalid body for snippet '{name}': expected string or array"
            )

        return VSCodeSnippet(
            name=name,
            prefix=prefix,
            body=body,
            description=description,
        )


class SnippetProcessor:
    def __init__(self, *, snippet_name: str, snippet_lang: str | None) -> None:
        """
        Initialize SnippetProcessor with snippet name and language.

        Args:
            snippet_name: Name of the snippet
            snippet_lang: Language identifier for the snippets
        """
        self.snippet_name: str = snippet_name
        self.snippet_lang: str | None = snippet_lang

    def parse_snippet_json(
        self, json_data: dict[str, Any]
    ) -> list[VSCodeSnippet]:
        """
        Parse JSON data into VSCodeSnippet objects.

        Args:
            json_data: Raw JSON data from snippet file

        Returns:
            list of VSCodeSnippet objects

        Raises:
            SnippetError: If JSON structure is invalid
        """
        snippets: list[VSCodeSnippet] = []

        if not isinstance(json_data, dict):
            raise SnippetError(
                "Invalid JSON structure: expected object at root level"
            )

        for name, snippet_data in json_data.items():
            try:
                snip = VSCodeSnippet.create(name, snippet_data)
                snippets.append(snip)
            except KeyError as e:
                raise SnippetError(
                    f"Missing required field in snippet '{name}': {e}"
                )

        return snippets

    def load_snippet_file(self) -> list[VSCodeSnippet]:
        """
        Load snippets from a JSON file.

        Args:
            file_path: Path to the snippet file

        Returns:
            list of VSCodeSnippet objects

        Raises:
            SnippetError: If file cannot be read or parsed
        """
        try:
            path = get_snippets_path().joinpath(
                f"{self.snippet_name.lower()}.json"
            )

            if not path.exists():
                raise SnippetError(f"Snippet file not found: {path}")

            if not path.suffix.lower() == ".json":
                raise SnippetError(f"File must be a JSON file: {path}")

            json_data = json.loads(path.read_text(encoding="utf-8"))

            return self.parse_snippet_json(json_data)
        except Exception as e:
            raise SnippetError(f"Error reading snippet file '{path}': {e}")

    def write_markdown(self, snippets: list[VSCodeSnippet]) -> str:
        """
        Generate a complete Markdown document from snippets.

        Args:
            snippets: list of VSCodeSnippet objects
            language: Language for code blocks

        Returns:
            Complete Markdown document as string
        """
        if not snippets:
            return "# No Snippets Found\n\nThe provided input contains no valid snippets."

        markdown_sections = []

        for snippet in snippets:
            markdown_sections.append(
                snippet.to_markdown(
                    language=self.snippet_lang or self.snippet_name
                )
            )

        return "\n\n---\n".join(markdown_sections)


def ls_snippets() -> list[str]:
    """
    List available snippets in the snippets directory.

    Returns:
        List of snippet file names without extension
    """
    snippets_path = get_snippets_path()
    if not snippets_path.exists():
        raise SnippetError(f"Snippets path does not exist: {snippets_path}")

    return [f.stem for f in snippets_path.glob("*.json") if f.is_file()]


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert VSCode snippet files to Markdown format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -f snippets.json -l python
  %(prog)s -s '{"test": {"prefix": "t", "body": ["test"]}}' -l javascript
  %(prog)s -f my-snippets.json --snippet-path ~/.vscode/snippets -l python
        """,
    )

    parser.add_argument(
        "-s",
        "--snippet",
        type=str,
        required=False,
        help="Target language for snippets",
    )

    parser.add_argument(
        "-ls",
        "--list",
        action="store_true",
        help="List available snippets in the snippets directory",
        default=False,
    )

    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default="",
        required=False,
        help="Language identifier for Markdown code blocks (e.g., shellscript snippet for bash), defaults to snippet",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file path (default: stdout)",
        required=False,
    )

    parser.add_argument(
        "--print",
        action="store_true",
        help="Print the Markdown output to console instead of writing to a file",
        default=False,
    )

    return parser

    return markdown_content


def export_snippet_md(dest: str, snippet_md: str) -> int:
    try:
        with Path(dest).open("w", encoding="utf-8") as f:
            f.write(snippet_md)

        console.print(f"[green]Snippets exported to {dest}[/green]")
        return 0
    except Exception as e:
        console.print(f"[red bold]Error exporting snippets: {e}[/red bold]")
    return 1


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()
    assert get_snippets_path().exists(), (
        "Snippet path does not exist. Please check the path or hard code the path to your snippets directory."
    )
    exit_code = 0
    try:
        processor = SnippetProcessor(
            snippet_name=args.snippet,
            snippet_lang=args.language or None,
        )
        if args.list:
            console.print("[green]Available snippets:[/green]")
            for snippet in ls_snippets():
                console.print(f"- [blue]{snippet}[/blue]")

        if not args.snippet:
            return 0

        snippets = processor.load_snippet_file()
        markdown_content = processor.write_markdown(snippets)
        if not markdown_content:
            raise SnippetError("No valid snippets found in the file.")

        if args.print:
            console.print(Markdown(markdown_content, justify="full"))

        if args.output:
            exit_code = export_snippet_md(args.output, markdown_content)

    except SnippetError as e:
        console.print(f"[red bold]Error: {e}[/red bold]")
        exit_code = 1
    except KeyboardInterrupt:
        console.print("\n[yellow]Closing program..[/yellow]")
        exit_code = 1
    except Exception as e:
        console.print(f"[red bold]Unexpected error: {e}[/red bold]")
        exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
