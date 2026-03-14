# Changelog

## [0.1.0] - 2026-03-14

### Added

- Initial release of slugsmith — modern, zero-dependency URL slug generator
- Built-in Unicode transliteration (no external deps) covering Latin, Greek, Cyrillic, and CJK scripts
- Language-specific character mappings (German ü→ue, ß→ss, etc.)
- Full `python-slugify`-compatible API (`slugify()` with `separator`, `max_length`, `word_boundary`, `stopwords`, `replacements`, `lowercase`, `truncate_chars` parameters)
- Strict type annotations throughout (PEP 561 `py.typed` marker)
- Comprehensive test suite (87 tests) covering edge cases and Unicode handling
- Python 3.9–3.13 support
