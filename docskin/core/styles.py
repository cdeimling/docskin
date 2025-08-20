"""PDF style utilities for Markdown to PDF conversion."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import re

from docskin.core.content import ContentManager


class StyleManager:
    """Flexible CSS style manager for Markdown HTML rendering.

    Optional public attributes:
        margin: Page margin (default: "1cm").
        background: Background color (optional).
        foreground: Foreground/text color (optional).
        body_class: CSS class for <body> (optional).
    """

    def __init__(
        self, css_path: Path, css_class: str, logo_path: Path, footer_text: str
    ) -> None:
        """Initialize PDFStyle with required fields."""
        self.logo_path = logo_path
        self.css_class = css_class
        self.css_text = css_path.read_text(encoding="utf-8")
        self.footer_text = footer_text
        self.margin = "2cm"

    def get_css_value(self, property_name: str) -> str | None:
        """Extract the value of a CSS property from the CSS text."""
        match = re.search(rf"{property_name}\s*:\s*([^;]+);", self.css_text)
        return match.group(1).strip() if match else None

    def render_html(
        self,
        content: str,
        title: str = "",
        labels: list[str] | None = None,
    ) -> str:
        """Render the HTML into a CSS-styled PDF."""
        background_color = self.get_css_value("background-color")

        content_manager = ContentManager(
            logo_path=self.logo_path,
            title=title,
            labels=labels,
            footer_text=self.footer_text,
        )
        body = content_manager.build_body(content_html=content)
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
                {body}
            </body>
        </html>
        """
