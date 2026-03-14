"""Unicode to ASCII transliteration engine."""

from __future__ import annotations


CHAR_MAP: dict[str, str] = {}


def transliterate(text: str) -> str:
    """Transliterate Unicode text to ASCII."""
    return text
