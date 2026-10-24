# Contributing

This repo accepts two kinds of contribution: new skills, and corrections to existing skills. A skill is a structured runbook under `module/skills/<skill-name>/` that an AI agent reads before acting on an OT security task. Corrections to existing skills follow the same rules as new skills: validated structure, real IDs, terse prose.

## Skill Requirements

Every skill must include:

- `SKILL.md`: the runbook. Starts with the YAML frontmatter (name, description, version, license, metadata with `skill_id` and `author`), then exactly five H2 sections in this order: When to Use, Prerequisites, Workflow, Verification, Framework Mappings. It cites `references/standards.md` and every other file that ships under `references/`.
- `references/standards.md`: expands every row of the Framework Mappings table with why it applies and to which step.
- Optional, depending on skill type:
  - `references/questionnaire.md` for skills that gather input through questions (assessments, reviews, plans).
  - `references/design-template.md` for skills that produce design or plan documents.
  - `references/decision-matrix.md` for skills with branching decisions (triage, response, forensics).
  - `references/detection-rules.md` for skills that produce IDS or SIEM rules.
- `scripts/`: only where the skill needs one. Scripts must be functional, use real library APIs, and run with the standard library or the libraries named in Prerequisites. No pseudocode.

A skill that does not fit one of these types still follows the five-section structure and the rules below. Read `module/skills/_template/SKILL.md` before writing anything.

## Skill Structure

```
module/skills/<skill-name>/
  SKILL.md
  references/
    standards.md
    questionnaire.md        # where input gathering is needed
    design-template.md      # for design and plan skills
    decision-matrix.md      # for branching procedures
    detection-rules.md      # for detection skills
  scripts/                  # only if the skill needs one
```

## Writing Guidelines

- Forbidden words: delve, landscape, leverage, robust, seamless, comprehensive, cutting-edge, game-changer, empower, unlock, harness.
- No em-dashes. Use commas or periods.
- No emojis.
- Terse technical prose. Short sentences. Assume the reader knows what Modbus and DNP3 are.
- Every Workflow step is a concrete action, not a description. "Run X against Y" is a step. "Ensure the configuration is correct" is not.
- Decision points state both paths with concrete criteria. "If the response code is 0x05, continue. If 0x0A, stop and report."
- Verification sections state what correct output looks like and at least two failure modes with what they indicate.
- Safety or design-phase skills state their nature in the Safety subsection. See Safety Rules below.

## Framework Mapping Discipline

- Real control and technique IDs only. Do not invent IDs.
- When unsure of an exact sub-identifier, use the family or standard level and add a note that the sub-ID needs verification against the current published document.
- Every mapping row states which workflow step it anchors and why.
- `references/standards.md` explains each row in more detail and carries the update rules: change `SKILL.md` and `standards.md` in the same change, and remove any mapping that cannot be verified from skill output.
- Where a publication uses practice areas instead of control IDs, for example NIST SP 800-161, cite the publication and say so explicitly.

## Validation

Run before opening a PR:

```
python scripts/validate_all.py
```

It must print `Validated N skills. 0 failed.` and exit 0, where N is the total skill count. The validator checks:

- `SKILL.md` presence and frontmatter: `license` is Apache-2.0, `version` is three-part, `name` matches the directory, and `description` is within 1024 characters with an OT trigger keyword.
- `metadata.author`, `metadata.skill_id`, and `metadata.frameworks`. The skill ID is canonical for the directory and unique across the pack.
- The five H2 sections in order, and the `### Safety` subsection with an active or passive declaration. Design and governance skills must use their exact sentence. Incident response skills must carry a SAFETY gate, and active skills must carry a STOP gate.
- `references/standards.md` with `## Update Rules`, every Framework Mappings row expanded in it, and every file under `references/` cited from `SKILL.md`.
- Writing rules on every markdown file: no em dashes, no banned words, no emojis, no CRLF, no trailing whitespace, no byte order mark.
- Every bundled Python script compiles and every shell script passes `sh -n`.

CI runs `python scripts/validate_all.py` from `.github/workflows/validate.yml` on every push to `main` and on every pull request, and rejects PRs that fail it. Fix the validator output before requesting review. Do not modify the validator to make a skill pass.

## Safety Rules

Three conventions, by skill type:

- Active skills that touch live OT systems carry a STOP gate blockquote above every step that changes or queries a live device:
  > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
- Incident response skills carry this blockquote at the top of the Workflow, before any active step:
  > SAFETY: If at any point the action risks human safety or process integrity, halt and escalate to the operations lead before continuing.
- Design and governance skills are document production only. The Safety subsection reads exactly: "This skill is passive. It produces design documents only." or "This skill is passive. It produces assessment and governance documents only."

In OT, process continuity outranks evidence, and human safety outranks both. Every response skill names a decision authority, and it is the operations manager, not the CISO.

## Commit Guidelines

- Small commits. One skill per commit at most, or one correction per commit.
- Vary commit messages to describe what changed. Do not repeat one message across a series.
- Do not open one giant commit with several skills or with a skill plus unrelated changes. Large commits do not review well and cannot be reverted cleanly.
- Do not commit generated files, validator cache, or editor artifacts.

## Review Process

A maintainer checks, in order:

1. Validator passes on the branch.
2. Structure matches the template: frontmatter, five H2 sections in order, named Safety convention for the skill type.
3. Framework mappings are real IDs, and `standards.md` traces every row to a step.
4. Workflow steps are concrete actions. Descriptions get sent back.
5. Writing guidelines hold: no banned words, no em-dashes, terse prose.
6. For active skills: every live-system step carries a STOP gate, and the skill names its decision authority.
7. For detection skills: rules use real syntax and layered protocols anchor on the outer header first.
8. Scripts compile and use real APIs.
9. Tone reads as written by a working OT engineer, not generated.

Corrections to existing skills need points 1, 5, and 6 for the touched sections only. Trivial corrections such as typo fixes need points 1 and 5.
