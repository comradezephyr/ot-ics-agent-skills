---
name: nerc-cip-compliance-check
description: Assess a site against applicable NERC CIP standards, producing a requirement-level compliance matrix with evidence sources and gap notes. Use when preparing for a CIP audit or determining applicability for on-site generation.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-GOV-nerc-cip-compliance-check
  author: your-github-username
  frameworks:
    - NERC CIP
    - NIST SP 800-82r3
# allowed-tools: Read Grep Bash
---

## When to Use

- Preparing for a NERC CIP audit or a self-certification.
- Determining CIP applicability for a site with on-site generation.
- Building the evidence register that supports an audit response.
- Reviewing a compliance program after a networking or control change.

## Prerequisites

- Registered entity status and functional registration per site.
- BES Cyber System categorization from the current CIP-002 assessment.
- Evidence pack: ESP diagrams, patch records, access lists, training records, recovery test results, supply chain procedures.
- Current NERC CIP standards version list from the NERC website or regional entity.
- Credentials: none. This skill produces assessment documents.
- Authorization: compliance manager owns the matrix. Legal or regulatory review is required before any external submission.
- Upstream skills: `passive-ot-network-discovery` for observed network reality, `ot-asset-ownership-governance` for ownership records.

### Safety

This skill is passive. It produces assessment and governance documents only.

## Workflow

1. Establish applicability before assessing anything. Requirement: scope is defined by registration and categorization, not by asset count. Anchor: CIP-002-5.1a. Decision: record registered entity status per site and the functional registration held. A site with no registration and no BES Cyber System has no CIP obligations, and the matrix says so explicitly rather than listing rows as not applicable. Trade-off accepted: narrow applicability determination reduces assessment cost and raises enforcement risk if the determination is wrong. The determination is documented so it can be defended.
2. Categorize BES Cyber Systems and their associated impact levels. Requirement: impact level drives which requirements apply. Anchor: CIP-002-5.1a R1. Decision: perform or obtain the categorization before requirement assessment. Impact level High, Medium, and Low carry different requirement sets, and a matrix that ignores impact level will show false gaps. Trade-off accepted: categorization is per-site effort and must be redone when the topology changes.
3. Confirm the current version of every standard before quoting a requirement. Requirement: the matrix cites the version in force. Decision: for each standard, record the version and its effective date from the current NERC published list. Where the applicable sub-requirement identifier cannot be confirmed from the current standard document, the row cites the standard number only and carries the note "sub-requirement needs verification against the current standard". Trade-off accepted: version verification is manual and slows the matrix. A matrix quoting a superseded version is worse than a slow one because audit responses cite it.
4. Build the requirement matrix. Requirement: one row per applicable requirement. Anchor: the standard set. Decision: rows cover CIP-002-5.1a (categorization), CIP-003 (security management controls), CIP-004 (personnel and training), CIP-005 (electronic security perimeter), CIP-006 (physical security), CIP-007-6 (systems security management, R1 through R5), CIP-008 (incident reporting and response), CIP-009 (recovery plans), CIP-010-3 (configuration change management and vulnerability assessment), CIP-011 (information protection), CIP-013 (supply chain risk management, R1 through R3), and CIP-014 (physical security of critical stations) where applicable. Trade-off accepted: the matrix is long and most rows are compliant. The length is the audit artifact.
5. Evidence rule. Requirement: every compliance state cites an artifact and a date. Decision: a requirement with no artifact is non-compliant, not unknown. Trade-off accepted: this makes internal reports look worse than the program may deserve when the evidence exists but was not filed. The alternative is a matrix that claims compliance the entity cannot demonstrate in an audit.
6. Compliance state definitions. Requirement: states mean the same thing to everyone reading them. Decision: compliant means the artifact proves the requirement is met as written, including the retention and cadence elements. Partial means some elements are met and others are not. Non-compliant means the requirement is not met or cannot be demonstrated. Not applicable means the requirement does not apply to this entity or impact level, with a written justification. Trade-off accepted: partial rows are reported as non-compliant in any external submission. Keeping partial visible internally shows progress. Reporting it as compliant would misrepresent the entity to the regulator.
7. Reality check against observed network state. Requirement: documented boundaries match actual traffic. Anchor: CIP-005 electronic security perimeter, SC-7. Decision: compare the documented perimeter and conduit list against observed flows from `passive-ot-network-discovery`. A flow crossing a documented boundary that the boundary does not permit is a gap even when every document is in order. Trade-off accepted: the reality check requires a capture window and can surface gaps the compliance program believed were closed. That is the point of running it before an audit rather than during one.
8. Assemble `nerc-cip-compliance-matrix.md` from `references/assessment-template.md`. Every row carries a state, an evidence reference, and an owner. The version table is complete before the matrix is considered done.

## Verification

- Correct output: every applicable requirement has a compliance state, an evidence source with a date, and a named owner. The standards version table lists a verified version per standard. Not applicable rows carry justifications.
- Gap pattern: a matrix with no evidence column, or a blank one. The states are assertions rather than demonstrations. An auditor treats every assertion as non-compliant.
- Gap pattern: every requirement marked compliant with no artifact dates. Blanket compliance with no dates means the evidence was never assembled.
- Gap pattern: not applicable rows without justifications, or not applicable used on the hard requirements such as patch management and access control. Overuse of not applicable is the most common finding pattern in self-certification.
- Gap pattern: a version column showing a superseded standard version. The matrix is quoting retired language.
- OT check: the electronic security perimeter in the documents matches observed traffic. A capture showing flows that cross an undocumented path is a perimeter gap regardless of the diagram.
- OT check: patch management evidence is per-device and dated, not a policy document. A PDF describing a patch process proves nothing about whether the controller was patched.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| NERC CIP | CIP-002-5.1a R1 | BES Cyber System categorization. Steps 1 and 2. |
| NERC CIP | CIP-007-6 R1 through R5 | Ports and services, patch management, malicious code prevention, event monitoring, access control. Step 4. |
| NERC CIP | CIP-010-3 R1 | Configuration change management. Step 4. |
| NERC CIP | CIP-013-1 R1 through R3 | Supply chain risk management. Step 4. |
| NERC CIP | CIP-005, CIP-006, CIP-008, CIP-009, CIP-011, CIP-014 | Perimeter, physical security, incident response, recovery, information protection. Step 4. |
| NIST SP 800-82r3 | SI-2 | Flaw Remediation. Maps to CIP-007-6 R2 patch management evidence. |
| NIST SP 800-82r3 | SC-7 | Boundary Protection. Maps to the electronic security perimeter reality check in step 7. |
| NIST SP 800-82r3 | IR-4 | Incident Handling. Maps to CIP-008 response planning. |
| NIST SP 800-82r3 | CP-9 | System Backup. Maps to CIP-009 recovery planning. |
| NIST SP 800-82r3 | CM-3 | Configuration Change Control. Maps to CIP-010-3 R1. |
| NIST SP 800-82r3 | RA-3 | Risk Assessment. Maps to the categorization basis in step 2. |
| NIST SP 800-82r3 | SA-9 | External Information System Services. Maps to CIP-013 vendor obligations. |
