"""Compatibility tests — verifies slugsmith produces expected output
for common python-slugify use cases."""

from __future__ import annotations

import pytest
from slugsmith import slugify


@pytest.mark.parametrize(
    "text,kwargs,expected",
    [
        # Basic slugification
        ("Hello World", {}, "hello-world"),
        ("hello world", {}, "hello-world"),
        ("  hello   world  ", {}, "hello-world"),
        # Separator
        ("hello world", {"separator": "_"}, "hello_world"),
        ("hello world", {"separator": "."}, "hello.world"),
        # Lowercase
        ("Hello", {"lowercase": False}, "Hello"),
        ("HELLO WORLD", {"lowercase": True}, "hello-world"),
        # Max length
        ("hello world foo", {"max_length": 5}, "hello"),
        ("hello world foo", {"max_length": 11}, "hello-world"),
        # Word boundary
        ("hello world foo", {"max_length": 12, "word_boundary": True}, "hello-world"),
        # Stopwords
        ("the quick brown fox", {"stopwords": ("the",)}, "quick-brown-fox"),
        # Replacements
        ("C++ rocks", {"replacements": [("++", "pp")]}, "cpp-rocks"),
        # Unicode
        ("café", {}, "cafe"),
        ("Über cool", {}, "uber-cool"),
        # Edge cases
        ("", {}, ""),
        ("---", {}, ""),
        ("!!!###", {}, ""),
    ],
)
def test_compat(text: str, kwargs: dict[str, object], expected: str) -> None:
    assert slugify(text, **kwargs) == expected  # type: ignore[arg-type]


class TestLanguageCompat:
    """Language-specific transliteration compatibility."""

    def test_german_ue(self) -> None:
        assert slugify("Ü", lang="de") == "ue"

    def test_german_oe(self) -> None:
        assert slugify("ö", lang="de") == "oe"

    def test_german_ae(self) -> None:
        assert slugify("ä", lang="de") == "ae"

    def test_german_ss(self) -> None:
        assert slugify("ß", lang="de") == "ss"
