"""Core API tests for slugsmith.slugify."""

from __future__ import annotations

import pytest
from slugsmith import slugify


class TestBasicSlugify:
    def test_hello_world(self) -> None:
        assert slugify("Hello World") == "hello-world"

    def test_simple_ascii(self) -> None:
        assert slugify("foo bar baz") == "foo-bar-baz"

    def test_leading_trailing_whitespace(self) -> None:
        assert slugify("  hello world  ") == "hello-world"

    def test_multiple_spaces(self) -> None:
        assert slugify("hello   world") == "hello-world"

    def test_already_slug(self) -> None:
        assert slugify("already-a-slug") == "already-a-slug"

    def test_numbers(self) -> None:
        assert slugify("version 2.0") == "version-20"

    def test_mixed_case(self) -> None:
        assert slugify("CamelCaseText") == "camelcasetext"


class TestSeparator:
    def test_underscore(self) -> None:
        assert slugify("hello world", separator="_") == "hello_world"

    def test_dot(self) -> None:
        assert slugify("hello world", separator=".") == "hello.world"

    def test_empty_separator(self) -> None:
        assert slugify("hello world", separator="") == "helloworld"

    def test_tilde(self) -> None:
        assert slugify("hello world", separator="~") == "hello~world"


class TestLowercase:
    def test_no_lowercase(self) -> None:
        assert slugify("Hello World", lowercase=False) == "Hello-World"

    def test_lowercase_default(self) -> None:
        assert slugify("UPPER") == "upper"


class TestMaxLength:
    def test_max_length(self) -> None:
        assert slugify("hello world", max_length=5) == "hello"

    def test_max_length_zero_unlimited(self) -> None:
        result = slugify("hello world", max_length=0)
        assert result == "hello-world"

    def test_max_length_exact(self) -> None:
        assert slugify("hello world", max_length=11) == "hello-world"

    def test_max_length_longer_than_slug(self) -> None:
        assert slugify("hi", max_length=100) == "hi"


class TestWordBoundary:
    def test_word_boundary(self) -> None:
        assert slugify("hello world", max_length=8, word_boundary=True) == "hello"

    def test_word_boundary_exact_fit(self) -> None:
        result = slugify("hello world", max_length=11, word_boundary=True)
        assert result == "hello-world"

    def test_word_boundary_no_max(self) -> None:
        # word_boundary without max_length should not truncate
        assert slugify("hello world", word_boundary=True) == "hello-world"


class TestStopwords:
    def test_single_stopword(self) -> None:
        assert slugify("the quick brown fox", stopwords=("the",)) == "quick-brown-fox"

    def test_multiple_stopwords(self) -> None:
        result = slugify("the quick and brown fox", stopwords=("the", "and"))
        assert result == "quick-brown-fox"

    def test_no_stopwords(self) -> None:
        assert slugify("hello world", stopwords=()) == "hello-world"

    def test_all_stopwords(self) -> None:
        assert slugify("the a an", stopwords=("the", "a", "an")) == ""

    def test_stopwords_case_insensitive(self) -> None:
        assert slugify("The Quick", stopwords=("the",)) == "quick"


class TestReplacements:
    def test_cpp(self) -> None:
        assert slugify("C++ is great", replacements=[("++", "pp")]) == "cpp-is-great"

    def test_multiple_replacements(self) -> None:
        result = slugify("C# & .NET", replacements=[("#", "sharp"), ("&", "and"), (".", "dot")])
        assert result == "csharp-and-dotnet"

    def test_no_replacements(self) -> None:
        assert slugify("hello world", replacements=None) == "hello-world"


class TestAllowUnicode:
    def test_allow_unicode(self) -> None:
        result = slugify("héllo wörld", allow_unicode=True)
        assert "héllo" in result

    def test_unicode_stripped_by_default(self) -> None:
        result = slugify("héllo")
        assert "é" not in result
        assert result == "hello"


class TestRegexPattern:
    def test_custom_regex(self) -> None:
        # Remove digits
        result = slugify("hello123world", regex_pattern=r"[0-9]")
        assert result == "helloworld"


class TestEdgeCases:
    def test_empty_string(self) -> None:
        assert slugify("") == ""

    def test_only_special_chars(self) -> None:
        assert slugify("!!!###") == ""

    def test_only_whitespace(self) -> None:
        assert slugify("   ") == ""

    def test_single_word(self) -> None:
        assert slugify("hello") == "hello"

    def test_hyphens_in_input(self) -> None:
        assert slugify("hello-world") == "hello-world"

    def test_consecutive_separators(self) -> None:
        result = slugify("hello---world")
        assert result == "hello-world"


class TestLang:
    def test_german(self) -> None:
        assert slugify("Über", lang="de") == "ueber"

    def test_turkish(self) -> None:
        result = slugify("İstanbul", lang="tr")
        assert result == "istanbul"

    def test_unknown_lang(self) -> None:
        # Should fall through to default transliteration
        assert slugify("café", lang="xx") == "cafe"
