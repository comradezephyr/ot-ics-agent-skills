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

### Cline

```
git clone https://github.com/comradezephyr/ot-ics-agent-skills.git ot-ics-agent-skills
cp -r ot-ics-agent-skills/module/. ~/.cline/skills/
```

### Claude Code

```
git clone https://github.com/comradezephyr/ot-ics-agent-skills.git ot-ics-agent-skills
cp -r ot-ics-agent-skills/module/. ~/.claude/skills/
```

### Cursor

```
git clone https://github.com/comradezephyr/ot-ics-agent-skills.git ot-ics-agent-skills
cp -r ot-ics-agent-skills/module/. ~/.cursor/skills/
```

Path names are per host. Adjust `~/.cursor/skills/` to whatever directory your Cursor install reads for agent rules.

On Windows, replace `cp -r <src> <dst>` with `Copy-Item -Recurse -Force <src> <dst>` in PowerShell.

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
    scripts/
```

`SKILL.md` is always present. It contains five sections in order: When to Use, Prerequisites, Workflow, Verification, Framework Mappings. The `scripts/` directory is optional and holds any commands the runbook invokes.

## Safety

Several skills take active steps against live systems. Those steps require change control approval before execution. Rollback verification is part of the workflow, not an afterthought.

Do not run active skills against production OT networks without a tested rollback plan and an approved maintenance window. Passive skills (network discovery, log review) are safe to run during normal operations. Active skills (scanning, config changes, isolation) are not.

Use these skills only on systems you are authorized to assess.

## Contributing

See `CONTRIBUTING.md` for how to add or improve a skill.

## License

Apache License 2.0. See `LICENSE`.
