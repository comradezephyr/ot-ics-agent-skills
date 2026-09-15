---
name: ot-asset-ownership-governance
description: Establish governance for OT asset ownership covering who owns each asset class, who approves changes, who reviews access, who signs off lifecycle decisions, and the escalation path for unowned assets. Use when accountability for OT assets is unclear or contested.
version: 0.1.0
license: Apache-2.0
metadata:
  author: your-github-username
  frameworks:
    - IEC 62443-2-1
    - NIST SP 800-82r3
# allowed-tools: Read Grep Bash
---

## When to Use

- Establishing asset ownership where no one is accountable per class.
- Resolving ownership disputes between IT and OT after a convergence project.
- Fixing a governance gap surfaced by an incident where no one could authorize action.
- Assigning lifecycle sign-off for aging or end-of-life assets.

## Prerequisites

- Asset inventory by class: controllers, HMIs, EWS, network devices, historians, DMZ services, SIS.
- Organization chart with named roles.
- The change management design, so ownership aligns with approval gates.
- Current access review process, if any.
- Credentials: none. This skill produces design documents.
- Authorization: an accountable executive signs the ownership matrix. Without one name at the top, ownership records are unenforceable.
- Upstream skills: `passive-ot-network-discovery` for the asset inventory, `ot-change-management-workflow` for approval alignment.

### Safety

This skill is passive. It produces assessment and governance documents only.

## Workflow

1. Ownership matrix decision. Requirement: every asset class has one named owner. Anchor: CM-8, 62443-2-1 4.3.2.2. Decision: owners are per class, not per device: controllers and their logic, HMIs, EWS, network devices, historians, DMZ services, and SIS. Each class names one operational owner and one security counterpart. Trade-off accepted: per-class ownership can disagree with per-site operations structures. The alternative is per-device ownership that scales to hundreds of rows and decays immediately.
2. Change approval alignment decision. Requirement: ownership matches the approval gates in the change workflow. Anchor: 4.3.2.2, CM-3. Decision: the owner of a class is the approver for that class in the change workflow. Where the change workflow names a different authority, one of the two documents changes. Trade-off accepted: aligning the two documents removes a whole class of who-approves disputes during incidents. The cost is that this design cannot be written without the change workflow design.
3. Access review decision. Requirement: someone reviews who can reach each asset class. Anchor: CM-8, IR-7 context. Decision: the security counterpart per class reviews access quarterly, with the review record naming assets checked and accounts removed. Trade-off accepted: quarterly reviews are recurring effort. The alternative is access drift, which is discovered during incidents.
4. Lifecycle sign-off decision. Requirement: end-of-life, replacement, and decommission decisions have a named sign-off. Anchor: 4.3.2.2. Decision: the class owner signs lifecycle decisions, with the safety engineer co-signing for anything with a safety function. Trade-off accepted: lifecycle sign-off inserts security into retirement decisions that were historically purely operational. The alternative is decommissioned systems that remain connected.
5. Unowned asset escalation decision. Requirement: assets without an owner have a defined resolution path. Anchor: CM-8. Decision: unowned assets route to the accountable executive after 30 days, and until resolved they are treated as untrusted for access and patching decisions. Trade-off accepted: treating unowned assets as untrusted can disrupt integrations nobody wants to claim. That pressure is what forces ownership to be assigned.
6. Dispute resolution decision. Requirement: ownership disputes have a resolver. Anchor: 4.3.2.2. Decision: IT-OT boundary disputes resolve to the accountable executive, who decides based on the consequence statement per zone rather than on which department has budget. Trade-off accepted: executive dispute resolution means the executive becomes a bottleneck for boundary disputes. Boundary disputes are the disputes that matter, so the bottleneck is acceptable.
7. Assemble `asset-ownership-governance.md` from `references/plan-template.md`. The ownership matrix and the escalation path are the core artifacts.

## Verification

- Correct output: every asset class has a named operational owner and security counterpart, change approval alignment is stated, and the escalation path for unowned assets is defined with a deadline.
- Gap pattern: an ownership matrix with departments instead of names. A department cannot approve a change at 03:00. Ownership is a named person per class.
- Gap pattern: ownership and change workflow naming different approvers for the same class. The alignment decision was skipped. The two documents will contradict each other during the first incident.
- Gap pattern: access reviews scheduled with no owner or no record format. A review that no one owns does not happen.
- OT check: SIS class ownership includes the safety engineer as a co-signer for lifecycle decisions. A safety system owned by an operations manager alone misses the safety function test discipline.
- OT check: the unowned-asset path defines what untrusted means operationally. Treating an unowned asset as untrusted without defining the access and patching consequences is a statement, not a control.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-2-1 | 4.3.2.2 | Roles and responsibilities. The ownership matrix and dispute resolution. |
| NIST SP 800-82r3 | CM-8 | System Component Inventory. The inventory that the ownership matrix covers. |
| NIST SP 800-82r3 | PM-1 | Information Security Program Plan. The governance document is the program artifact. |
| NIST SP 800-82r3 | CM-3 | Configuration Change Control. The approval alignment with the change workflow. |
| NIST SP 800-82r3 | CA-7 | Continuous Monitoring. The quarterly access review cadence. |
| NIST CSF 2.0 | GV.RR | Roles, Responsibilities, and Authorities. The ownership matrix is the GV.RR artifact. |

