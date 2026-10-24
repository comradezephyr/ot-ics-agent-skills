---
name: nist-800-82-control-mapping
description: Map existing OT controls to NIST SP 800-82 Rev. 3 control families through a structured questionnaire and evidence review. Use when building a control coverage matrix for a plant or fleet.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-ASM-nist-800-82-control-mapping
  author: comradezephyr
  frameworks:
    - NIST SP 800-82r3
    - NIST CSF 2.0
# allowed-tools: Read Grep Bash
---

## When to Use

- Building the control coverage matrix for a plant or fleet.
- Pre-assessment review before a NIST-based audit.
- Comparing coverage across sites on one worksheet.
- Feeding the remediation backlog a family-level view.

## Prerequisites

- Evidence pack: policies, standards, device hardening guides, backup records, training logs, incident reports.
- Interview time with the site control owner. Two hours per site typical.
- Credentials: none.
- Authorization: site manager sign-off.
- Upstream skills: `iec-62443-gap-assessment` when the 62443 register feeds the matrix.

### Safety

This skill is passive by default. Active steps are gated in the Workflow section.

- Passive. Document and questionnaire review. Sends no packets. Safe to run during normal operations.

## Workflow

1. Load the evidence pack. Confirm one control owner per site.
2. Open `references/questionnaire.md`. Complete one block per control family: AC, AU, CA, CM, CP, IA, IR, MA, MP, PE, PL, PS, RA, SA, SC, SI.
3. Record per family: rating (Implemented, Partial, Absent), evidence pointer, family lead.
4. Decision point: a family rated Implemented with no evidence pointer is downgraded to Partial. Evidence is the rating, not the interview answer.
5. Where a specific 800-82 control applies, for example AC-2 account management, note the control ID in the family row. Family-wide coverage stays at family level.
6. Produce `control-coverage-matrix.md` with one row per family: family, rating, evidence, lead, open items.

## Verification

- Correct output: all 16 families appear once each in the matrix, each with a rating and an evidence pointer.
- Failure mode: a family is rated Partial with no open items listed. The rating is unsupported. Recomplete that block.
- Failure mode: two sites produce identical matrices. Evidence pointers diverge when interviews happen. Re-interview.
- OT check: OT-specific families (CM, CP, SA, SC) must cite OT artifacts. An IT policy cited for an OT control is a finding.
- OT check: every Partial row maps to at least one open item schedulable outside a freeze window.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| NIST SP 800-82r3 | AC | Access Control. Family level. Questionnaire block AC. |
| NIST SP 800-82r3 | AU | Audit and Accountability. Family level. Block AU. |
| NIST SP 800-82r3 | CA | Assessment, Authorization, and Monitoring. Family level. Block CA. |
| NIST SP 800-82r3 | CM | Configuration Management. Family level. Block CM. |
| NIST SP 800-82r3 | CP | Contingency Planning. Family level. Block CP. |
| NIST SP 800-82r3 | IA | Identification and Authentication. Family level. Block IA. |
| NIST SP 800-82r3 | IR | Incident Response. Family level. Block IR. |
| NIST SP 800-82r3 | MA | Maintenance. Family level. Block MA. |
| NIST SP 800-82r3 | MP | Media Protection. Family level. Block MP. |
| NIST SP 800-82r3 | PE | Physical and Environmental Protection. Family level. Block PE. |
| NIST SP 800-82r3 | PL | Planning. Family level. Block PL. |
| NIST SP 800-82r3 | PS | Personnel Security. Family level. Block PS. |
| NIST SP 800-82r3 | RA | Risk Assessment. Family level. Block RA. |
| NIST SP 800-82r3 | SA | System and Services Acquisition. Family level. Block SA. |
| NIST SP 800-82r3 | SC | System and Communications Protection. Family level. Block SC. |
| NIST SP 800-82r3 | SI | System and Information Integrity. Family level. Block SI. |
| NIST CSF 2.0 | GV | Govern. Family level. Matrix ownership and review cadence. |

Row-by-row justification lives in `references/standards.md`.
