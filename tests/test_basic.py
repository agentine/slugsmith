"""Basic smoke tests for slugsmith."""

from slugsmith import slugify


def test_hello_world() -> None:
    assert slugify("hello world") == "hello-world"


def test_import_version() -> None:
    from slugsmith import __version__

    assert isinstance(__version__, str)
