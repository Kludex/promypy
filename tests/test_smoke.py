import inspect

import progressive_mypy


def test_smoke() -> None:
    assert inspect.ismodule(progressive_mypy)
