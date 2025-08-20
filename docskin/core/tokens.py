"""Lightweight token replacement utilities for HTML generation.

Supported tokens:
- {date}                -> current date in DD.MM.YYYY
- {date:<strftime>}     -> current date formatted using a Python strftime format
- {year}                -> current year in YYYY

You can pass overrides to inject or override token values programmatically.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

_TOKEN_RE = re.compile(r"\{(\w+)(?::([^}]+))?\}")


def replace_tokens(
    text: str,
    overrides: dict[str, str] | None = None,
    now: datetime | None = None,
) -> str:
    """Replace simple curly-brace tokens in `text`.

    Parameters:
    ----------
    text:
        Input string possibly containing tokens like `{date}`,
        `{date:%Y-%m-%d}`, `{year}`.
        If `text` is None, an empty string is returned.
    overrides:
        Optional mapping used to override or add token values. Values here take
        precedence over built-in tokens.
    now:
        Optional datetime used as the current time source. If omitted,
        `datetime.now(tz=timezone.utc)` is used.

    Returns:
    -------
    str
        The input with tokens replaced. Unknown tokens remain unchanged.
    """
    if text is None:
        return ""

    now = now or datetime.now(tz=timezone.utc)
    values: dict[str, str] = {
        "date": now.strftime("%d.%m.%Y"),
        "year": now.strftime("%Y"),
    }
    if overrides:
        values.update(overrides)

    def _repl(m: re.Match) -> str:
        key, fmt = m.group(1), m.group(2)
        if key == "date" and fmt:
            try:
                return now.strftime(fmt)
            except ValueError:
                return m.group(0)
        return values.get(key, m.group(0)) or m.group(0)

    return _TOKEN_RE.sub(_repl, text)
