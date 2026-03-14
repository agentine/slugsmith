"""Core slugification logic."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable, Sequence

from slugsmith.special import apply_language
from slugsmith.transliterate import transliterate

# Pre-compiled default regex patterns
_DEFAULT_ALLOWED_RE = re.compile(r"[^\w\s-]", re.UNICODE)
_UNICODE_ALLOWED_RE = re.compile(r"[^\w\s-]", re.UNICODE)
_WHITESPACE_SEP_RE = re.compile(r"[-\s]+")


def slugify(
    text: str,
    separator: str = "-",
    lowercase: bool = True,
    max_length: int = 0,
    word_boundary: bool = False,
    save_order: bool = False,
    stopwords: Iterable[str] = (),
    regex_pattern: str | None = None,
    replacements: Sequence[Sequence[str]] | None = None,
    allow_unicode: bool = False,
    lang: str | None = None,
) -> str:
    """Generate a URL-friendly slug from the given text.

    Args:
        text: Input string to slugify.
        separator: Character(s) to use between words. Default ``"-"``.
        lowercase: Convert to lowercase. Default ``True``.
        max_length: Maximum length of the slug (0 = unlimited).
        word_boundary: Truncate at word boundary when *max_length* is set.
        save_order: Accepted for python-slugify compatibility (word order is
            always preserved).
        stopwords: Words to remove from the slug. Accepts any iterable of strings.
        regex_pattern: Custom regex pattern for allowed characters.
        replacements: Sequence of ``(old, new)`` pairs applied first. Accepts
            lists of tuples or lists of lists.
        allow_unicode: Keep Unicode characters in the slug.
        lang: Language code for language-specific transliteration.
    """
    if not text:
        return ""

    slug = text

    # 1. Apply literal replacements
    if replacements:
        for old, new in replacements:
            slug = slug.replace(old, new)

    # 2/3. Transliterate or normalize
    if not allow_unicode:
        slug = apply_language(slug, lang)
        slug = transliterate(slug)
    else:
        slug = unicodedata.normalize("NFC", slug)

    # 4. Apply regex pattern (strip disallowed chars)
    if regex_pattern is not None:
        slug = re.sub(regex_pattern, "", slug)
    else:
        if allow_unicode:
            slug = _UNICODE_ALLOWED_RE.sub("", slug)
        else:
            slug = _DEFAULT_ALLOWED_RE.sub("", slug)

    # 5. Apply lowercase
    if lowercase:
        slug = slug.lower()

    # 6. Split on whitespace/separators, filter stopwords
    tokens = _WHITESPACE_SEP_RE.split(slug.strip())
    tokens = [t for t in tokens if t]  # remove empties

    if stopwords:
        stop_set = {w.lower() for w in stopwords}
        tokens = [t for t in tokens if t.lower() not in stop_set]

    # 7. Join with separator
    slug = separator.join(tokens)

    # 8/9. Apply max_length with optional word boundary
    if max_length > 0:
        if word_boundary:
            slug = _truncate_word_boundary(slug, max_length, separator)
        else:
            slug = slug[:max_length]

    # 10. Strip leading/trailing separators
    slug = slug.strip(separator)

    return slug


def _truncate_word_boundary(
    slug: str, max_length: int, separator: str
) -> str:
    """Truncate slug at a word boundary, respecting max_length."""
    if len(slug) <= max_length:
        return slug
    truncated = slug[:max_length]
    # If we cut in the middle of a word, back up to the last separator
    if slug[max_length:max_length + 1] != separator and separator in truncated:
        truncated = truncated[: truncated.rfind(separator)]
    return truncated.strip(separator)
