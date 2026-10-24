---
name: ot-backup-and-recovery-design
description: Design backup and recovery for PLCs, HMIs, and historians with per-asset-class RTO and RPO targets, offline storage and air-gap strategy, and a restore test schedule. Use when designing how OT systems recover from compromise or failure.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-ARC-ot-backup-and-recovery-design
  author: comradezephyr
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0889
# allowed-tools: Read Grep Bash
---

## When to Use

- Designing backup coverage for a new OT network or asset class.
- Fixing a backup design after a restore test failed.
- Setting RTO and RPO targets per asset class with the operations manager.
- Designing the air-gap strategy after a ransomware assessment.

## Prerequisites

- Asset inventory by class: PLC logic, HMI images, historian archives, EWS images, network configs.
- Process tolerance per asset class: how long can the process run without this function.
- Current backup capability: what is backed up, where, and how fast it restores.
- Ransomware posture input from `ransomware-response-in-ot` if an assessment exists.
- Credentials: none. This skill produces documents.
- Authorization: operations manager accepts RTO and RPO targets. The budget owner accepts cost.
- Upstream skills: `passive-ot-network-discovery` for the asset inventory.

### Safety

This skill is passive. It produces design documents only.

## Workflow

1. Complete `references/questionnaire.md` with operations and the controls engineer. Every RTO and RPO target must trace to a stated process tolerance, not a guess.
2. Asset class decision. Requirement: backup design groups assets by recovery behavior, not by device. Anchor: CP-9. Decision: classes are PLC logic and configuration, HMI images and projects, historian archives, EWS images, and network device configs. Trade-off accepted: class-level design treats similar devices identically. A device that deviates needs its own row.
3. RTO and RPO decision per class. Requirement: recovery time and recovery point targets reflect process tolerance. Anchor: CP-10. Decision: targets set with the operations manager per class, for example PLC logic RTO 4 hours, RPO one shift. Trade-off accepted: tighter targets cost more in backup infrastructure and restore capacity. An RTO the budget cannot buy is a wish, not a target.
4. Storage location decision. Requirement: at least one recovery copy exists that ransomware on the production network cannot reach. Anchor: CP-9, SR 7.2. Decision: offline or air-gapped copy per class. Mechanism options: rotating offline media, tape with vaulting, or a backup network reachable only during backup windows. Trade-off accepted: offline copies restore slower and age faster. Rotation discipline becomes a manual process that fails without an owner.
5. Air-gap mechanism decision. Requirement: the air gap is enforced by architecture, not by policy. Anchor: SR 7.2. Decision: prefer pull-based backup from a separate backup network, or media rotation with documented custody. A backup target mounted on the production network is not air-gapped regardless of policy. Trade-off accepted: pull-based backup needs its own credentials and network, which is more infrastructure.
6. Restore test schedule decision. Requirement: backups are tested by restoring. Anchor: CP-10, SR 7.3. Decision: per class, a restore test at a stated interval on a bench or spare system, with a named owner and a recorded result. Trade-off accepted: restore tests consume engineering time and a spare controller. An untested backup is a hypothesis.
7. Integrity decision. Requirement: backups are verifiable. Anchor: SR 3.1, AU-9. Decision: hash every backup at creation and verify at test. Trade-off accepted: hash storage and verification time.
8. Assemble `backup-recovery-plan.md` from `references/design-template.md`. The asset class table is the core artifact. Every row states RTO, RPO, mechanism, and the accepted trade-off.

## Verification

- Correct output: every asset class from the inventory has a plan row with RTO, RPO, storage mechanism, air-gap mechanism, restore test interval, and named owner.
- Gap pattern: a plan with RTO or RPO targets that trace to no stated process tolerance. The numbers were copied from a template. Re-derive them with operations.
- Gap pattern: a plan where every backup lives on the production network. The air-gap decision was skipped. Ransomware encrypts the backup and the production copy at the same time.
- Gap pattern: a plan with no restore test schedule. CP-10 and SR 7.3 have no design. The first real restore is not a test.
- OT check: the PLC logic class captures logic, configuration, and the project files together. Logic without its project file restores into an unrecoverable state at the next change.
- OT check: the plan states what happens to safety system backups. SIS backups follow the safety engineer's change discipline, not the general schedule.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 7.2 | Control system backup. The backup design is the SR 7.2 implementation. |
| IEC 62443-3-3 | SR 7.3 | Control system recovery and reconstitution. The restore test schedule is the SR 7.3 design. |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. Backup hashing is the integrity check. |
| NIST SP 800-82r3 | CP-9 | System Backup. Asset class coverage and offline storage. |
| NIST SP 800-82r3 | CP-10 | System Recovery. RTO targets and restore testing. |
| NIST SP 800-82r3 | CP-2 | Business Continuity Plan. The plan feeds site continuity. |
| NIST SP 800-82r3 | AU-9 | Protection of Audit Information. Backup integrity and custody. |
| NIST CSF 2.0 | RC | Recover. Family level. Site assigns specific subcategories. |
| ATT&CK for ICS | T0889 | Modify Program. PLC logic backups are the recovery from a T0889 event. |


Row-by-row justification lives in `references/standards.md`.
