"""Language-specific character mappings."""

from __future__ import annotations


LANGUAGE_MAP: dict[str, dict[str, str]] = {}


def apply_language(text: str, lang: str | None) -> str:
    """Apply language-specific character substitutions."""
    return text
