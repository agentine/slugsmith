"""Tests for the transliteration engine."""

from __future__ import annotations

import pytest
from slugsmith import slugify
from slugsmith.transliterate import transliterate


class TestTransliterateFunction:
    def test_ascii_passthrough(self) -> None:
        assert transliterate("hello") == "hello"

    def test_accented_latin(self) -> None:
        assert transliterate("café") == "cafe"

    def test_umlaut(self) -> None:
        assert transliterate("Über") == "Uber"

    def test_tilde(self) -> None:
        assert transliterate("señor") == "senor"

    def test_cedilla(self) -> None:
        assert transliterate("façade") == "facade"

    def test_scandinavian(self) -> None:
        assert transliterate("ø") == "o"
        assert transliterate("æ") == "ae"

    def test_sharp_s(self) -> None:
        assert transliterate("Straße") == "Strasse"


class TestCyrillic:
    def test_basic(self) -> None:
        result = transliterate("Привет")
        assert result == "Privet"

    def test_full_word(self) -> None:
        result = transliterate("Москва")
        assert result == "Moskva"

    def test_slugify_cyrillic(self) -> None:
        result = slugify("Привет мир")
        assert result.isascii()
        assert result == "privet-mir"


class TestGreek:
    def test_basic(self) -> None:
        result = transliterate("αβγ")
        assert result == "abg"

    def test_slugify_greek(self) -> None:
        result = slugify("αβγ")
        assert result.isascii()

    def test_accented_greek(self) -> None:
        # ά (U+03AC) decomposes to α + combining acute
        assert transliterate("Ελληνικά") == "Ellinika"

    @pytest.mark.parametrize(
        "char,expected",
        [
            ("ά", "a"),  # U+03AC -> α + accent
            ("έ", "e"),  # U+03AD -> ε + accent
            ("ή", "i"),  # U+03AE -> η + accent
            ("ί", "i"),  # U+03AF -> ι + accent
            ("ό", "o"),  # U+03CC -> ο + accent
            ("ύ", "y"),  # U+03CD -> υ + accent
            ("ώ", "o"),  # U+03CE -> ω + accent
        ],
    )
    def test_accented_greek_chars(self, char: str, expected: str) -> None:
        assert transliterate(char) == expected

    def test_slugify_accented_greek(self) -> None:
        assert slugify("Ελληνικά") == "ellinika"


class TestSymbols:
    def test_copyright(self) -> None:
        assert transliterate("©") == "c"

    def test_registered(self) -> None:
        assert transliterate("®") == "r"

    def test_trademark(self) -> None:
        assert transliterate("™") == "tm"

    def test_euro(self) -> None:
        assert transliterate("€") == "euro"

    def test_pound(self) -> None:
        assert transliterate("£") == "pound"


class TestSlugifyTransliteration:
    def test_german_umlaut(self) -> None:
        assert slugify("Über") == "uber"

    def test_cafe(self) -> None:
        assert slugify("café") == "cafe"

    def test_mixed_unicode_ascii(self) -> None:
        assert slugify("hello wörld") == "hello-world"

    @pytest.mark.parametrize(
        "input_text,expected",
        [
            ("résumé", "resume"),
            ("naïve", "naive"),
            ("piñata", "pinata"),
            ("El Niño", "el-nino"),
        ],
    )
    def test_common_accented(self, input_text: str, expected: str) -> None:
        assert slugify(input_text) == expected
