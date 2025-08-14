"""CLI command for converting GitHub issues to PDF using docskin.

This module defines a Click command that fetches a GitHub issue
and renders it as a PDF, optionally applying custom CSS styles.
"""

from pathlib import Path

import click

from docskin.converter import get_github_issue_converter


@click.command(name="github")
@click.option(
    "--output", required=True, type=click.Path(), help="Output PDF file path"
)
@click.option("--repo", required=True, help="GitHub repo in owner/name format")
@click.option("--issue", required=True, type=int, help="Issue number")
@click.option(
    "--api-base", default="https://api.github.com", help="GitHub API base URL"
)
@click.pass_context
def github(
    ctx: click.Context,
    repo: str,
    issue: int,
    api_base: str,
    output: Path,
) -> None:
    """Convert a GitHub issue to PDF with optional theming."""
    click.echo(f"🐙 Fetching issue #{issue} from {repo}")
    converter = get_github_issue_converter(
        ctx.obj["css_style"], ctx.obj["css_class"], ctx.obj["logo"]
    )
    converter.render(repo, issue, api_base, output)
    click.echo(f"✅ Saved as {output}")
