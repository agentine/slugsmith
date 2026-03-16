# Slugsmith — Implementation Plan

## Overview

**Slugsmith** is a modern, self-contained Python library for generating URL-friendly slugs from Unicode text. It replaces **python-slugify** (62M/month downloads, single maintainer inactive since March 2024, stale dependency chain).

**PyPI name:** `slugsmith` (verified available)

## Target Library: python-slugify

- **Downloads:** 62M/month (2.4M/day)
- **Maintainer:** un33k (Val Neekman) — last code commit March 2024
- **Issues:** 4 open, 3 unmerged PRs, no review activity
- **Key risk:** Depends on `text-unidecode` (last release 2019, abandoned)
- **License concern:** Alternative dependency `Unidecode` is GPL; many projects cannot use it

## Architecture

### Core Module: `slugsmith/`

```
slugsmith/
├── __init__.py          # Public API: slugify()
├── slugify.py           # Core slugification logic
├── transliterate.py     # Built-in Unicode→ASCII transliteration (no external deps)
├── special.py           # Language-specific character mappings (German ü→ue, etc.)
├── py.typed             # PEP 561 marker
└── _version.py          # Version string
```

### Key Design Decisions

1. **Zero dependencies** — Built-in transliteration tables eliminate the need for text-unidecode or Unidecode. Ship comprehensive Unicode→ASCII mappings derived from CLDR/Unicode data (MIT-compatible sources only).

2. **API compatibility** — Provide a `slugify()` function with the same core parameters as python-slugify (`text`, `separator`, `lowercase`, `max_length`, `word_boundary`, `save_order`, `stopwords`, `regex_pattern`, `replacements`, `allow_unicode`). Easy migration path.

3. **Type-safe** — Full type annotations, PEP 561 compliant, passes mypy strict.

4. **Performance** — Optimize hot paths. Avoid unnecessary regex compilation on each call (pre-compile patterns). Target ≥2x throughput vs python-slugify.

5. **Modern Python** — Require Python 3.10+. Use modern string/regex features.

6. **MIT licensed** — Clear, permissive license with no GPL dependencies.

### Transliteration Strategy

- Ship a comprehensive mapping table covering Latin Extended, Cyrillic, Greek, CJK (basic), Arabic, Hebrew, Thai, and other major scripts.
- Source mappings from CLDR transliteration rules and Unicode NFKD decomposition.
- Support language-specific transliteration (e.g., German: ü→ue, ö→oe; Turkish: ı→i).
- Use `unicodedata.normalize('NFKD', ...)` as first pass, then apply custom mappings for characters that don't decompose cleanly.

## Deliverables

1. Core `slugify()` function with full parameter compatibility
2. Built-in transliteration engine (no external dependencies)
3. Language-specific character mappings
4. Comprehensive test suite (unit + property-based)
5. Migration guide from python-slugify
6. PyPI package published as `slugsmith`

## Non-Goals

- Django integration (users can wrap `slugify()` themselves)
- CLI tool (keep scope focused on the library)
- Python 2 or Python <3.9 support
