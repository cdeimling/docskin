"""Module for converting Markdown files to PDFs using WeasyPrint."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pathlib
    from collections.abc import Generator

    from .styles import BaseStyle

import markdown
from weasyprint import HTML


class MarkdownToPDFConverter:
    """Converts Markdown files into GitHub-styled PDFs."""

    def __init__(self, style_manager: BaseStyle | None = None) -> None:
        """Initialize the converter with a style manager."""
        self.style = style_manager

    def convert_file(
        self, md_path: pathlib.Path, output_path: pathlib.Path
    ) -> None:
        """Convert a single Markdown file to a PDF."""
        md_content = md_path.read_text(encoding="utf-8")
        html_content = self._markdown_to_html(md_content)
        HTML(string=html_content).write_pdf(output_path)

    def convert_folder(
        self, folder_path: pathlib.Path
    ) -> Generator[tuple[str, str], pathlib.Path, None]:
        """Convert all Markdown files in a folder to PDF."""
        for md_file in folder_path.glob("*.md"):
            output_path = md_file.with_suffix(".pdf")
            self.convert_file(md_file, output_path)
            yield md_file.name, output_path.name

    def _markdown_to_html(self, md_text: str) -> str:
        body = markdown.markdown(
            md_text, extensions=["fenced_code", "tables", "codehilite"]
        )
        full_style = self.style.build_full_style()
        return f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>{full_style}</style>
        </head>
            <body class="markdown-body">{body}</body>
        </html>
        """
