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
import markdown
from weasyprint import HTML

from docskin.github_api import GitHubIssueFetcher
from docskin.styles import CustomCSSStyle


@click.group()
def main() -> None:
    """📄 Convert Markdown or GitHub issues to styled PDF files."""
    pass  # noqa: PIE790


def common_options(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to add common options to CLI commands."""

    @click.option(
        "--logo",
        type=click.Path(exists=True),
        help="Optional path to logo image",
    )
    @click.option(
        "--css-style",
        type=click.Path(exists=True),
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

    fetcher = GitHubIssueFetcher(repo, issue, api_base=api_base)
    issue_data = fetcher.fetch()

    title = issue_data["title"]
    labels = [label["name"] for label in issue_data.get("labels", [])]
    content = markdown.markdown(
        issue_data["body"], extensions=["fenced_code", "codehilite"]
    )

    click.echo(f"📄 Rendering issue #{issue} to PDF...")

    style_renderer = CustomCSSStyle(
        title, content, labels, css_path=Path(css_style)
    )
    html = style_renderer.render_html()

    click.echo("🖨️  Rendering PDF...")
    HTML(string=html).write_pdf(output)
    click.echo(f"✅ Saved as {output}")


@main.command(name="md")
@click.option(
    "--output",
    required=True,
    type=click.Path(file_okay=True),
    help="Output directory for PDFs",
)
@click.option(
    "--input",
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
    required=True,
    help="Path to the Markdown file",
)
@common_options
def md(
    input: Path,  # noqa: A002
    output: Path,
    logo: Path,  # noqa: ARG001
    css_style: Path,
) -> None:
    """Convert a local Markdown file to PDF with optional theming."""
    click.echo(f"📄 Converting {input} to PDF using style '{css_style}'")

    with input.open("r", encoding="utf-8") as f:
        md_content = f.read()

    title = input.stem
    labels: list[str] = []
    content = markdown.markdown(
        md_content, extensions=["fenced_code", "codehilite"]
    )

    style_renderer = CustomCSSStyle(
        title, content, labels, css_path=Path(css_style)
    )
    html = style_renderer.render_html()

    click.echo("🖨️  Rendering PDF...")
    HTML(string=html).write_pdf(output)
    click.echo(f"✅ Saved as {output}")


@main.command(name="md-dir")
@click.option(
    "--output",
    required=True,
    type=click.Path(file_okay=False, dir_okay=True),
    help="Output directory for PDFs",
)
@click.option(
    "--input",
    required=True,
    type=click.Path(file_okay=False, exists=True, dir_okay=True),
    help="Directory containing Markdown files",
)
@common_options
def md_dir(
    input: Path,
    logo: Path,  # noqa: ARG001
    css_style: Path,
    output: Path,
) -> None:
    """Convert all Markdown files in a directory to PDF."""
    click.echo(f"📁 Scanning {input} for Markdown files...")
    output = Path(output)
    input = Path(input)

    output.mkdir(parents=True, exist_ok=True)

    md_files = list(input.rglob("*.md"))
    if not md_files:
        click.echo("⚠️  No Markdown files found.")
        return

    for path in md_files:
        rel_path = path.relative_to(input)
        output_path = output / rel_path.with_suffix(".pdf")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        click.echo(f"📄 Rendering {rel_path} -> {output_path}")

        with path.open("r", encoding="utf-8") as f:
            md_content = f.read()

        title = path.stem
        labels: list[str] = []
        content = markdown.markdown(
            md_content, extensions=["fenced_code", "codehilite"]
        )

        style_renderer = CustomCSSStyle(
            title, content, labels, css_path=Path(css_style)
        )
        html = style_renderer.render_html()
        HTML(string=html).write_pdf(output_path)

    click.echo(f"✅ All Markdown files converted to PDF in {output}")
