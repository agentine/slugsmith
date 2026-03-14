"""Core slugification logic."""

from __future__ import annotations

import re


_WHITESPACE_RE = re.compile(r"[\s]+")
_NON_WORD_RE = re.compile(r"[^\w\s-]")


def slugify(
    text: str,
    separator: str = "-",
    lowercase: bool = True,
    max_length: int = 0,
    word_boundary: bool = False,
    save_order: bool = False,
    stopwords: tuple[str, ...] = (),
    regex_pattern: str | None = None,
    replacements: list[tuple[str, str]] | None = None,
    allow_unicode: bool = False,
    lang: str | None = None,
) -> str:
    """Generate a URL-friendly slug from the given text."""
    if not text:
        return ""

    slug = text

    if lowercase:
        slug = slug.lower()

    # Basic: strip non-word chars, replace whitespace with separator
    slug = _NON_WORD_RE.sub("", slug)
    slug = _WHITESPACE_RE.sub(separator, slug)
    slug = slug.strip(separator)

    return slug
