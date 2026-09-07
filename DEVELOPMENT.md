# Development contract

Generate character references limited to facts revealed through a chosen story milestone.

Preserve deterministic, source-safe behavior and the interpretation boundary documented in the README. Every feature release must update tests, version metadata, `CHANGELOG.md`, README claims and limitations, repository metadata, release assets, and the Forge catalog together.

## 1.1.0 improvement session

Validate character facts and introductions, gate aliases by milestone, and add a printable searchable HTML guide with boundary previews.

Each character may set `introduced_at` (default 0) and `aliases` as objects with name and milestone. Facts require text and a nonnegative integer milestone. Future character names, aliases and facts are omitted from every export; unsupported extra fields are also omitted. The HTML guide searches only visible content and can preview earlier boundaries up to the exported ceiling. It cannot reveal later material because that material is absent from the file. Use browser Print for a clean printable guide. Introduction boundaries and fact accuracy remain author-controlled.

Local formatting, lint, strict types and regression tests pass. Public release completion requires the protected CI/CodeQL matrix, tagged artifacts and matching Forge catalog/detail deployment.
