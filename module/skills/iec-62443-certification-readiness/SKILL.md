---
name: iec-62443-certification-readiness
description: Prepare for IEC 62443 certification across the applicable parts, covering scope definition, prerequisite designs, per-part evidence registers, gap analysis, and certification body coordination. Use when planning product or system certification.
version: 0.1.0
license: Apache-2.0
metadata:
  author: your-github-username
  frameworks:
    - IEC 62443-2-4
    - IEC 62443-3-3
    - IEC 62443-4-1
    - IEC 62443-4-2
# allowed-tools: Read Grep Bash
---

## When to Use

- Planning certification for a product, component, system, or service.
- Responding to a customer requirement for a 62443 certificate.
- Preparing for a pre-assessment with a certification body.
- Deciding which parts to certify first.

## Prerequisites

- Product, component, or system definition with version and boundaries.
- Existing process documentation: development lifecycle, service delivery, incident handling.
- Zone and conduit design from `ot-network-segmentation-design` for system-level work.
- Component inventory with any existing certificates and their scope.
- Credentials: none. This skill produces assessment documents.
- Authorization: product management and security management accept the readiness decision and its cost.
- Upstream skills: `ot-network-segmentation-design` for 3-3 scope, `conduit-security-design` for system requirement evidence.

### Safety

This skill is passive. It produces assessment and governance documents only.

## Workflow

1. Define the certification scope precisely. Requirement: scope names the part, the target, and the version. Anchor: 62443-2-4, 62443-3-3, 62443-4-1, and 62443-4-2 as applicable. Decision: one scope statement per part, each naming the audited entity: the development process for 4-1, the component and its version for 4-2, the system and its zone boundary for 3-3, and the service delivery process for 2-4. Trade-off accepted: a narrow scope costs less and is faster, and it may not satisfy a customer whose requirement cites a wider scope. Confirm the customer's requirement wording before fixing scope rather than after.
2. Prerequisite check per part. Requirement: certification starts from designs and processes that exist. Decision: 3-3 requires the zone and conduit design, the SL-T targets, and the requirement allocation to system elements. 4-2 requires the component requirement mapping against the CR families. 4-1 requires a documented development lifecycle with the SM practices. 2-4 requires documented service delivery, personnel, and access processes. Trade-off accepted: building the prerequisites inside the certification project lengthens it substantially. Sites that start certification before the design exists end up certifying a design they then change, which invalidates the certificate.
3. Build the evidence register per part. Requirement: every requirement maps to evidence. Decision: for 4-1, rows against the SM practice families SM-1 through SM-13. For 4-2, rows against the CR families, CR 1.1 through CR 7.8. For 3-3, rows against the SR families for the target SL. For 2-4, rows against the service provider requirement families. Trade-off accepted: the register is large and most rows are already satisfied. The register is what the auditor works from.
4. Handle component certificates honestly. Requirement: component certification does not certify the system. Anchor: 62443-4-2, 62443-3-3. Decision: record each component certificate with its scope and the requirement it satisfies, then assess the system against 3-3 independently. Trade-off accepted: a system built entirely from certified components still requires system-level assessment, including the composition risks the component certificates do not cover. Claiming system compliance from component certificates is the most common misrepresentation in 62443 submissions.
5. Gap analysis per part. Requirement: gaps carry severity, owner, and remediation effort. Decision: severity High where the gap blocks certification, Medium where it requires rework before the audit, Low where it is a documentation improvement. Trade-off accepted: fixing High gaps before the audit delays the date. Submitting with open High gaps guarantees a non-certification outcome and the fee is spent.
6. Certification body coordination. Requirement: the body, its accreditation, and the audit format are known before scheduling. Decision: record the selected certification body, its accreditation status, the pre-assessment option and its cost, the audit format (remote, onsite, witness test for 4-2 components), and the remediation window between audit stages. Trade-off accepted: a pre-assessment costs money and time. It finds the gaps before the formal audit, when they are cheapest to fix. Self-assessing to the standard and booking the audit directly is faster until the first finding.
7. Readiness decision. Requirement: the readiness call is explicit. Decision: ready, ready with conditions named, or not ready. A not-ready decision is a project outcome, not a failure. Trade-off accepted: delaying certification to fix gaps slips the market commitment the certificate supports. The readiness report states the cost of both delays so the decision is made with numbers.
8. Assemble `iec-62443-cert-readiness.md` from `references/assessment-template.md`. The per-part readiness sections and the evidence register are the core artifacts.

## Verification

- Correct output: one readiness section per part in scope, an evidence register with named artifacts per requirement family, a gap analysis with severity and owner, and the certification body record.
- Gap pattern: a scope statement that names the part but not the audited target. A 4-1 certificate is for a development process, not for a product. A 4-2 certificate is for one component at one version.
- Gap pattern: a readiness report with no evidence register entries. The gap analysis without evidence rows is an opinion.
- Gap pattern: a system-level 3-3 claim built from component certificates with no composition assessment. The composition risks, for example requirement interactions between components, are what 3-3 audits.
- Gap pattern: no certification body named, or a body selected without recorded accreditation. The audit date means nothing without the body.
- OT check: for 3-3, the SL-T targets from the zone design are stated in the scope. A system assessed without an SL-T target cannot be certified at any level.
- OT check: for 2-4, the service delivery scope covers remote access into customer environments. A service provider certification that excludes remote access excludes the part that matters most.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-4-1 | SM-1 through SM-13 | Security management practices for the development lifecycle. Step 3. |
| IEC 62443-4-2 | CR 1.1 through CR 7.8 | Component requirement families. Step 3. |
| IEC 62443-3-3 | SR families at target SL | System requirement families for the target security level. Step 3. |
| IEC 62443-2-4 | service provider requirements | Service delivery, personnel, and access processes. Step 2. |
| IEC 62443-3-2 | zone and conduit design | Prerequisite for the 3-3 scope. Step 2. |

