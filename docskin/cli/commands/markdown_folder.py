"""CLI command for converting all Markdown files in a directory to PDF.

This module defines the 'md-dir' command, which scans a directory for Markdown
files and converts them to PDF using the specified CSS style.
"""

from pathlib import Path

import click

from docskin.core.converter import get_markdown_converter


@click.command(name="md-dir")
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
@click.pass_context
def md_dir(
    ctx: click.Context,
    input_md_folder: Path,
    output_md_folder: Path,
) -> None:
    """Convert all Markdown files in a directory to PDF."""
    click.echo(f"📁 Scanning {input_md_folder} for Markdown files...")
    converter = get_markdown_converter(
        ctx.obj["css_style"], ctx.obj["css_class"], ctx.obj["logo"]
    )
    results = list(converter.render_folder(input_md_folder, output_md_folder))
    click.echo(f"✅ All Markdown files converted to PDF in {output_md_folder}")
    if not results:
        click.echo("No Markdown files found")
        return
    for md_name, pdf_name in results:
        click.echo(f"  - {md_name} ➔ {pdf_name}")
