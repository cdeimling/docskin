"""Mermaid diagram pre-processing for Markdown-to-HTML conversion."""

from __future__ import annotations

import base64
import json
import logging
import re

import requests

logger = logging.getLogger(__name__)

_MERMAID_FENCE: re.Pattern[str] = re.compile(
    r"```mermaid\s*(.*?)\s*```",
    re.DOTALL,
)

_MERMAID_INK_URL = "https://mermaid.ink/svg/{encoded}"


def _encode_mermaid(code: str) -> str:
    """Encode Mermaid diagram code for use with the mermaid.ink API.

    Args:
        code: Raw Mermaid diagram definition.

    Returns:
        A URL-safe base64 string representing the JSON payload.
    """
    payload = json.dumps({"code": code, "mermaid": {"theme": "default"}})
    return base64.urlsafe_b64encode(payload.encode()).decode()


def render_mermaid_to_svg(code: str) -> str:
    """Render a Mermaid diagram to an SVG string via the mermaid.ink API.

    Sends the diagram source to ``https://mermaid.ink/svg/`` and returns
    the resulting SVG markup.  On any HTTP or network error the function
    logs a warning and returns an HTML ``<pre>`` block containing the
    original source so the document still renders without crashing.

    Args:
        code: Raw Mermaid diagram definition.

    Returns:
        An SVG string on success, or an HTML ``<pre>`` fallback on failure.
    """
    url = _MERMAID_INK_URL.format(encoded=_encode_mermaid(code))
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.warning(
            "Mermaid rendering failed (%s); using plain-text fallback.", exc
        )
        return f'<pre class="mermaid-fallback"><code>{code}</code></pre>'
    return response.text


def preprocess_mermaid(text: str) -> str:
    """Replace Mermaid fenced code blocks with inline SVG in Markdown text.

    Scans *text* for fenced code blocks tagged ``mermaid``, calls the
    mermaid.ink rendering API for each one, and substitutes the resulting
    SVG (or a plain-text fallback) into the text before it is parsed by
    the Markdown library.

    Args:
        text: Raw Markdown text that may contain Mermaid fenced blocks.

    Returns:
        The text with every ``mermaid`` code fence replaced by an HTML div.
    """

    def _replace_block(match: re.Match[str]) -> str:
        code = match.group(1).strip()
        svg = render_mermaid_to_svg(code)
        return f'\n<div class="mermaid-diagram">\n{svg}\n</div>\n'

    return _MERMAID_FENCE.sub(_replace_block, text)
