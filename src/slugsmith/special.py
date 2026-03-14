"""Language-specific character mappings."""

from __future__ import annotations

LANGUAGE_MAP: dict[str, dict[str, str]] = {
    "de": {  # German
        "\u00fc": "ue", "\u00f6": "oe", "\u00e4": "ae", "\u00df": "ss",
        "\u00dc": "Ue", "\u00d6": "Oe", "\u00c4": "Ae",
    },
    "tr": {  # Turkish
        "\u0131": "i", "\u0130": "I",
        "\u011f": "g", "\u011e": "G",
        "\u015f": "s", "\u015e": "S",
        "\u00e7": "c", "\u00c7": "C",
    },
    "pl": {  # Polish
        "\u0105": "a", "\u0104": "A",
        "\u0107": "c", "\u0106": "C",
        "\u0119": "e", "\u0118": "E",
        "\u0142": "l", "\u0141": "L",
        "\u0144": "n", "\u0143": "N",
        "\u00f3": "o", "\u00d3": "O",
        "\u015b": "s", "\u015a": "S",
        "\u017a": "z", "\u0179": "Z",
        "\u017c": "z", "\u017b": "Z",
    },
    "cs": {  # Czech
        "\u0159": "r", "\u0158": "R",
        "\u010d": "c", "\u010c": "C",
        "\u0161": "s", "\u0160": "S",
        "\u017e": "z", "\u017d": "Z",
        "\u016f": "u", "\u016e": "U",
        "\u010f": "d", "\u010e": "D",
        "\u0165": "t", "\u0164": "T",
        "\u0148": "n", "\u0147": "N",
        "\u011b": "e", "\u011a": "E",
    },
    "fi": {  # Finnish
        "\u00e4": "a", "\u00c4": "A",
        "\u00f6": "o", "\u00d6": "O",
    },
    "sv": {  # Swedish
        "\u00e5": "a", "\u00c5": "A",
        "\u00e4": "a", "\u00c4": "A",
        "\u00f6": "o", "\u00d6": "O",
    },
}


def apply_language(text: str, lang: str | None) -> str:
    """Apply language-specific character substitutions.

    If the language is not recognized, the text is returned unchanged.
    """
    if lang is None:
        return text
    mapping = LANGUAGE_MAP.get(lang)
    if mapping is None:
        return text
    for src, dst in mapping.items():
        text = text.replace(src, dst)
    return text
