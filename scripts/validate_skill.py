# Copyright 2026 comradezephyr
# SPDX-License-Identifier: Apache-2.0
"""Validate the structure of a skill directory."""

import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9-]+$")
H2_SECTIONS = [
    "## When to Use",
    "## Prerequisites",
    "## Workflow",
    "## Verification",
    "## Framework Mappings",
]
OT_KEYWORDS = (
    "ot", "ics", "scada", "plc", "rtu", "hmi", "historian", "purdue",
    "modbus", "dnp3", "profinet", "ethernet/ip", "opc ua", "iec 62443",
    "sis", "safety instrumented",
)


def split_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return None, None


def parse_frontmatter(block):
    data = {}
    for line in block.splitlines():
        if not line.strip() or line[0] in (" ", "#"):
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip()
    return data


def validate(skill_dir):
    path = Path(skill_dir)
    skill_md = path / "SKILL.md"
    if not skill_md.is_file():
        return ["SKILL.md missing"]
    text = skill_md.read_text(encoding="utf-8").lstrip("\ufeff")
    front, body = split_frontmatter(text)
    if front is None:
        return ["frontmatter missing or malformed (top '---' markers required)"]
    data = parse_frontmatter(front)

    errors = []
    name = data.get("name", "")
    if not name:
        errors.append("missing required field 'name'")
    elif not NAME_RE.match(name):
        errors.append("field 'name' is not kebab-case (lowercase, digits, hyphens only)")
    elif name != path.name:
        errors.append(f"field 'name' {name!r} does not match directory name {path.name!r}")

    desc = data.get("description", "")
    if not 1 <= len(desc) <= 1024:
        errors.append("field 'description' must be 1 to 1024 characters")
    elif not any(kw in desc.lower() for kw in OT_KEYWORDS):
        errors.append("field 'description' lacks an OT trigger keyword")

    if not data.get("version"):
        errors.append("missing required field 'version'")

    sections = [line.strip() for line in body.splitlines() if line.startswith("## ")]
    if sections != H2_SECTIONS:
        errors.append(
            "body must have exactly five H2 sections in order: "
            "When to Use, Prerequisites, Workflow, Verification, Framework Mappings"
        )
    return errors


def main():
    if len(sys.argv) != 2:
        print("usage: python scripts/validate_skill.py path/to/skill-directory")
        return 2
    skill_dir = sys.argv[1]
    errors = validate(skill_dir)
    for error in errors:
        print(f"FAIL: {skill_dir} -- {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
