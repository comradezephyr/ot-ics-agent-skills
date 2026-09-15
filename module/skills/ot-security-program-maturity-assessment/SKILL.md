---
name: ot-security-program-maturity-assessment
description: Assess OT security program maturity against the C2M2 domains with MIL 0 through 3 per domain, producing per-domain scores, evidence, top gaps, and an improvement roadmap. Use when measuring program maturity or planning capability investment.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-GOV-ot-security-program-maturity-assessment
  author: comradezephyr
  frameworks:
    - C2M2
    - NIST SP 800-82r3
# allowed-tools: Read Grep Bash
---

## When to Use

- Measuring OT security program maturity before and after a capability investment.
- Comparing maturity across sites on one scale.
- Building an improvement roadmap with named gaps.
- Answering a customer or regulator maturity question with a standard model.

## Prerequisites

- Evidence pack: policies, procedures, training records, incident records, architecture documents, vendor registers.
- Interviews with the program owner, operations, engineering, and IT leads.
- Prior maturity assessment if one exists, for trend comparison.
- Credentials: none. This skill produces assessment documents.
- Authorization: program owner accepts the scores and the roadmap.
- Upstream skills: outputs from any prior assessment skills serve as evidence.

### Safety

This skill is passive. It produces assessment and governance documents only.

## Workflow

1. Score per domain at domain level. Requirement: the C2M2 model is scored by domain, and this skill does not invent practice-level identifiers. Anchor: C2M2 domains. Decision: the ten domains are Asset, Change, and Configuration Management; Identity and Access Management; Threat and Vulnerability Management; Risk Management; Situational Awareness; Event and Incident Response; Third-Party Risk Management; Workforce Management; Cybersecurity Architecture; and Cybersecurity Program Management. Trade-off accepted: domain-level scoring is coarser than practice-level scoring and takes a fraction of the time. Where a detailed C2M2 practice assessment exists, use it and note the score source in the report.
2. MIL definition. Requirement: the scale means the same thing per domain. Anchor: C2M2. Decision: MIL 0 means not performed. MIL 1 means performed ad hoc and undocumented. MIL 2 means performed and documented with a repeatable process. MIL 3 means reviewed, measured, and improved. Trade-off accepted: MIL 3 requires evidence of measurement and improvement, not just documentation. A program with good documents and no metrics is MIL 2, and writing it as MIL 3 because the documents exist is the most common inflation error in maturity assessments.
3. Evidence rule. Requirement: each domain score cites artifacts or interviews. Decision: MIL 2 and 3 claims require named documents or records. A domain with no evidence scores MIL 0 or 1, not 2. Trade-off accepted: this penalizes programs that do the work but do not write it down, and the remediation for those programs is documentation, which is cheap and worth naming.
4. OT-specific evidence check per domain. Requirement: OT evidence, not IT evidence. Decision: asset management evidence must name OT assets, access management evidence must cover HMIs and controllers, threat management evidence must name OT threat sources. An IT evidence pack does not prove OT maturity. Trade-off accepted: the check lengthens the assessment and is the reason the report is credible.
5. Identify the top gaps. Requirement: the report names the three domains furthest from target, with why. Anchor: the consequence statement per zone. Decision: gap priority derives from process consequence, not from the domain with the lowest score. A MIL 0 in a low-consequence domain is not the top gap. Trade-off accepted: consequence-weighted gap ranking means the roadmap does not read as a simple ascending score list.
6. Improvement roadmap. Requirement: each gap carries an action, an owner, and a re-assessment date. Decision: actions reference existing pack skills where one exists, for example backup design for a Threat and Vulnerability Management gap, rather than inventing new programs. Trade-off accepted: reusing the pack's designs gives faster closure than novel programs and may not match the site's internal program structure.
7. Assemble `c2m2-maturity-report.md` from `references/assessment-template.md`. The domain table and the gap register are the core artifacts.

## Verification

- Correct output: all ten C2M2 domains scored MIL 0 through 3 with cited evidence, top gaps ranked by consequence, and a roadmap with owners and dates.
- Gap pattern: a report with no MIL scores per domain. A narrative maturity summary is an opinion, not an assessment.
- Gap pattern: every domain at MIL 2 or 3 with no evidence artifacts. Uniform maturity means the interviews confirmed what people believe, not what exists.
- Gap pattern: gap priority matching score order exactly. Consequence weighting changes the order. A report where the ranking is just the sorted scores skipped the weighting step.
- Gap pattern: MIL 3 domains with documents but no metrics. MIL 3 is measured and improved. Documentation alone is MIL 2.
- OT check: the Identity and Access Management domain cites evidence covering controllers and HMIs, not just the enterprise directory. An access review of the IT estate does not measure OT access maturity.
- OT check: the Third-Party Risk Management domain cites the vendor register, with the remote access model dimension. A vendor maturity claim with no access model assessment is incomplete for OT.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| C2M2 | Asset, Change, and Configuration Management | Domain scored in step 1. Maps to CM-8 and CM-3 evidence. |
| C2M2 | Identity and Access Management | Domain scored in step 1. Maps to AC and IA evidence. |
| C2M2 | Threat and Vulnerability Management | Domain scored in step 1. Maps to SI-2 and RA-5 evidence. |
| C2M2 | Risk Management | Domain scored in step 1. Maps to RA-2 and RA-3 evidence. |
| C2M2 | Situational Awareness | Domain scored in step 1. Maps to SI-4 and AU-6 evidence. |
| C2M2 | Event and Incident Response | Domain scored in step 1. Maps to IR-4 and IR-5 evidence. |
| C2M2 | Third-Party Risk Management | Domain scored in step 1. Maps to SA-9 and SA-12 evidence. |
| C2M2 | Workforce Management | Domain scored in step 1. Maps to AT-2, AT-3, and PS evidence. |
| C2M2 | Cybersecurity Architecture | Domain scored in step 1. Maps to SC-7 and SR 5.1 design evidence. |
| C2M2 | Cybersecurity Program Management | Domain scored in step 1. Maps to PM family evidence. |
| NIST SP 800-82r3 | CM-8 | System Component Inventory. Evidence for the asset domain. |
| NIST SP 800-82r3 | SI-4 | System Monitoring. Evidence for the situational awareness domain. |
| NIST SP 800-82r3 | PM family | Program management evidence for the program domain. |
