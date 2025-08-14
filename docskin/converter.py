"""Module for converting Markdown files to PDFs using WeasyPrint."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path

import markdown
from weasyprint import HTML

from docskin.styles import StyleManager

from .github_api import GitHubIssueFetcher


class MarkdownHTMLExtractor:
    """Converts Markdown text to HTML."""

    def __init__(self, extensions: list[str] | None = None) -> None:
        """Initialize with optional Markdown extensions."""
        self.extensions = extensions or ["fenced_code", "tables", "codehilite"]

    def extract(self, md_text: str) -> str:
        """Convert Markdown text to HTML."""
        return markdown.markdown(
            md_text,
            extensions=self.extensions,
            output_format="xhtml",
        )


class MarkdownPdfRenderer:
    """Converts Markdown files into GitHub-styled PDFs."""

    def __init__(self, style_manager: StyleManager) -> None:
        """Initialize the converter with a style manager."""
        self.style = style_manager
        self.extractor = MarkdownHTMLExtractor()

    def render_file(self, input_md_path: Path, output_pdf_path: Path) -> None:
        """Convert a single Markdown file to a PDF."""
        content = input_md_path.read_text(encoding="utf-8")
        title = input_md_path.stem
        html_content = self.markdown_to_html(content, title)
        if output_pdf_path.is_file():
            output_pdf_path.unlink()
        HTML(string=html_content).write_pdf(output_pdf_path)

    def render_folder(
        self, input_md_folder: Path, output_md_folder: Path
    ) -> Generator[tuple[str, str], Path, None]:
        """Convert all Markdown files in a folder to PDF."""
        for md_file in input_md_folder.rglob("*.md"):
            relative_path = md_file.relative_to(input_md_folder).with_suffix(
                ".pdf"
            )
            output_path = output_md_folder / relative_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            self.render_file(md_file, output_path)
            yield md_file.name, output_path.name

    def markdown_to_html(
        self,
        content: str,
        title: str | None = None,
        labels: list[str] | None = None,
    ) -> str:
        """Convert Markdown text to HTML and apply styles.

        Returns.
        -------
        str
            The styled HTML content.
        """
        markdown_content = self.extractor.extract(content)
        return self.style.render_html(markdown_content, title, labels)


class GitHubIssuePdfRenderer:
    """Service for converting GitHub issues to styled PDF documents."""

    def __init__(self, style_manager: StyleManager) -> None:
        """Initializes the converter and sets up a MarkdownHTMLExtractor."""
        self.style_manager = style_manager
        self.extractor = MarkdownHTMLExtractor()

    def render(
        self, repo: str, issue: int, api_base: str, output: Path
    ) -> None:
        """Fetch a GitHub issue and render it as a styled PDF."""
        fetcher = GitHubIssueFetcher(repo, issue, api_base=api_base)
        issue_data = fetcher.fetch()
        title = issue_data["title"]
        labels = [label["name"] for label in issue_data.get("labels", [])]
        content = self.extractor.extract(issue_data["body"])
        html = self.style_manager.render_html(content, title, labels)
        HTML(string=html).write_pdf(output)


def get_markdown_converter(
    css_style: Path, css_class: str, logo: Path
) -> MarkdownPdfRenderer:
    """Get a Markdown to PDF converter."""
    style_manager = StyleManager(css_style, css_class, logo)
    return MarkdownPdfRenderer(style_manager)


def get_github_issue_converter(
    css_style: Path, css_class: str, logo: Path
) -> GitHubIssuePdfRenderer:
    """Get a GitHub issue to PDF converter."""
    style_manager = StyleManager(css_style, css_class, logo)
    return GitHubIssuePdfRenderer(style_manager)
