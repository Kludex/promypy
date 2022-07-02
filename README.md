<h1 align="center">
    <strong>promypy</strong>
</h1>
<p align="center">
    <a href="https://github.com/Kludex/promypy" target="_blank">
        <img src="https://img.shields.io/github/last-commit/Kludex/promypy" alt="Latest Commit">
    </a>
        <img src="https://img.shields.io/github/workflow/status/Kludex/promypy/Test">
        <img src="https://img.shields.io/codecov/c/github/Kludex/promypy">
    <br />
    <a href="https://pypi.org/project/promypy" target="_blank">
        <img src="https://img.shields.io/pypi/v/promypy" alt="Package version">
    </a>
    <img src="https://img.shields.io/pypi/pyversions/promypy">
    <img src="https://img.shields.io/github/license/Kludex/promypy">
</p>

You've decided to add type annotation on the code source. What's your plan? 😅

This package is a small tool set to help you to achieve your dreamed fully type annotation project. 🚀

Using `mypy`, you'd probably add a [`files`](https://mypy.readthedocs.io/en/stable/config_file.html#confval-files)
entry on your configuration file, and each time someone on the team wants to include type annotation on that file,
you'd add on the `files` list. There are a some problems with this approach:

1. Each new file doesn't need to be added on the `files` list.
2. If a file gets fully type annotated, and you didn't even notice, it will not be added to the `files` list.

The `1.` is more important, as we don't want to have regressions on our goal to have our code source fully type annotated.
But you don't want to worry about `2.` as well...

What this package does:
- [`dump`](#dump): Generates a **list** of files that are currently not type annotated.
- [`check`](#check): Given an input of files:
  - If a file is in the **list**, and is fully type annotated, it will be removed from the **list**.
  - If a file is in the **list**, and is **not** fully annotated, it will be ignored.
  - If a file is **not** in the **list**, and is fully annotated, it will be ignored.
  - If a file is **not** in the **list**, and is **not** fully annotated, it will raise errors.

## Installation

As usual.

```bash
pip install promypy
```

## Usage

There are two commands available: `dump` and `check`.

### Dump

```bash
Usage: promypy dump [OPTIONS] FILES...

  Generate a list of files that are not fully type annotated.

Arguments:
  FILES...  [required]

Options:
  --mypy-args TEXT
  --output TEXT
  --help            Show this message and exit.
```

### Check

```bash
Usage: promypy check [OPTIONS] FILES...

  Check the given files with mypy, applying a set of custom rules.

Arguments:
  FILES...  [required]

Options:
  -f, --ignore-file PATH  [required]
  --mypy-args TEXT
  --help                  Show this message and exit.
```

## License

This project is licensed under the terms of the MIT license.
