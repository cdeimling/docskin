"""CLI for converting Markdown and GitHub issues to styled PDF files.

This module provides commands to:
- Convert a GitHub issue to PDF
- Convert a local Markdown file to PDF
- Convert all Markdown files in a directory to PDF
"""

import functools
from pathlib import Path
from typing import Any, Callable

import click

from docskin.converter import GitHubIssueToPDFService, MarkdownToPDFConverter
from docskin.styles import StyleManager


@click.group()
def main() -> None:
    """📄 Convert Markdown or GitHub issues to styled PDF files."""
    pass  # noqa: PIE790


def common_options(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to add common options to CLI commands."""

    @click.option(
        "--logo",
        type=click.Path(exists=True, path_type=Path),
        help="Optional path to logo image",
    )
    @click.option(
        "--css-style",
        type=click.Path(exists=True, path_type=Path),
        help="Optional path to CSS style file",
        default="assets/markdown-dark.css",
    )
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        return func(*args, **kwargs)

    return wrapper


@main.command(name="github")
@click.option(
    "--output", required=True, type=click.Path(), help="Output PDF file path"
)
@click.option("--repo", required=True, help="GitHub repo in owner/name format")
@click.option("--issue", required=True, type=int, help="Issue number")
@click.option(
    "--api-base", default="https://api.github.com", help="GitHub API base URL"
)
@common_options
def github(
    repo: str,
    issue: int,
    api_base: str,
    css_style: Path,
    output: Path,
    logo: Path,  # noqa: ARG001
) -> None:
    """Convert a GitHub issue to PDF with optional theming."""
    click.echo(
        f"🐙 Fetching issue #{issue} from {repo} with style '{css_style}'"
    )

    style_manager = StyleManager(css_style)
    service = GitHubIssueToPDFService(style_manager)
    service.convert(repo, issue, api_base, output)
    click.echo(f"✅ Saved as {output}")


@main.command(name="md")
@click.option(
    "--output",
    "output_pdf",
    required=True,
    type=click.Path(file_okay=True, path_type=Path),
    help="Output directory for PDFs",
)
@click.option(
    "--input",
    "input_md",
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
    required=True,
    help="Path to the Markdown file",
)
@common_options
def md(
    input_md: Path,
    output_pdf: Path,
    logo: Path,  # noqa: ARG001
    css_style: Path,
) -> None:
    """Convert a local Markdown file to PDF with optional theming."""
    click.echo(f"📄 Rendering {input_md} to PDF...")
    style_manager = StyleManager(css_path=css_style)
    converter = MarkdownToPDFConverter(style_manager)
    converter.convert_file(input_md, output_pdf)
    click.echo(f"✅ Saved as {output_pdf}")


@main.command(name="md-dir")
@click.option(
    "--output",
    "output_md_folder",
    required=True,
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    help="Output directory for PDFs",
)
@click.option(
    "--input",
    "input_md_folder",
    required=True,
    type=click.Path(
        file_okay=False, exists=True, dir_okay=True, path_type=Path
    ),
    help="Directory containing Markdown files",
)
@common_options
def md_dir(
    input_md_folder: Path,
    logo: Path,  # noqa: ARG001
    css_style: Path,
    output_md_folder: Path,
) -> None:
    """Convert all Markdown files in a directory to PDF."""
    click.echo(f"📁 Scanning {input_md_folder} for Markdown files...")
    style_manager = StyleManager(css_path=css_style)
    converter = MarkdownToPDFConverter(style_manager)
    converter.convert_folder(input_md_folder, output_md_folder)
    click.echo(f"✅ All Markdown files converted to PDF in {output_md_folder}")
