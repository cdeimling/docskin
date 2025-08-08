import pathlib
import markdown
from weasyprint import HTML
from .styles import StyleManager

class MarkdownToPDFConverter:
    """Converts Markdown files into GitHub-styled PDFs."""

    def __init__(self, style_manager: StyleManager = None):
        self.style = style_manager or StyleManager.from_github_default()

    def convert_file(self, md_path: pathlib.Path, output_path: pathlib.Path):
        """Convert a single Markdown file to a PDF."""
        md_content = md_path.read_text(encoding="utf-8")
        html_content = self._markdown_to_html(md_content)
        HTML(string=html_content).write_pdf(output_path)

    def convert_folder(self, folder_path: pathlib.Path):
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
