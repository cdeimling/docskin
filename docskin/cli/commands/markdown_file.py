"""CLI command for converting Markdown files to PDF using docskin.

This module defines the 'md' command, which takes a Markdown file
and outputs a themed PDF.
"""

from pathlib import Path

import click

from docskin.core.converter import get_markdown_converter


@click.command(name="md")
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
@click.pass_context
def md(
    ctx: click.Context,
    input_md: Path,
    output_pdf: Path,
) -> None:
    """Convert a local Markdown file to PDF with optional theming."""
    click.echo(f"📄 Rendering {input_md} to PDF...")
    converter = get_markdown_converter(
        ctx.obj["css_style"],
        ctx.obj["css_class"],
        ctx.obj["logo"],
        ctx.obj["footer_text"],
    )
    converter.render_file(input_md, output_pdf)
    click.echo(f"✅ Saved as {output_pdf}")
