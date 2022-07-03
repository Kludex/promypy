import os
import re
import shlex
import subprocess
import sys
from contextlib import ExitStack
from pathlib import Path
from typing import List, Optional, Set

import typer
from typer import Typer, echo

FILE_PATTERN = re.compile(r"^([^:]*.py).*")

app = Typer(
    help="Progressive type annotation without regression! 🚀", add_completion=False
)


def run_mypy(args: List[str], capture_output: bool) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["MYPY_FORCE_COLOR"] = "1"
    command = ["mypy", *args]
    return subprocess.run(command, capture_output=capture_output, env=env, text=True)


def write_to_file(file: Optional[str], filenames: Set[str]) -> None:
    """Write filenames to file or stdout.

    Args:
        file (Optional[str]): File to write to. If None, write to stdout.
        filenames (Set[str]): Filenames to write into the file.
    """
    output_filenames = "\n".join(sorted(filenames))
    with ExitStack() as stack:
        fh = stack.enter_context(open(file, "w")) if file else sys.stdout
        echo(output_filenames, file=fh)


@app.command()
def dump(
    files: List[str], mypy_args: Optional[str] = None, output: Optional[str] = None
) -> None:
    """Generate a list of files that are not fully type annotated."""
    filenames = set()
    args = shlex.split(mypy_args or "")

    result = run_mypy(files + args, capture_output=True)
    for line in result.stdout.split("\n"):
        match = re.match(FILE_PATTERN, line)
        if ":" in line and match:
            file = match.group(1)
            filenames.add(file)

    write_to_file(output, filenames)


@app.command(help="Check the given files with mypy, applying a set of custom rules.")
def check(
    files: List[str],
    ignore_file: Path = typer.Option(..., "--ignore-file", "-f"),
    mypy_args: Optional[str] = None,
) -> None:
    """Check the given files with mypy, applying a set of custom rules.

    Given the the input `files`, and the list of files in the `ignore_file`:
    - If a file is in the list, and is fully type annotated, it will be removed from the list.
    - If a file is in the list, and is not fully annotated, it will be ignored.
    - If a file is not in the list, and is fully annotated, it will be ignored.
    - If a file is not in the list, and is not fully annotated, it will raise errors.
    """
    with ignore_file.open("r") as file:
        all_ignored_files = {line.strip() for line in file.readlines()}
    files_to_ignore = set(files) & all_ignored_files

    files_with_error = set()
    args = shlex.split(mypy_args or "")
    result = run_mypy(files + args, capture_output=True)
    output = []
    for line in result.stdout.split("\n"):
        match = re.match(FILE_PATTERN, line)
        if ":" in line and match:
            filename = match.group(1)
            files_with_error.add(filename)
            if filename not in files_to_ignore:
                output.append(line)

    files_to_remove = files_to_ignore - files_with_error
    ignored_files = all_ignored_files - files_to_remove

    modify_ignored_files = all_ignored_files > ignored_files

    if modify_ignored_files and len(ignored_files) != 0:
        echo(f"{ignore_file} has been updated.")
        with ignore_file.open("w") as file:
            echo("\n".join(sorted(ignored_files)), file=file)

    for line in output:
        echo(line)

    if len(output) == 0 and len(ignored_files) == 0:
        echo("This project is now fully type annotated! 🎉")
        ignore_file.unlink()
        raise typer.Exit(1)

    if len(output) == 0:
        echo("Success! 🚀")
        echo(f"Number of files missing: {len(ignored_files)}.")
        raise typer.Exit(1 if modify_ignored_files else 0)

    raise typer.Exit(result.returncode)


if __name__ == "__main__":  # pragma: no cover
    app()
