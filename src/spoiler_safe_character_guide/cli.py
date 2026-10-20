from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import analyze, render_json, render_markdown
from .preview import render_html


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a deterministic, reviewable report from explicit JSON input."
    )
    parser.add_argument("input", type=Path, help="UTF-8 JSON input file")
    parser.add_argument("--format", choices=("markdown", "json", "html"), default="markdown")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--through", type=int, help="Export through this nonnegative milestone")
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        if args.through is not None:
            if not isinstance(data, dict):
                raise TypeError("input must be a JSON object")
            data["through"] = args.through
        report = analyze(data)
        rendered = {"json": render_json, "markdown": render_markdown, "html": render_html}[
            args.format
        ](report)
        if args.output:
            if args.output.exists() or args.output.is_symlink():
                raise ValueError(f"output already exists: {args.output}")
            with args.output.open("x", encoding="utf-8", newline="") as handle:
                handle.write(rendered)
        else:
            sys.stdout.write(rendered)
    except (OSError, UnicodeError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0
