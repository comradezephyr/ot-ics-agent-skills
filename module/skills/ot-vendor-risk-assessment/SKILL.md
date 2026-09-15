---
name: ot-vendor-risk-assessment
description: Assess security risk of OT vendors and suppliers against defined dimensions with cited evidence, incident history measures, SBOM availability, remote access model, and contract clause mapping. Use when onboarding a vendor or refreshing third-party risk.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-GOV-ot-vendor-risk-assessment
  author: comradezephyr
  frameworks:
    - IEC 62443-2-4
    - NIST SP 800-161
    - NIST SP 800-82r3
# allowed-tools: Read Grep Bash
---

## When to Use

- Onboarding a new OT vendor, integrator, or service provider.
- Annual third-party risk refresh across the vendor estate.
- Reviewing a vendor after a security advisory names their product.
- Renewing a contract that lacks the required security clauses.

## Prerequisites

- Vendor list with product, service, and deployment footprint per site.
- Contract copies with clause numbering for vendors already engaged.
- Advisory data: vendor PSIRT pages, ICS-CERT advisories, NVD entries per product.
- Remote access design from `safe-remote-access-architecture` to score the access model against.
- Credentials: none. This skill produces assessment documents.
- Authorization: procurement and security manager accept the composite ratings and treatments.
- Upstream skills: `safe-remote-access-architecture`, `it-ot-convergence-risk-assessment`.

### Safety

This skill is passive. It produces assessment and governance documents only.

## Workflow

1. Complete `references/questionnaire.md` per vendor. Every score in the register must trace to an answer or an artifact.
2. Fix the dimension set and weights before scoring any vendor. Requirement: criteria are committed before results are known. Anchor: NIST SP 800-161 supply chain risk management. Dimensions: security program, incident history, patch cadence, SBOM availability, remote access model, contract clauses, long-term support. Default weights put remote access model and patch cadence highest because those two directly affect plant exposure. Trade-off accepted: pre-committed weights can fit a vendor poorly and force lower scores than the relationship deserves. A weight override is allowed only with the security manager's written sign-off recorded in the register.
3. Scoring rule. Requirement: every score cites a named artifact. Anchor: IEC 62443-2-4. Decision: each dimension scores 1 (lowest risk) through 5 (highest). No artifact means the dimension scores 5, not 3. Trade-off accepted: documentation-poor but well-run vendors score worse than they deserve, and vendors will dispute it. The alternative is scoring unassessed risk as acceptable, which is the outcome this assessment exists to prevent.
4. Incident history, measured not described. Requirement: the score derives from counts and intervals. Anchor: SA-9. Decision: record advisories naming the vendor product in the last 36 months, the median days from disclosure to patch, and the count of critical advisories still unpatched after 12 months. Thresholds: median over 180 days or any unpatched critical advisory older than 12 months scores 4 or higher regardless of vendor statements. Trade-off accepted: a vendor with many low-severity advisories scores worse than a vendor that discloses nothing. Disclosure is better behavior, and the register notes the disclosure posture separately so the count is read in context.
5. Patch cadence. Requirement: stated cadence compared against observed advisories. Anchor: SA-12. Decision: record the stated cadence from the vendor, then the observed intervals from step 4. A stated cadence with no observed advisories in 36 months is a maintenance posture question, not evidence of good cadence. Trade-off accepted: some mature products legitimately have no advisories. The register records "no recent advisories" as a fact and requires the vendor to state whether the product line is actively maintained.
6. SBOM availability. Requirement: the site can enumerate components in vendor products. Anchor: SA-12. Decision: machine-readable SBOM in SPDX or CycloneDX, including transitive dependencies, regenerated at each release. No machine-readable SBOM scores 4 minimum because component-level risk cannot be assessed by the site. Trade-off accepted: demanding SBOMs excludes smaller vendors who cannot produce them, and the site then decides between exclusion and accepting unassessable component risk.
7. Remote access model, scored against the remote access design. Requirement: the vendor's access model matches the site architecture. Anchor: 62443-2-4, SA-9. Decision: direct inbound tunnel to L3 or below scores 5. Shared vendor accounts score 4 minimum. Per-session grants with MFA, session recording, and source pinning score 1 or 2. Trade-off accepted: vendors with legacy access models score high and the remediation is a change project, not a contract clause.
8. Contract clause mapping. Requirement: security obligations are enforceable. Anchor: NIST SP 800-161, SA-9. Decision: map each required clause to its clause number in the contract: breach notification timeline, right to audit, patch support window and EOL notice, vulnerability disclosure obligation, SBOM delivery on request, subcontractor flow-down, and source or configuration escrow. For vendors already under contract that lack clauses, record compensating controls that hold until renewal. Trade-off accepted: mid-term contract changes are usually not enforceable, so the site accepts risk with compensating controls: per-session access approval, hash verification of every update, and no standing access. These controls cost operations effort per interaction.
9. Long-term support posture. Requirement: the site knows when support ends. Anchor: SA-9. Decision: record years the product line has been supported, last EOL announcement, and whether the vendor has a published support lifecycle. Trade-off accepted: assessing lifecycle shortens the usable life of some purchases and creates replacement cost pressure. The alternative is discovering EOL during an incident.
10. Composite rating and risk treatment. Requirement: every vendor gets a treatment, not a rating. Anchor: NIST SP 800-161. Decision: treatments are accept, mitigate with named compensating controls, transfer at contract renewal, or avoid by replacing or not purchasing. Trade-off accepted: avoiding a vendor costs an integration project. The register states the cost so the decision is made with numbers.
11. Assemble `vendor-risk-register.md` from `references/assessment-template.md`. Every dimension score cites an artifact. Every unknown is scored 5 with the reason recorded.

## Verification

- Correct output: every vendor has all seven dimensions scored, each with a cited artifact, and every vendor has a treatment with named controls or a stated avoidance cost.
- Gap pattern: a register with no incident history column. The most predictive dimension was skipped because it requires looking up advisory IDs.
- Gap pattern: every vendor rated Medium. Uniform ratings mean the criteria were not applied. Real estates have vendors that score 1 and vendors that score 5.
- Gap pattern: a treatment column reading "monitor". Monitoring is not a treatment. The four treatments are accept, mitigate, transfer at renewal, and avoid.
- Gap pattern: contract clause mapping present only for new purchases. The risk sits with incumbent vendors holding live tunnels, not with the next purchase order.
- OT check: every vendor with a remote access model traces to an entry in the tunnel inventory. A vendor access model assessed without naming the actual tunnel is assessment by assumption.
- OT check: every vendor whose product sits at L1 or L2 has its advisory count recorded, not just its certifications. Certifications describe the development process. Advisories describe the deployed product.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-2-4 | service provider requirements | Vendor security program and remote access requirements per dimension. |
| NIST SP 800-161 | supply chain risk management | Family level. The dimension set, weights, and treatments. |
| NIST SP 800-82r3 | SA-9 | External Information System Services. Contract clause mapping and access model scoring. |
| NIST SP 800-82r3 | SA-12 | Supply Chain Protection. SBOM availability and patch cadence. |
| NIST SP 800-82r3 | RA-3 | Risk Assessment. Likelihood from advisory posture, impact from zone exposure. |
| ATT&CK for ICS | T0862 | Supply Chain Compromise. The threat this assessment reduces. |
