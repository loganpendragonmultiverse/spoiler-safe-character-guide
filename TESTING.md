# Testing

Run `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build`. CI also audits dependencies and runs the supported OS/Python matrix.

## 1.1.0 regression acceptance

Run the complete existing suite plus the new regression fixtures. Confirm the documented command produces the selected output, malformed input remains actionable, and source files remain unchanged. Validate character facts and introductions, gate aliases by milestone, and add a printable searchable HTML guide with boundary previews.

## 1.2.0 acceptance

Exercise the optional input with the full regression suite, including validation, inclusive boundaries, deterministic ordering and legacy default behavior. Optional top-level `relationships` contains objects with `source`, `target`, `text`, and nonnegative integer `milestone`. Endpoints reference unique optional character `id` values. A relationship appears only at or after its own milestone and both introductions (inclusive). Exports contain visible endpoint names, never internal IDs or extra fields; HTML search and earlier-boundary previews use the same filtered relationship data. Authored text remains the author's responsibility. Omit `relationships` to retain the existing report shape.

## 1.3.0 acceptance

Run full lint, strict typing, coverage and builds. `tests/test_gold_review.py`
checks CLI overrides/source preservation, export parity, blank facts/aliases,
and exact serialized milestones above 2**53. Install wheel and sdist separately;
from outside the checkout run all tests against site-packages and all report
formats on the installed example. Confirm four installed document hashes. Browser
acceptance covers inclusive large-number boundaries, earlier previews, search,
ceiling clamps, malformed preview values, and absent future data in Chromium,
Firefox and WebKit at desktop/mobile widths. Retain the 90% coverage floor.

`tests/test_output_links.py` checks refusal of existing dangling-link metadata
on every platform and actual dangling symlinks where creation is supported.
