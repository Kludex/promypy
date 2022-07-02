import inspect

import promypy


def test_smoke() -> None:
    assert inspect.ismodule(promypy)
