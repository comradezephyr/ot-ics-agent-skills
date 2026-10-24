# Copyright 2026 comradezephyr
# SPDX-License-Identifier: Apache-2.0
"""Validate every skill under module/skills/."""

import sys
from collections import Counter
from pathlib import Path

from validate_skill import CATEGORY_NAMES, parse_frontmatter, split_frontmatter, validate


def skill_id(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return ""
    text = skill_md.read_text(encoding="utf-8").lstrip("\ufeff")
    front, _ = split_frontmatter(text)
    if front is None:
        return ""
    return parse_frontmatter(front).get("metadata", {}).get("skill_id", "")


def main():
    skills_root = Path(__file__).resolve().parent.parent / "module" / "skills"
    total = 0
    failed = 0
    seen = {}
    categories = Counter()
    for child in sorted(skills_root.iterdir()):
        if not child.is_dir() or child.name.startswith("_"):
            continue
        total += 1
        errors = validate(child)
        identifier = skill_id(child)
        if identifier:
            if identifier in seen:
                errors.append(
                    f"duplicate skill id {identifier!r}, also used by {seen[identifier]}"
                )
            seen[identifier] = child.name
            categories[identifier.split("-")[1]] += 1
        if errors:
            failed += 1
            for error in errors:
                print(f"FAIL: {child} -- {error}")
    for code in CATEGORY_NAMES:
        print(f"{CATEGORY_NAMES[code]}: {categories.get(code, 0)}")
    print(f"Validated {total} skills. {failed} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

