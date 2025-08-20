"""ContentManager: build the HTML body and full documents.

This module centralizes HTML manipulations:
- optional logo injection into <h1> headings
- rendering a footer container (positioning is handled by CSS in themes)
- optional title and labels sections
- final full-document assembly (head + body)
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from .tokens import replace_tokens


class ContentManager:
    """Compose HTML content blocks and produce complete HTML documents."""

    def __init__(
        self,
        logo_path: Path,
        title: str = "",
        labels: list[str] | None = None,
        footer_text: str = "",
    ) -> None:
        """Initialize a ContentManager."""
        self._TRAILING_HR_PATTERN = re.compile(
            r"(<hr\s*/?>\s*)+$", re.DOTALL | re.IGNORECASE
        )
        self._HR1_RE_PATTERN = re.compile(
            r"<h1[^>]*>.*?</h1>", re.DOTALL | re.IGNORECASE
        )
        self.logo_path = logo_path
        self.title = title
        self.labels = labels or []
        self.footer_text = footer_text

    def _remove_trailing_hr(self, html: str) -> str:
        """Remove trailing <hr> or <hr /> from the end of the HTML content."""
        return re.sub(self._TRAILING_HR_PATTERN, "", html)

    def _inject_logo_into_h1(self, html: str) -> str:
        """Wrap every <h1> with a header container and inject the logo image.

        If `logo_path` is not set, the input HTML is returned unchanged.
        """
        if not self.logo_path:
            return html

        def _wrap(m: re.Match) -> str:
            h1 = m.group(0)
            return f"""<div class="slide-header">
                {h1}<img class="brand-logo" src="{self.logo_path}" alt="logo" />
            </div>"""

        return re.sub(self._HR1_RE_PATTERN, _wrap, html)

    def _render_footer_html(self) -> str:
        """Render a footer container as <div id="footer">…</div>.

        The footer is returned as a plain HTML block. Its positioning (e.g.,
        paged-media margin boxes via `element(footer)`) is expected to be
        handled by CSS in the theme.
        """
        if not self.footer_text:
            return ""
        txt = replace_tokens(self.footer_text)
        # Escape each line, preserving empty lines on purpose.
        lines = txt.splitlines()
        inner = "".join(f"<div>{line}</div>" for line in lines)
        return f'<div id="footer">{inner}</div>'

    def _render_labels(self) -> str:
        """Render a minimal labels block."""
        return (
            f'<div class="labels">Labels: {", ".join(self.labels)}</div>'
            if self.labels
            else ""
        )

    def _render_title(self) -> str:
        """Render a first-slide title section."""
        return (
            f'<section class="first-slide"><h1>{self.title}</h1></section>'
            if self.title
            else ""
        )

    def build_body(
        self,
        content_html: str,
    ) -> str:
        """Build the <body> inner HTML (without <head> and CSS).

        Order matters: the footer is placed first so CSS paged-media features
        (like `element(footer)`) can reference it reliably.
        """
        content_html = self._inject_logo_into_h1(content_html)
        content_html = self._remove_trailing_hr(content_html)
        footer_html = self._render_footer_html()
        title_html = self._render_title()
        labels_html = self._render_labels()
        return f"""
            {footer_html}
            {title_html}
            {labels_html}
            {content_html}
        """
