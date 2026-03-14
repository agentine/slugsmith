# slugsmith

Modern, zero-dependency Python library for generating URL-friendly slugs from Unicode text.

A drop-in replacement for python-slugify with built-in transliteration, no external dependencies, and full type annotations.

## Installation

```bash
pip install slugsmith
```

## Usage

```python
from slugsmith import slugify

slugify("Hello World")  # "hello-world"
slugify("café latte")   # "cafe-latte"
```

## License

MIT
