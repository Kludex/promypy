import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

import typer
from typer import Typer, echo

app = Typer()

FILE_PATTERN = re.compile(r"(.*)[^:]")


def run_mypy(args: List[str], capture_output: bool) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["MYPY_FORCE_COLOR"] = "1"
    command = ["mypy", *args]
    return subprocess.run(command, capture_output=capture_output, env=env, text=True)


@app.command()
def dump(files: List[str], args: Optional[str] = None, output: Optional[str] = None):
    filenames = set()
    splitted_args = shlex.split(args or "")
    all_args = list(files) + splitted_args
    result = run_mypy(all_args, capture_output=True)
    for line in result.stdout.split("\n"):
        match = re.match(r"^([^:]*).*", line)
        if ":" in line and match:
            file = match.group(1)
            filenames.add(file)

    output_filenames = "\n".join(filenames)
    fh = open(output, "w") if output else sys.stdout
    echo(output_filenames, file=fh)
    if fh is not sys.stdout:
        fh.close()


@app.command()
def check(
    files: List[str],
    ignore_file: Path = typer.Option(..., "--ignore-file", "-f"),
    args: Optional[str] = None,
):
    with ignore_file.open("r") as file:
        all_ignored_files = {line.strip() for line in file.readlines()}
    files_to_ignore = set(files) & all_ignored_files

    files_with_error = set()
    splitted_args = shlex.split(args or "")
    all_args = list(files) + splitted_args
    result = run_mypy(all_args, capture_output=True)
    output = []
    for line in result.stdout.split("\n"):
        match = re.match(r"^([^:]*).*", line)
        if ":" in line and match:
            file = match.group(1)
            files_with_error.add(file)
            if file not in files_to_ignore:
                output.append(line)

    files_to_remove = files_to_ignore - files_with_error
    ignored_files = all_ignored_files - files_to_remove

    # Remove input files from list
    with ignore_file.open("w") as file:
        file.write("\n".join(ignored_files))

    for line in output:
        echo(line)

    if len(output) == 0 and len(ignored_files) == 0:
        echo("This project is now fully type annotated! 🎉")
        raise typer.Exit(0)

    if len(output) == 0:
        echo("Success! 🚀")
        echo(f"{len(ignored_files)} files are still ignored.")
        raise typer.Exit(0)

    raise typer.Exit(result.returncode)


app()
