---
name: ot-change-management-workflow
description: Design a change management workflow for OT that maintains security controls, covering request fields, class-based approval gates, a security review step, mandatory rollback plans, and post-change verification. Use when designing how changes reach OT systems.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-ARC-ot-change-management-workflow
  author: your-github-username
  frameworks:
    - IEC 62443-2-1
    - NIST SP 800-82r3
    - ATT&CK for ICS T0889
# allowed-tools: Read Grep Bash
---

## When to Use

- Designing a change management workflow for a new OT network or site.
- Fixing a workflow after an unauthorized change reached production.
- Adding a security review step to an existing engineering change process.
- Aligning the change process with 62443-2-1 requirements.

## Prerequisites

- Asset classes from `ot-backup-and-recovery-design` or the inventory.
- Current change process: what exists, who approves what, where it breaks.
- Zone map from `ot-network-segmentation-design` for class-based routing.
- Backup capability from the recovery design, because rollback depends on it.
- Credentials: none. This skill produces documents.
- Authorization: operations manager owns the approval gates. The design must be accepted by operations, engineering, and security.
- Upstream skills: `ot-backup-and-recovery-design` for the rollback capability.

### Safety

This skill is passive. It produces design documents only.

## Workflow

1. Define change classes. Requirement: approval effort scales with process risk. Anchor: 62443-2-1 4.3.4.3. Decision: classes are controller logic, network and firewall, HMI and historian configuration, OS and platform patching, and safety system. Each class routes to its own gate set. Trade-off accepted: class routing adds classification overhead per request. A single approval path for all changes is either too slow for a firewall rule or too loose for a logic download.
2. Define the request fields. Requirement: the request carries what approvers need. Anchor: CM-3. Decision: fields are requester, asset and zone, change class, description, justification, rollback plan reference, backup reference, window requested, verification plan, and the vendor ticket if one exists. Trade-off accepted: form length versus approvals made without rollback information. A change with no rollback plan is not ready to approve.
3. Define the security review step. Requirement: changes that touch zone boundaries, accounts, or update channels get security review. Anchor: CM-4. Decision: security review is mandatory for network and firewall class, any request opening a new conduit, and any account change. Trade-off accepted: security review adds lead time, typically a day. Skipping it is how unauthorized conduits appear.
4. Define the approval gates. Requirement: the operations manager approves anything touching a running process. Anchor: 4.3.4.3. Decision: logic class requires operations manager plus controls engineer. Safety class requires the safety engineer as an additional gate. Network class requires operations manager plus security review. Trade-off accepted: two-person gates are slower. Single-person approval on logic changes concentrates too much authority in one schedule.
5. Define the rollback requirement. Requirement: every change carries a tested rollback. Anchor: CM-3, SR 7.2. Decision: the request references the backup it rolls back to, and the rollback is executed once on a bench or the previous change. Trade-off accepted: rollback validation effort per change. A rollback plan that has never run is a paragraph, not a plan.
6. Define the post-change verification step. Requirement: every change is verified against its stated intent. Anchor: CM-4. Decision: the verification plan from the request is executed after deployment and the result recorded. Logic changes get a hash comparison against the approved version. Trade-off accepted: verification effort per change. Unverified changes make the audit trail a list of claims.
7. Define the audit trail and retention. Requirement: the change record is auditable. Anchor: SR 2.8, AU-9. Decision: requests, approvals, verification results, and rollback records retain for at least three years or the site's regulatory requirement, whichever is longer. Trade-off accepted: storage and records management effort.
8. Define the emergency change path. Requirement: incidents need faster changes without dropping the controls. Anchor: IR-4. Decision: emergency changes require operations manager approval by voice plus a retroactive record within 24 hours, with the security review after the fact. Trade-off accepted: emergency changes bypass lead time, not accountability. The retroactive record is what keeps the bypass auditable.
9. Assemble `change-management-procedure.md` from `references/design-template.md`. The class-to-gate table is the core artifact.

## Verification

- Correct output: every change class routes to a named gate set, the request field list is complete, and the emergency path retains accountability.
- Gap pattern: a workflow where the security review is optional or "as needed". CM-4 has no design. Reviewers who are optional are reviewers who are skipped.
- Gap pattern: a workflow with no rollback requirement on the logic class. CM-3 and SR 7.2 have no design. A failed logic change with no rollback becomes an outage.
- Gap pattern: an emergency path with no retroactive record. The bypass becomes permanent. The 24 hour record is the control.
- OT check: the safety class route adds the safety engineer as a gate, not as a reviewer. Safety changes approved by the same authority as ordinary logic changes is a design defect.
- OT check: the verification step for logic class requires a hash comparison against the approved version, not an operator eyeball check. A hash check would have caught every unauthorized download in the incident record.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-2-1 | 4.3.4.3 | Change management. The class routing, gates, and verification are the 4.3.4.3 implementation. |
| IEC 62443-3-3 | SR 7.2 | Control system backup. The rollback requirement depends on the backup capability. |
| IEC 62443-3-3 | SR 2.8 | Auditable events. The change record is the audit trail of modifications. |
| NIST SP 800-82r3 | CM-3 | Configuration Change Control. Request fields, gates, and emergency path. |
| NIST SP 800-82r3 | CM-4 | Impact Analysis. The security review step. |
| NIST SP 800-82r3 | CM-5 | Access Restrictions for Change. Gate authority per class. |
| NIST SP 800-82r3 | IR-4 | Incident Handling. The emergency change path. |
| NIST CSF 2.0 | GV | Govern. Family level. Gate authority is a governance decision. |
| ATT&CK for ICS | T0889 | Modify Program. The hash verification step detects unauthorized program changes riding the change process. |

