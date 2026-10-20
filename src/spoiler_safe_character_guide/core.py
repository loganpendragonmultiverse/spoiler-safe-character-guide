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
    if not isinstance(through, int) or isinstance(through, bool) or through < 0:
        raise ValueError("through must be a non-negative integer")
    characters = []
    ids: dict[str, dict[str, Any]] = {}
    for character in (
        data.get("characters", []) if isinstance(data.get("characters", []), list) else []
    ):
        if isinstance(character, dict) and "id" in character:
            identifier = character["id"]
            if not isinstance(identifier, str) or not identifier.strip() or identifier in ids:
                raise ValueError("character ids must be unique nonempty text")
            ids[identifier] = character
    raw_characters = data.get("characters", [])
    if not isinstance(raw_characters, list):
        raise TypeError("characters must be an array")
    for index, character in enumerate(raw_characters):
        if (
            not isinstance(character, dict)
            or not isinstance(character.get("name"), str)
            or not character["name"].strip()
        ):
            raise ValueError(f"characters[{index}].name must be nonempty text")
        introduced = character.get("introduced_at", 0)
        if not isinstance(introduced, int) or isinstance(introduced, bool) or introduced < 0:
            raise ValueError(f"characters[{index}].introduced_at must be a nonnegative integer")
        facts = character.get("facts", [])
        aliases = character.get("aliases", [])
        if not isinstance(facts, list) or not isinstance(aliases, list):
            raise TypeError(f"characters[{index}].facts and aliases must be arrays")
        for group, items in (("facts", facts), ("aliases", aliases)):
            for j, item in enumerate(items):
                key = "text" if group == "facts" else "name"
                if not isinstance(item, dict) or not isinstance(item.get(key), str):
                    raise TypeError(f"characters[{index}].{group}[{j}].{key} must be text")
                if not item[key].strip():
                    raise ValueError(f"characters[{index}].{group}[{j}].{key} must not be blank")
                milestone = item.get("milestone")
                if not isinstance(milestone, int) or isinstance(milestone, bool) or milestone < 0:
                    raise ValueError(
                        f"characters[{index}].{group}[{j}].milestone must be a nonnegative integer"
                    )
        if introduced <= through:
            characters.append(
                {
                    "name": character["name"],
                    "introduced_at": introduced,
                    "facts": [
                        {"text": fact["text"], "milestone": fact["milestone"]}
                        for fact in sorted(facts, key=lambda fact: fact["milestone"])
                        if fact["milestone"] <= through
                    ],
                    "aliases": [
                        {"name": alias["name"], "milestone": alias["milestone"]}
                        for alias in aliases
                        if alias["milestone"] <= through
                    ],
                }
            )
    result: dict[str, Any] = {"through": through, "characters": characters}
    if "relationships" in data:
        relationships = data["relationships"]
        if not isinstance(relationships, list):
            raise TypeError("relationships must be an array")
        visible = []
        for relation in relationships:
            if not isinstance(relation, dict):
                raise TypeError("relationships must contain objects")
            if any(
                not isinstance(relation.get(key), str) or not relation[key].strip()
                for key in ("source", "target", "text")
            ):
                raise ValueError("relationships require source, target and text")
            if relation["source"] not in ids or relation["target"] not in ids:
                raise ValueError("relationship endpoints must reference character ids")
            milestone = relation.get("milestone")
            if not isinstance(milestone, int) or isinstance(milestone, bool) or milestone < 0:
                raise ValueError("relationship milestone must be a nonnegative integer")
            left, right = ids[relation["source"]], ids[relation["target"]]
            revealed = max(milestone, left.get("introduced_at", 0), right.get("introduced_at", 0))
            if revealed <= through:
                visible.append(
                    {
                        "source": left["name"],
                        "target": right["name"],
                        "text": relation["text"],
                        "milestone": revealed,
                    }
                )
        result["relationships"] = visible
    return result


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise TypeError("input must be a JSON object")
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
