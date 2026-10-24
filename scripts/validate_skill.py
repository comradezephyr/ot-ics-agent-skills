# Copyright 2026 comradezephyr
# SPDX-License-Identifier: Apache-2.0
"""Validate the structure and content of a skill directory."""

import re
import subprocess
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9-]+$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
SKILL_ID_RE = re.compile(r"^otics-(DIS|ASM|MON|IRR|ARC|GOV)-([a-z0-9-]+)$")
H2_SECTIONS = [
    "## When to Use",
    "## Prerequisites",
    "## Workflow",
    "## Verification",
    "## Framework Mappings",
]
CATEGORY_NAMES = {
    "DIS": "Discovery and Inventory",
    "ASM": "Assessment and Audit",
    "MON": "Monitoring and Detection",
    "IRR": "Incident Response",
    "ARC": "Architecture and Design",
    "GOV": "Compliance and Governance",
}
OT_KEYWORDS = (
    "ot", "ics", "scada", "plc", "rtu", "hmi", "historian", "purdue",
    "modbus", "dnp3", "profinet", "ethernet/ip", "opc ua", "iec 62443",
    "sis", "safety instrumented",
)
BANNED_WORDS = (
    "delve", "landscape", "leverage", "robust", "seamless", "comprehensive",
    "cutting-edge", "game-changer", "empower", "unlock", "harness",
)
DESIGN_SAFETY = "This skill is passive. It produces design documents only."
GOVERNANCE_SAFETY = (
    "This skill is passive. It produces assessment and governance documents only."
)
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")
BANNED_RE = re.compile(r"\b(" + "|".join(re.escape(w) for w in BANNED_WORDS) + r")\b", re.I)


def split_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return None, None


def parse_frontmatter(block):
    """Parse flat keys plus the one-level metadata mapping and its list."""
    data = {"metadata": {}, "frameworks": []}
    section = None
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        if indent == 0:
            key, _, value = stripped.partition(":")
            section = key.strip() if not value.strip() else None
            data[key.strip()] = value.strip() if value.strip() else {}
        elif section == "metadata":
            if stripped.startswith("- "):
                data["frameworks"].append(stripped[2:].strip())
            else:
                key, _, value = stripped.partition(":")
                data["metadata"][key.strip()] = value.strip()
    return data


def section_text(body, heading):
    if heading not in body:
        return ""
    tail = body.split(heading, 1)[1]
    return tail.split("\n## ", 1)[0]


def mapping_rows(body):
    rows = []
    for line in section_text(body, "## Framework Mappings").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 3 or set(cells[0]) <= set("- "):
            continue
        if cells[0].lower() == "framework":
            continue
        rows.append(cells)
    return rows


def check_markdown(markdown, skill_dir, errors):
    text = markdown.read_text(encoding="utf-8")
    label = markdown.relative_to(skill_dir).as_posix()
    if text.startswith("\ufeff"):
        errors.append(f"{label}: starts with a byte order mark")
    if "\r\n" in text:
        errors.append(f"{label}: uses CRLF line endings")
    for number, line in enumerate(text.splitlines(), 1):
        if line.rstrip() != line:
            errors.append(f"{label}:{number}: trailing whitespace")
    if "\u2014" in text:
        errors.append(f"{label}: contains an em dash")
    match = BANNED_RE.search(text)
    if match:
        errors.append(f"{label}: contains banned word {match.group(0)!r}")
    if EMOJI_RE.search(text):
        errors.append(f"{label}: contains an emoji")


def check_scripts(skill_dir, errors):
    scripts = skill_dir / "scripts"
    if not scripts.is_dir():
        return
    for script in sorted(scripts.iterdir()):
        if not script.is_file():
            continue
        if script.suffix == ".py":
            try:
                compile(script.read_text(encoding="utf-8"), str(script), "exec")
            except SyntaxError as exc:
                errors.append(f"scripts/{script.name}: syntax error at line {exc.lineno}")
        elif script.suffix == ".sh":
            try:
                proc = subprocess.run(["sh", "-n", str(script)], capture_output=True, text=True)
            except FileNotFoundError:
                continue
            if proc.returncode != 0:
                errors.append(f"scripts/{script.name}: {proc.stderr.strip()}")


def validate(skill_dir):
    path = Path(skill_dir)
    errors = []
    skill_md = path / "SKILL.md"
    if not skill_md.is_file():
        return ["SKILL.md missing"]
    text = skill_md.read_text(encoding="utf-8").lstrip("\ufeff")
    front, body = split_frontmatter(text)
    if front is None:
        return ["frontmatter missing or malformed (top '---' markers required)"]
    data = parse_frontmatter(front)
    metadata = data.get("metadata", {})

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

    if not VERSION_RE.match(data.get("version", "")):
        errors.append("field 'version' must be a three-part number such as 0.1.0")

    if data.get("license") != "Apache-2.0":
        errors.append("field 'license' must be Apache-2.0")

    if not metadata.get("author"):
        errors.append("missing required field 'metadata.author'")

    skill_id = metadata.get("skill_id", "")
    category = None
    if not skill_id:
        errors.append("missing required field 'metadata.skill_id'")
    else:
        match = SKILL_ID_RE.match(skill_id)
        if not match:
            errors.append(
                "field 'metadata.skill_id' must look like otics-<CATEGORY>-<directory>"
            )
        else:
            category = match.group(1)
            if match.group(2) != path.name:
                errors.append(
                    "field 'metadata.skill_id' names "
                    f"{match.group(2)!r}, directory is {path.name!r}"
                )
            if skill_id != f"otics-{category}-{path.name}":
                errors.append("field 'metadata.skill_id' is not canonical")

    if not data.get("frameworks"):
        errors.append("missing required field 'metadata.frameworks'")

    sections = [line.strip() for line in body.splitlines() if line.startswith("## ")]
    if sections != H2_SECTIONS:
        errors.append(
            "body must have exactly five H2 sections in order: "
            "When to Use, Prerequisites, Workflow, Verification, Framework Mappings"
        )

    prerequisites = section_text(body, "## Prerequisites")
    if "### Safety" not in prerequisites:
        errors.append("Prerequisites must contain a '### Safety' subsection")
    safety = section_text(prerequisites, "### Safety")
    if "This skill is active" in safety:
        if "> STOP:" not in body:
            errors.append("active skill has no STOP gate")
    elif "This skill is passive" not in safety:
        errors.append("Safety must state whether the skill is active or passive")

    if category == "ARC" and DESIGN_SAFETY not in safety:
        errors.append(f"design skill Safety must read exactly: {DESIGN_SAFETY}")
    if category == "GOV" and GOVERNANCE_SAFETY not in safety:
        errors.append(f"governance skill Safety must read exactly: {GOVERNANCE_SAFETY}")
    if category == "IRR" and "> SAFETY:" not in body:
        errors.append("incident response skill has no SAFETY gate")

    standards = path / "references" / "standards.md"
    if not standards.is_file():
        errors.append("references/standards.md missing")
    else:
        standards_text = standards.read_text(encoding="utf-8")
        if "## Update Rules" not in standards_text:
            errors.append("references/standards.md has no '## Update Rules' section")
        rows = mapping_rows(body)
        if not rows:
            errors.append("Framework Mappings has no table rows")
        for row in rows:
            for control in [part.strip() for part in row[1].split(",") if part.strip()]:
                if control not in standards_text:
                    errors.append(
                        f"mapping row {control!r} is not expanded in references/standards.md"
                    )
            if len(row[2].split()) < 5:
                errors.append(
                    f"mapping row {row[1]!r} needs a relevance sentence, not a label"
                )

    references = path / "references"
    if references.is_dir():
        for reference in sorted(references.iterdir()):
            if reference.is_file() and f"references/{reference.name}" not in text:
                errors.append(f"references/{reference.name} is never referenced from SKILL.md")
    if "references/standards.md" not in text:
        errors.append("SKILL.md never points at references/standards.md")

    for markdown in sorted(path.rglob("*.md")):
        check_markdown(markdown, path, errors)
    check_scripts(path, errors)
    return errors


def main():
    if len(sys.argv) != 2:
        print("usage: python scripts/validate_skill.py path/to/skill-directory")
        return 2
    skill_dir = sys.argv[1]
    errors = validate(skill_dir)
    for error in errors:
        print(f"FAIL: {skill_dir} -- {error}")
    if not errors:
        print(f"OK: {skill_dir}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

