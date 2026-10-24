<div align="center">

# OT/ICS Agent Skills

**Structured security runbooks for AI agents working in OT/ICS environments.**

![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Skills](https://img.shields.io/badge/skills-42-brightgreen)
![Frameworks](https://img.shields.io/badge/frameworks-IEC%2062443%20%7C%20NIST%20800--82%20%7C%20ATT%26CK%20ICS-orange)

</div>

A pack of structured runbooks for AI coding agents working in OT/ICS environments. It is for security engineers who assess, monitor, and respond to incidents on industrial networks. The runbooks replace loose prompt libraries with defined trigger conditions, exact commands, and verification steps. Safety gates sit inside every workflow so the agent does not act without approval and rollback planning.

## Why This Exists

Generic agents break in OT. They guess protocol commands. They fabricate tool output. They drop a PLC into program mode because the prompt was vague. OT safety constraints do not survive contact with an unstructured prompt.

This pack forces structure. Every skill has explicit trigger conditions, real commands, and verification steps. The agent works inside that track. Nothing executes until prerequisites and approval gates pass, and nothing is called done until the verification steps pass too.

These runbooks were assembled against IEC 62443-3-3, NIST SP 800-82 Rev. 3, and MITRE ATT&CK for ICS as those frameworks stood in early 2026. Framework versions change. Where a control or technique citation is load-bearing for a workflow, verify it against the current published version before relying on it.

## Quick Start

```sh
# Set HOST_DIR per host: ~/.cline/skills, ~/.claude/skills, or ~/.cursor/skills
HOST_DIR=~/.cline/skills
git clone https://github.com/comradezephyr/ot-ics-agent-skills.git
mkdir -p "$HOST_DIR"
cp -r ot-ics-agent-skills/module/skills/* "$HOST_DIR"
rm -rf "$HOST_DIR/_template"
cp ot-ics-agent-skills/module/AGENTS.md ./AGENTS.md
```

`_template` is the authoring scaffold, not a skill. Remove it after install so the host does not load a placeholder. `AGENTS.md` is the module-level context the agent reads alongside the runbooks, so it goes where your host reads agent instructions, usually the workspace root.

Path names are per host. Adjust `HOST_DIR` to whatever directory your host reads for agent skills.

On Windows, replace the copy steps with `Copy-Item -Recurse -Force .\module\skills\* $HOST_DIR` and `Remove-Item -Recurse -Force "$HOST_DIR\_template"` in PowerShell.

## What's Inside

| Category | Skills |
| --- | --- |
| Discovery and Inventory | 7 |
| Assessment and Audit | 7 |
| Monitoring and Detection | 7 |
| Incident Response | 7 |
| Architecture and Design | 7 |
| Compliance and Governance | 7 |

See the full list, up to date, in `module/AGENTS.md`.

Each skill ships `references/standards.md`, which expands every framework row with why it applies and which step it anchors. Skills that gather input or produce documents ship the matching template as well.

## Framework Coverage

- IEC 62443. Zones, conduits, and security levels SL1 through SL4.
- NIST SP 800-82 Rev. 3. ICS-specific control baselines.
- MITRE ATT&CK for ICS. Adversary technique mapping.
- Purdue Model. Placement of assets and traffic across levels L0 through L4/L5.
- NIST CSF 2.0. Govern, Identify, Protect, Detect, Respond, and Recover functions.

## Skill Format

```
module/skills/
  passive-ot-network-discovery/
    SKILL.md
    references/
      standards.md
      detection-rules.md
    scripts/
      ot_capture.py
```

`SKILL.md` is always present. It contains five sections in order: When to Use, Prerequisites, Workflow, Verification, Framework Mappings. Prerequisites carries a `### Safety` subsection that states whether the skill is passive or active.

`references/standards.md` is always present. It expands every row of the Framework Mappings table with why the control applies and which workflow step it anchors. Other reference files are optional and depend on the skill type: `questionnaire.md` for skills that gather input through questions, `design-template.md` and `assessment-template.md` for document production, `plan-template.md` for plans, `decision-matrix.md` for branching procedures, and `detection-rules.md` for rule sets.

`scripts/` is optional and holds the commands the runbook invokes. Every script runs against the libraries named in Prerequisites, with no pseudocode.

## Validation

```sh
python scripts/validate_all.py
```

The validator prints a count per category and `Validated 42 skills. 0 failed.`, and exits non-zero on any failure. It checks the frontmatter and metadata block, the five sections and their order, the Safety declaration and the STOP and SAFETY gates, every framework row against `references/standards.md`, every reference file against the runbook that must cite it, the writing rules, and that each bundled script parses. CI runs the same command on every push to `main` and on every pull request.

## Safety

Several skills take active steps against live systems. Those steps require change control approval before execution. Rollback verification is part of the workflow, not an afterthought.

Do not run active skills against production OT networks without a tested rollback plan and an approved maintenance window. Passive skills (network discovery, log review) are safe to run during normal operations. Active skills (scanning, config changes, isolation) are not.

Use these skills only on systems you are authorized to assess.

## Contributing

See `CONTRIBUTING.md` for how to add or improve a skill.

## License

Apache License 2.0. See `LICENSE`.
