---
name: iec-62443-gap-assessment
description: Assess a zone against IEC 62443-3-3 system security requirements using a structured questionnaire and document review. Use when preparing a gap register for an OT zone before remediation planning.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-ASM-iec-62443-gap-assessment
  author: your-github-username
  frameworks:
    - IEC 62443-3-3
    - NIST CSF 2.0
# allowed-tools: Read Grep Bash
---

## When to Use

- Preparing a gap register for a zone before remediation planning.
- Responding to a request for a 62443-3-3 baseline.
- Pre-audit preparation against an integrator checklist.
- Feeding the zone and conduit audit with documented evidence.

## Prerequisites

- Zone list and membership from `purdue-model-zone-conduit-audit`, or an equivalent zone map.
- Evidence pack: network diagrams, firewall rule sets, account lists, backup records, monitoring reports.
- Interview time with the zone owner and the control engineer. One hour per zone typical.
- Credentials: none.
- Authorization: site security manager sign-off to collect evidence.
- Upstream skills: `purdue-model-zone-conduit-audit` for zone scope.

### Safety

This skill is passive by default. Active steps are gated in the Workflow section.

- Passive. Document and questionnaire review. Sends no packets. Safe to run during normal operations.

## Workflow

1. Load the zone list and the evidence pack. Confirm every zone has a named owner.
2. Open `references/questionnaire.md`. Complete one question block per SR for each zone.
3. Record three fields per answer in `gap-register.md`: current state, target state, and the evidence artifact that proves the current state. Answers without evidence are gaps.
4. Decision point: an answer of partial with an evidence artifact is still a gap. Downgrade every partial to a gap until the evidence shows the full control in place.
5. Classify severity: High where a gap crosses a zone boundary or stops a process. Medium where it degrades audit or availability. Low where it affects documentation only.
6. Cross-check register rows against the evidence pack. Every High finding must name its evidence file. Missing evidence means the interview was incomplete. Reopen that row.
7. Produce `gap-register.md` with columns: SR, requirement, current state, target state, severity, evidence, owner, due date.

## Verification

- Correct output: every SR in `references/questionnaire.md` appears in `gap-register.md` exactly once, with all columns filled and a named owner.
- Failure mode: an SR row has no evidence artifact. The interview did not reach the evidence owner. Reopen the SR block.
- Failure mode: two zones produce identical registers. The questionnaire was copied, not completed. Re-interview per zone.
- OT check: every High finding references a control with an anchor in the zone conduit map. A finding with no zone anchor is out of scope.
- OT check: remediation due dates avoid production freeze windows. A due date inside a freeze is a scheduling error.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 1.1 | Identification and authentication of human users. Block A1. |
| IEC 62443-3-3 | SR 1.2 | Software process and device identification. Block A2. |
| IEC 62443-3-3 | SR 2.1 | Authorization enforcement. Block B1. |
| IEC 62443-3-3 | SR 2.8 | Auditable events. Block B2. |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. Block C1. |
| IEC 62443-3-3 | SR 3.3 | Security functionality verification. Block C2. |
| IEC 62443-3-3 | SR 4.1 | Information confidentiality. Block D1. |
| IEC 62443-3-3 | SR 4.3 | Use of cryptography. Block D2. |
| IEC 62443-3-3 | SR 5.1 | Network segmentation. Block E1. |
| IEC 62443-3-3 | SR 5.2 | Zoning. Block E2. |
| IEC 62443-3-3 | SR 5.4 | General purpose person-to-person communication restriction. Block E3. |
| IEC 62443-3-3 | SR 6.1 | Audit log accessibility. Block F1. |
| IEC 62443-3-3 | SR 6.2 | Continuous monitoring. Block F2. |
| IEC 62443-3-3 | SR 7.1 | Resilience against denial of service. Block G1. |
| IEC 62443-3-3 | SR 7.2 | Control system backup and recovery. Block G2. |
| IEC 62443-3-3 | SR 7.6 | Network and service availability. Block G3. |
| NIST CSF 2.0 | GV | Govern. Family level. Register owners are assigned in this workflow. |
