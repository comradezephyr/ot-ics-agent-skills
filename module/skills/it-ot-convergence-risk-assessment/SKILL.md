---
name: it-ot-convergence-risk-assessment
description: Assess risks from IT/OT convergence projects such as data lakes, cloud analytics, remote monitoring, and IoT sensors, producing a risk register with go or no-go criteria per path. Use when a convergence project proposes a new data or access path into OT.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-ARC-it-ot-convergence-risk-assessment
  author: comradezephyr
  frameworks:
    - IEC 62443-3-2
    - NIST SP 800-82r3
    - ATT&CK for ICS T0884
# allowed-tools: Read Grep Bash
---

## When to Use

- A convergence project proposes a data lake, cloud analytics platform, or remote monitoring service.
- IoT sensors are proposed for the OT network.
- An enterprise data initiative wants live OT data.
- Reviewing a convergence architecture before capital commitment.

## Prerequisites

- Proposed convergence architecture from the project: data flows, platforms, access paths.
- Zone and conduit design from `ot-network-segmentation-design`.
- DMZ design from `dmz-architecture-for-ot` or the current boundary state.
- Consequence-of-compromise statement per affected zone.
- Credentials: none. This skill produces documents.
- Authorization: security manager and operations manager jointly own the go or no-go decision.
- Upstream skills: `ot-network-segmentation-design`, `dmz-architecture-for-ot`.

### Safety

This skill is passive. It produces design documents only.

## Workflow

1. Complete `references/questionnaire.md` with the project team. Every risk in the register must trace to a stated architecture element.
2. Decompose the proposed architecture into data paths. Requirement: risk is assessed per path, not per project. Anchor: 62443-3-2 risk assessment. Criteria: one row per path with source zone, destination platform, direction, protocol, latency requirement, and data classification.
3. Classify each path against the zone design. Requirement: convergence paths do not create new direct crossings. Anchor: SR 5.1. Decision: a path that bypasses the L3.5 boundary is a redesign requirement, not an accepted risk. Trade-off accepted: routing through the DMZ adds latency and engineering cost. The alternative is a new enterprise-to-L3 path that outlives the project.
4. Risk per path. Requirement: likelihood and impact rated with named justification. Anchor: RA-2, RA-3. Decision: impact derives from the consequence-of-compromise statement of the source zone. Likelihood derives from the path's exposure: internet-reachable, partner-reachable, or internal. Trade-off accepted: qualitative ratings are coarse. They are sufficient for go or no-go and cheaper than quantitative analysis.
5. Common convergence risk patterns to evaluate per path:
   - Cloud analytics with outbound-only push from the DMZ: lowest risk if the push is one-way and the platform cannot reach back.
   - Data lake pulling from OT: converts a push into an enterprise-initiated pull, which reverses the boundary rule. Redesign to push or reject.
   - Remote monitoring SaaS: the vendor becomes a proxy into OT. T0884 pattern. Requires per-vendor tunnel and MFA design from the remote access architecture.
   - IoT sensors on the OT network: new unmanaged devices at L0 or L1. Requires device identity, network placement, and firmware update discipline before connection.
   - Unified IT-OT SIEM: log flows leave OT. Assess whether logs contain credentials or topology data worth protecting at the boundary.
6. Mitigation decision per risk. Requirement: every High risk carries a mitigation or a no-go. Anchor: SR 5.1. Decision: mitigations reuse the design skills, DMZ placement, conduit spec, remote access design. New control types are not invented per project. Trade-off accepted: reusing existing patterns slows novel architectures. Novel architectures also fail unpredictably, so the slowness is the control.
7. Go or no-go criteria per path. Requirement: the criteria are stated before the decision, not after. Anchor: 62443-3-2 risk assessment. Decision: per path, the conditions under which the project proceeds, for example "push-only through the DMZ with hash verification" as go, "enterprise-initiated pull from L3" as no-go pending redesign.
8. Assemble `convergence-risk-register.md` from `references/design-template.md`. Every risk row carries likelihood, impact, mitigation, and the go or no-go criterion.

## Verification

- Correct output: one register row per data path from step 2, each with rated likelihood and impact, a mitigation or no-go, and criteria stated before any decision.
- Gap pattern: a register that rates the project instead of its paths. Step 2 was skipped. A project has good paths and bad paths, and a project-level rating hides the bad ones.
- Gap pattern: High risks with mitigations that are "monitor closely". Monitoring is not a mitigation for a boundary violation. The mitigation must reference a design change.
- Gap pattern: go criteria written after the project was approved. The criteria exist to force the trade-off before commitment. Retroactive criteria are a record, not a control.
- OT check: every accepted path terminates at the DMZ and none creates a new direct L4-to-L3 or L3-to-L1 crossing. An accepted path that requires a new crossing has routed around the zone design.
- OT check: IoT sensor paths name their device identity and firmware update design. A sensor with no update path is unpatchable firmware attached to the control network.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-2 | risk assessment | The per-path risk rating is the 62443-3-2 risk assessment for the convergence scope. |
| IEC 62443-3-2 | zone and conduit design | Path classification against the zone design. |
| IEC 62443-3-3 | SR 5.1 | Network segmentation. The no-new-crossing decision. |
| IEC 62443-3-3 | SR 5.2 | Zone boundary protection. DMZ termination per path. |
| NIST SP 800-82r3 | RA-2 | Security Categorization. Impact derived from consequence of compromise. |
| NIST SP 800-82r3 | RA-3 | Risk Assessment. The likelihood and impact method. |
| NIST SP 800-82r3 | RA-5 | Vulnerability Monitoring. IoT and platform vulnerability posture feeds likelihood. |
| NIST SP 800-82r3 | CA-2 | Control Assessments. The go or no-go criteria are assessment criteria. |
| NIST SP 800-82r3 | SC-7 | Boundary Protection. Path placement decisions. |
| NIST CSF 2.0 | ID | Identify. Family level. Site assigns specific subcategories. |
| ATT&CK for ICS | T0884 | Connection Proxy. SaaS vendors and monitoring platforms become proxy paths into OT. |

