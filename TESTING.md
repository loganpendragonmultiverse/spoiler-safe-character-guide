# Testing

Run `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build`. CI also audits dependencies and runs the supported OS/Python matrix.

## 1.1.0 regression acceptance

Run the complete existing suite plus the new regression fixtures. Confirm the documented command produces the selected output, malformed input remains actionable, and source files remain unchanged. Validate character facts and introductions, gate aliases by milestone, and add a printable searchable HTML guide with boundary previews.

## 1.2.0 acceptance

Exercise the optional input with the full regression suite, including validation, inclusive boundaries, deterministic ordering and legacy default behavior. Optional top-level `relationships` contains objects with `source`, `target`, `text`, and nonnegative integer `milestone`. Endpoints reference unique optional character `id` values. A relationship appears only at or after its own milestone and both introductions (inclusive). Exports contain visible endpoint names, never internal IDs or extra fields; HTML search and earlier-boundary previews use the same filtered relationship data. Authored text remains the author's responsibility. Omit `relationships` to retain the existing report shape.
