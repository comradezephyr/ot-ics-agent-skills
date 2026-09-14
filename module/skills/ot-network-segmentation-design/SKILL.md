---
name: ot-network-segmentation-design
description: Design zone and conduit boundaries for an OT network using Purdue levels and the IEC 62443 zone model, with per-zone SL-T targets and a conduit list. Use when designing or redesigning OT network segmentation.
version: 0.1.0
license: Apache-2.0
metadata:
  author: your-github-username
  frameworks:
    - IEC 62443-3-2
    - NIST SP 800-82r3
    - ATT&CK for ICS T0886
# allowed-tools: Read Grep Bash
---

## When to Use

- Designing segmentation for a new or expanded OT network.
- Redesigning zones after an audit found cross-level traffic.
- Setting SL-T targets per zone before a 62443-3-3 assessment.
- Producing the zone map that downstream design skills consume.

## Prerequisites

- Asset inventory from `passive-ot-network-discovery` or equivalent.
- Process flow requirements from the control engineer: which functions depend on which flows.
- Consequence-of-compromise statement per function: what happens if this zone is compromised.
- Maintenance and operational constraints that bound the design.
- Credentials: none. This skill produces documents.
- Authorization: operations manager and security manager review the completed design.
- Upstream skills: `passive-ot-network-discovery` for the asset baseline.

### Safety

This skill is passive. It produces design documents only.

## Workflow

1. Group assets into candidate zones by function and consequence. Criteria: assets sharing a process function, a failure mode, and a consequence-of-compromise class share a zone. Zone by function first, protocol second.
2. Place zones on Purdue levels. L1 controllers, L2 supervision, L3 site operations, L3.5 DMZ, L4 enterprise. A zone never spans two levels. A zone that wants to span levels is two zones with a conduit.
3. Set SL-T per zone. Requirement: IEC 62443-3-2 risk assessment per zone. Anchor: 62443-3-2 zone and conduit design. Criteria: SL-T equals the highest security level the consequence-of-compromise justifies. Safety-adjacent zones and zones reachable from L4 target SL3 or SL4. Isolated low-consequence zones may target SL2. Trade-off accepted: higher SL-T raises capital cost and engineering effort. An SL-T set by budget rather than consequence is not an SL-T.
4. Define the conduit list between zones. Requirement: every flow between zones crosses a documented conduit. Anchor: SR 5.1. Criteria: one row per flow with source zone, destination zone, protocol, direction, and business justification. A flow with no justification is removed, not documented.
5. Decision point: the L3.5 boundary. All L4-to-OT traffic terminates in L3.5. No conduit crosses L3.5 directly to L1 or L2. Trade-off accepted: services that used to reach controllers directly now need a broker or a store-and-forward design. The alternative is an enterprise-reachable controller.
6. Zone hardening statement per zone. Requirement: each zone records its enforcement mechanism. Anchor: SR 5.2. Criteria: firewall, switch ACL, or VLAN boundary named per zone with the rule count and the rule review owner.
7. Assemble `zone-conduit-design.md` from `references/design-template.md`. Every zone states its SL-T, consequence, and enforcement. Every conduit states its justification.

## Verification

- Correct output: every asset from the inventory appears in exactly one zone, every zone carries an SL-T with its consequence-of-compromise basis, and the conduit list has a justification per flow.
- Gap pattern: a zone map without SL-T targets is incomplete. IEC 62443-3-2 requires the target security level per zone. A map of VLANs is not a zone design.
- Gap pattern: two zones with identical consequence, function, and enforcement are one zone. Over-segmentation without consequence differences adds firewall administration cost for no security gain.
- Gap pattern: a conduit list where every flow is marked critical. If everything is critical, the consequence analysis was skipped. Real designs have flows the site can afford to lose.
- OT check: no conduit crosses L3.5 directly to L1 or L2. A design that includes one has failed the boundary decision in step 5 regardless of the rest of the document.
- OT check: safety systems sit in their own zone with their own SL-T. Safety functions inside a general control zone is a design defect, not a hardening issue.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-2 | zone and conduit design | The zone map, SL-T targets, and conduit list are the 62443-3-2 outputs. |
| IEC 62443-3-2 | risk assessment | The consequence-of-compromise basis per zone is the risk assessment input to SL-T. |
| IEC 62443-3-3 | SR 5.1 | Network segmentation. The zone and conduit structure. |
| IEC 62443-3-3 | SR 5.2 | Zone boundary protection. Enforcement named per zone. |
| IEC 62443-3-3 | SR 7.1 | Resilience against denial of service. Zone boundaries bound flood propagation. |
| NIST SP 800-82r3 | SC-7 | Boundary Protection. Conduit enforcement design. |
| NIST SP 800-82r3 | RA-2 | Security Categorization. The consequence-of-compromise classification per zone. |
| NIST CSF 2.0 | GV | Govern. Family level. Zone ownership and SL-T acceptance are governance decisions. |
| ATT&CK for ICS | T0886 | Remote Services. Segmentation bounds the reach of a compromised remote path. |

