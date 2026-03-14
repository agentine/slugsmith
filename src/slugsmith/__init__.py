"""Slugsmith — modern, zero-dependency URL slug generator."""

from slugsmith._version import __version__
from slugsmith.slugify import slugify

__all__ = ["slugify", "__version__"]
