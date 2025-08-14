"""PDF style utilities for Markdown to PDF conversion."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import re


class StyleManager:
    """Flexible CSS style manager for Markdown HTML rendering.

    Optional public attributes:
        margin: Page margin (default: "1cm").
        background: Background color (optional).
        foreground: Foreground/text color (optional).
        body_class: CSS class for <body> (optional).
    """

    def __init__(self, css_path: Path, css_class: str, logo_path: Path) -> None:
        """Initialize PDFStyle with required fields."""
        self.logo_path = logo_path
        self.css_class = css_class
        self.css_text = css_path.read_text(encoding="utf-8")
        self.margin = "2cm"

    def get_css_value(self, property_name: str) -> str | None:
        """Extrahiere den Wert einer CSS-Eigenschaft aus dem CSS-Text."""
        match = re.search(rf"{property_name}\s*:\s*([^;]+);", self.css_text)
        if match:
            return match.group(1).strip()
        return None

    def render_html(
        self,
        content: str,
        title: str | None = None,
        labels: list[str] | None = None,
    ) -> str:
        """Render the HTML for the styled PDF."""
        background_color = self.get_css_value("background-color")
        labels_html = (
            f"<p><strong>Labels:</strong> {', '.join(labels)}</p>"
            if labels
            else ""
        )
        return f"""
        <html>
            <head>
                <meta charset="utf-8">
                <style>
                    @page {{
                        margin: {self.margin};
                        background: {background_color};
                    }}
                    {self.css_text}
                </style>
            </head>
            <body class="{self.css_class}">
                <h1>{title}<img class="brand-logo" src="{self.logo_path}" alt="Logo"></h1>
                {labels_html}
                {content}
            </body>
        </html>
        """
