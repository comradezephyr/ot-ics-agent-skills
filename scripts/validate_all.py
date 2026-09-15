# Copyright 2026 comradezephyr
# SPDX-License-Identifier: Apache-2.0
"""Validate every skill under module/skills/."""

import sys
from pathlib import Path

from validate_skill import validate


def main():
    skills_root = Path(__file__).resolve().parent.parent / "module" / "skills"
    total = 0
    failed = 0
    for child in sorted(skills_root.iterdir()):
        if not child.is_dir() or child.name.startswith("_"):
            continue
        total += 1
        errors = validate(child)
        if errors:
            failed += 1
            for error in errors:
                print(f"FAIL: {child} -- {error}")
    print(f"Validated {total} skills. {failed} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
