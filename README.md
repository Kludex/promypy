<h1 align="center">
    <strong>progressive-mypy</strong>
</h1>
<p align="center">
    <a href="https://github.com/Kludex/progressive-mypy" target="_blank">
        <img src="https://img.shields.io/github/last-commit/Kludex/progressive-mypy" alt="Latest Commit">
    </a>
        <img src="https://img.shields.io/github/workflow/status/Kludex/progressive-mypy/Test">
        <img src="https://img.shields.io/codecov/c/github/Kludex/progressive-mypy">
    <br />
    <a href="https://pypi.org/project/progressive-mypy" target="_blank">
        <img src="https://img.shields.io/pypi/v/progressive-mypy" alt="Package version">
    </a>
    <img src="https://img.shields.io/pypi/pyversions/progressive-mypy">
    <img src="https://img.shields.io/github/license/Kludex/progressive-mypy">
</p>

This is a package made for improve type annotation coverage on big repositories.

What this package does:
- [`dump`](#dump): Generates a **list** of files that are currently not type annotated.
- [`check`](#check): Given an input of files:
  - If a file is in the **list**, and is fully type annotated, it will be removed from the **list**.
  - If a file is in the **list**, and is **not** fully annotated, it will be ignored.
  - If a file is **not** in the **list**, and is fully annotated, it will be ignored.
  - If a file is **not** in the **list**, and is **not** fully annotated, it will raise errors.

## Installation

```bash
pip install progressive-mypy
```

## Usage

### Dump

### Check

## License

This project is licensed under the terms of the MIT license.
