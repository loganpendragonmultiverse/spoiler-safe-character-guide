# Spoiler-Safe Character Guide

[![CI](https://github.com/loganpendragonmultiverse/spoiler-safe-character-guide/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/spoiler-safe-character-guide/actions/workflows/ci.yml)

Generate character references limited to facts revealed through a chosen story milestone. The command runs locally, uses explicit UTF-8 JSON input, and produces deterministic JSON or Markdown reports without modifying the supplied source material.

## Three-minute start

```bash
python -m pip install .
spoiler-character-guide examples/sample.json
spoiler-character-guide examples/sample.json --format json --output report.json
```

The example documents the complete v1 input shape. Markdown is intended for immediate review; JSON preserves structured evidence for scripts and later comparison. An existing output file is never overwritten.

## Privacy and platforms

All character data stays local.

Python 3.10 or newer is supported on Windows, macOS, and Linux. The package has no runtime dependencies, telemetry, account, or hosted service.

## Interpretation boundary

Spoiler safety depends on accurate milestone numbering in the supplied source data; the tool does not infer canon or read manuscripts.

## Development

```bash
python -m pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy src
pytest
python -m build
```

The project is feature-complete for its documented v1 scope. Maintenance focuses on correctness, security, compatibility, and well-supported input improvements.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).

## Version 1.1.0: reviewed improvements

Validate character facts and introductions, gate aliases by milestone, and add a printable searchable HTML guide with boundary previews.

```bash
spoiler-character-guide examples/sample.json --format html --output guide.html
```

Each character may set `introduced_at` (default 0) and `aliases` as objects with name and milestone. Facts require text and a nonnegative integer milestone. Future character names, aliases and facts are omitted from every export; unsupported extra fields are also omitted. The HTML guide searches only visible content and can preview earlier boundaries up to the exported ceiling. It cannot reveal later material because that material is absent from the file. Use browser Print for a clean printable guide. Introduction boundaries and fact accuracy remain author-controlled.
