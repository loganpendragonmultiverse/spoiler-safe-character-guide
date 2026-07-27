from __future__ import annotations

import json
from typing import Any

PROJECT = "spoiler-safe-character-guide"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _character_guide(data: dict[str, Any]) -> dict[str, Any]:
    through = _require(data, "through")
    if not isinstance(through, int) or through < 0:
        raise ValueError("through must be a non-negative integer")
    characters = []
    for character in data.get("characters", []):
        facts = sorted(
            (
                fact
                for fact in character.get("facts", [])
                if isinstance(fact.get("milestone"), int) and fact["milestone"] <= through
            ),
            key=lambda fact: fact["milestone"],
        )
        characters.append({"name": character.get("name", "Unnamed"), "facts": facts})
    return {"through": through, "characters": characters}


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    return {"version": 1, "project": PROJECT, **_character_guide(data)}


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# {report['project'].replace('-', ' ').title()} report", ""]
    for key, value in report.items():
        if key not in {"version", "project"}:
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.append("")
            lines.append(f"```json\n{json.dumps(value, indent=2, ensure_ascii=False)}\n```")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
