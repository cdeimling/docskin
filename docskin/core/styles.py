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

    def _insert_logo_in_h1_headers(self, html: str) -> str:
        """Wrap every <h1> in the HTML with .slide-header and logo."""

        def _insert_logo_in_h1_matches(match: re.Match) -> str:
            h1_text = match.group(0)
            return f"""
            <div class="slide-header">
                {h1_text}
                <img class="brand-logo" src="{self.logo_path}" alt="Logo">
            </div>
            """

        return re.sub(
            r"<h1[^>]*>.*?</h1>",
            _insert_logo_in_h1_matches,
            html,
            flags=re.DOTALL,
        )

    def __init__(self, css_path: Path, css_class: str, logo_path: Path) -> None:
        """Initialize PDFStyle with required fields."""
        self.logo_path = logo_path
        self.css_class = css_class
        self.css_text = css_path.read_text(encoding="utf-8")
        self.margin = "2cm"

    def get_css_value(self, property_name: str) -> str | None:
        """Extract the value of a CSS property from the CSS text."""
        match = re.search(rf"{property_name}\s*:\s*([^;]+);", self.css_text)
        return match.group(1).strip() if match else None

    def render_html(
        self,
        content: str,
        title: str | None = None,
        labels: list[str] | None = None,
    ) -> str:
        """Render the HTML into a CSS-styled PDF."""
        background_color = self.get_css_value("background-color")
        labels_html = (
            f"<p><strong>Labels:</strong> {', '.join(labels)}</p>"
            if labels
            else ""
        )
        content_with_logo = self._insert_logo_in_h1_headers(content)

        first_slide = ""
        if title:
            first_slide = f"""
                <div class="slide-header">
                    <h1>{title}</h1>
                    <img class="brand-logo" src="{self.logo_path}" alt="Logo">
                </div>
            """

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
                {first_slide}
                {labels_html}
                {content_with_logo}
            </body>
        </html>
        """
