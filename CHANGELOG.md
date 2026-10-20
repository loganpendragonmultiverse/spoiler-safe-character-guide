# Changelog

## 1.3.0 - 2026-10-20

- Add a CLI export-boundary override without editing source data.
- Preserve exact HTML milestone boundaries above the JavaScript Number precision limit.
- Reject blank facts/aliases, create reports exclusively and ship authority docs/example.

## 1.2.1

- Correct released documentation labels; package behavior is unchanged.
- Preserve the original v1.2.0 tags and artifacts. This patch supplies corrected documentation in new artifacts.

## 1.2.0 - 2026-10-15

- Optional top-level `relationships` contains objects with `source`, `target`, `text`, and nonnegative integer `milestone`.

## 1.1.0 - 2026-09-07

- Validate character facts and introductions, gate aliases by milestone, and add a printable searchable HTML guide with boundary previews.
- Added regression coverage for the audited behavior and invalid inputs.

## 1.0.0 - 2026-07-26

- Released the first complete Spoiler-Safe Character Guide command-line workflow.
- Added deterministic JSON and Markdown reporting, representative examples, and cross-platform tests.
