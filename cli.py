"""
CLI commands for docskin: Convert Markdown files and GitHub issues to styled PDF documents.
"""
from pathlib import Path
import functools
import click
import markdown
from weasyprint import HTML

from docskin.styles import CustomCSSStyle
from docskin.github_api import GitHubIssueFetcher
import click
import functools
import markdown
from weasyprint import HTML
from pathlib import Path

from docskin.styles import CustomCSSStyle
from docskin.github_api import GitHubIssueFetcher



@click.group()
def main() -> None:
    """📄 Convert Markdown or GitHub issues to styled PDF files."""
    # Entry point for CLI group

def common_pdf_options(func: callable) -> callable:
    """    Decorator to add common PDF options (logo, CSS style) to CLI commands.    """
    @click.option("--logo", type=click.Path(exists=True), help="Optional path to logo image")
    @click.option("--css-style", type=click.Path(exists=True), help="Optional path to CSS style file", default="assets/markdown-dark.css")
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> None:
        return func(*args, **kwargs)
    return wrapper

@main.command(name="github")
@click.option("--output", required=True, type=click.Path(), help="Output PDF file path")
@click.option("--repo", required=True, help="GitHub repo in owner/name format")
@click.option("--issue", required=True, type=int, help="Issue number")
@click.option("--api-base", default="https://api.github.com", help="GitHub API base URL")
@common_pdf_options
def github(repo: str, issue: int, api_base: str, css_style: Path, output: Path, logo: Path) -> None:
    """Convert a GitHub issue to PDF with optional theming."""
    click.echo(f"🐙 Fetching issue #{issue} from {repo} with style "{css_style}"")

    fetcher = GitHubIssueFetcher(repo, issue, api_base=api_base)
    issue_data = fetcher.fetch()

    title = issue_data["title"]
    labels = [label["name"] for label in issue_data.get("labels", [])]
    content = markdown.markdown(issue_data["body"], extensions=["fenced_code", "codehilite"])

    click.echo(f"📄 Rendering issue #{issue} to PDF...")

    style_renderer = CustomCSSStyle(title, content, labels, css_path=Path(css_style))
    html = style_renderer.render_html()

    click.echo("🖨️  Rendering PDF...")
    HTML(string=html).write_pdf(output)
    click.echo(f"✅ Saved as {output}")


@main.command(name="md")
@click.option("--output", required=True, type=click.Path(file_okay=False), help="Output directory for PDFs")
@click.option("--input", type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
              required=True, help="Path to the Markdown file")
@common_pdf_options
def md(input: Path, output: Path, logo: Path, css_style: Path) -> None:
    """Convert a local Markdown file to PDF with optional theming."""
    click.echo(f"📄 Converting {input} to PDF using style "{css_style}"")

    with input.open("r", encoding="utf-8") as f:
        md_content = f.read()

    title = input.stem
    labels:list[str] = []
    content = markdown.markdown(md_content, extensions=["fenced_code", "codehilite"])

    style_renderer = CustomCSSStyle(title, content, labels, css_path=Path(css_style))
    html = style_renderer.render_html()

    if output.is_file():
        output.unlink()

    click.echo("🖨️  Rendering PDF...")
    HTML(string=html).write_pdf(output)
    click.echo(f"✅ Saved as {output}")


@main.command(name="md-dir")
@click.option("--output", required=True, type=click.Path(file_okay=False, dir_okay=True), help="Output directory for PDFs")
@click.option("--input", required=True, type=click.Path(file_okay=False, exists=True, dir_okay=True),
    help="Directory containing Markdown files")
@common_pdf_options
def md_dir(input: Path, logo: Path, css_style: Path, output: Path) -> None:
    """Convert all Markdown files in a directory to PDF with optional theming."""
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
        labels:list[str] = []
        content = markdown.markdown(md_content, extensions=["fenced_code", "codehilite"])

        style_renderer = CustomCSSStyle( title, content, labels, css_path=Path(css_style))
        html = style_renderer.render_html()
        HTML(string=html).write_pdf(output_path)

    click.echo(f"✅ All Markdown files converted to PDF in {output}")
