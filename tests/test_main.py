from pathlib import Path
from typing import List

import pytest
from typer.testing import CliRunner

from promypy.main import app


@pytest.mark.parametrize(
    "content, expected",
    [
        pytest.param(["def func() -> float:", "    return 1.0"], "Running mypy..."),
        pytest.param(["def func() -> int:", "    return '1'"], "main.py"),
    ],
)
def test_dump(tmp_path: Path, content: List[str], expected: str) -> None:
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        with open("main.py", "w") as f:
            f.write("\n".join(content))

        result = runner.invoke(app, ["dump"])
        assert expected in result.stdout


def test_check_complete(tmp_path: Path) -> None:
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        with open(".mypyignore", "w") as f:
            f.write("main.py\n")

        with open("main.py", "w") as f:
            f.write("\n".join(["def func() -> float:", "    return 1.0"]))

        result = runner.invoke(app, ["check", "main.py", "-f", ".mypyignore"])
        assert not Path(".mypyignore").exists()
        assert result.stdout == "This project is now fully type annotated! 🎉\n"
        assert result.exit_code == 1


def test_check_mypy_issue_but_in_the_list(tmp_path: Path) -> None:
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        with open(".mypyignore", "w") as f:
            f.write("main.py\n")

        with open("main.py", "w") as f:
            f.write("\n".join(["def func() -> int:", "    return 1.0"]))

        result = runner.invoke(app, ["check", "main.py", "-f", ".mypyignore"])
        assert Path(".mypyignore").exists()
        assert result.stdout == "Success! 🚀\nNumber of files missing: 1.\n"
        assert result.exit_code == 0


def test_check_without_mypy_issue_not_in_the_list(tmp_path: Path) -> None:
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        with open(".mypyignore", "w") as f:
            f.write("another.py\n")

        with open("another.py", "w") as f:
            f.write("\n".join(["def func() -> int:", "    return 1.0"]))

        with open("main.py", "w") as f:
            f.write("\n".join(["def func() -> int:", "    return 1"]))

        result = runner.invoke(app, ["check", "main.py", "-f", ".mypyignore"])
        assert Path(".mypyignore").exists()
        assert result.stdout == "Success! 🚀\nNumber of files missing: 1.\n"
        assert result.exit_code == 0


def test_check_mypy_issues_but_not_in_the_list(tmp_path: Path) -> None:
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        with open(".mypyignore", "w") as f:
            f.write("main.py\n")

        with open("another.py", "w") as f:
            f.write("\n".join(["def func() -> int:", "    return 1.0"]))

        result = runner.invoke(app, ["check", "another.py", "-f", ".mypyignore"])
        assert Path(".mypyignore").exists()
        assert "another.py:2: error:" in result.stdout
        assert result.exit_code == 1


def test_check_update_ignore_file(tmp_path: Path) -> None:
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        with open(".mypyignore", "w") as f:
            f.write("\n".join(["main.py", "another.py"]))

        with open("main.py", "w") as f:
            f.write("\n".join(["def func() -> int:", "    return 1.0"]))

        with open("another.py", "w") as f:
            f.write("\n".join(["def func() -> int:", "    return 1"]))

        result = runner.invoke(
            app, ["check", "another.py", "main.py", "-f", ".mypyignore"]
        )
        assert Path(".mypyignore").exists()
        assert result.stdout == (
            ".mypyignore has been updated.\n"
            "Success! 🚀\n"
            "Number of files missing: 1.\n"
        )
        assert result.exit_code == 1
