# slugsmith

[![CI](https://github.com/agentine/slugsmith/actions/workflows/ci.yml/badge.svg)](https://github.com/agentine/slugsmith/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/slugsmith)](https://pypi.org/project/slugsmith/)
[![Python](https://img.shields.io/pypi/pyversions/slugsmith)](https://pypi.org/project/slugsmith/)

Modern, zero-dependency Python library for generating URL-friendly slugs from Unicode text.

A drop-in replacement for [python-slugify](https://github.com/un33k/python-slugify) with built-in transliteration, no external dependencies, and full type annotations.

## Installation

```bash
pip install slugsmith
```

## Quick Start

```python
from slugsmith import slugify

slugify("Hello World")          # "hello-world"
slugify("café latte")           # "cafe-latte"
slugify("Ελληνικά")             # "ellinika"
slugify("Привет мир")           # "privet-mir"
slugify("北京")                  # "bei-jing"
```

## Features

- **Zero dependencies** — built-in Unicode→ASCII transliteration; no `text-unidecode` or `Unidecode` required
- **Drop-in replacement** for `python-slugify` — same `slugify()` signature
- **Language-aware** — language-specific mappings for German, Turkish, Polish, Czech, Finnish, Swedish
- **Type-safe** — full type annotations, PEP 561 compliant, passes mypy strict
- **MIT licensed** — no GPL dependency concerns

## API Reference

### `slugify(text, **options) -> str`

Generate a URL-friendly slug from `text`.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | *(required)* | Input string to slugify |
| `separator` | `str` | `"-"` | Character(s) between words |
| `lowercase` | `bool` | `True` | Convert to lowercase |
| `max_length` | `int` | `0` | Max slug length (0 = unlimited) |
| `word_boundary` | `bool` | `False` | Truncate at word boundary when `max_length` is set |
| `save_order` | `bool` | `False` | Accepted for python-slugify compatibility (word order is always preserved) |
| `stopwords` | `Iterable[str]` | `()` | Words to remove from the slug |
| `regex_pattern` | `str \| None` | `None` | Custom regex pattern for allowed characters |
| `replacements` | `Sequence[Sequence[str]] \| None` | `None` | Sequence of `(old, new)` pairs applied before transliteration; accepts lists of tuples or lists of lists |
| `allow_unicode` | `bool` | `False` | Keep Unicode characters in the slug |
| `lang` | `str \| None` | `None` | Language code for language-specific transliteration |

Returns an empty string if `text` is empty.

## Examples

### Separator and case

```python
slugify("Hello World", separator="_")           # "hello_world"
slugify("Hello World", lowercase=False)         # "Hello-World"
slugify("Hello World", separator="")            # "helloworld"
```

### Length limiting

```python
slugify("the quick brown fox", max_length=15)               # "the-quick-brow"
slugify("the quick brown fox", max_length=15, word_boundary=True)  # "the-quick"
```

### Stopwords

```python
slugify("the quick brown fox", stopwords=("the",))   # "quick-brown-fox"
```

### Replacements

```python
slugify("C++ is great", replacements=[("++", "pp")])  # "cpp-is-great"
slugify("$100 deal", replacements=[("$", "dollar")])   # "dollar100-deal"
```

### Unicode passthrough

```python
slugify("café au lait", allow_unicode=True)   # "café-au-lait"
slugify("北京 city", allow_unicode=True)       # "北京-city"
```

### Language-specific transliteration

```python
slugify("Ü-bung", lang="de")    # "ue-bung"   (German: ü→ue, ö→oe, ä→ae)
slugify("çalış", lang="tr")     # "calis"     (Turkish: ç→c, ş→s)
slugify("łódź", lang="pl")      # "lodz"      (Polish: ł→l, ó→o, ź→z)
slugify("říjen", lang="cs")     # "rijen"     (Czech: ř→r, í→i)
```

Supported language codes: `de` (German), `tr` (Turkish), `pl` (Polish), `cs` (Czech), `fi` (Finnish), `sv` (Swedish).

### Custom regex

```python
# Allow only alphanumeric and hyphens (strip underscores too)
slugify("hello_world foo", regex_pattern=r"[^a-z0-9-]")  # "helloworld-foo"
```

## Migration from python-slugify

slugsmith is a drop-in replacement:

```python
# Before
from slugify import slugify

# After
from slugsmith import slugify
```

The `slugify()` signature is identical. No other code changes are needed.

**Behavioural differences:**

| Feature | python-slugify | slugsmith |
|---------|---------------|-----------|
| Transliteration | `text-unidecode` (external dep) | Built-in table (zero deps) |
| License | MIT | MIT (no GPL risk) |
| Python support | 3.7+ | 3.9+ |
| Type annotations | Partial | Full (mypy strict) |
| Language-specific | Not built-in | `lang=` parameter |

## License

MIT
