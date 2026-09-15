---
name: dmz-architecture-for-ot
description: Design the DMZ between IT and OT covering service placement, data diode or firewall decisions, jump hosts, historian replication, patch staging, and vendor access termination. Use when designing or auditing the L3.5 boundary.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-ARC-dmz-architecture-for-ot
  author: comradezephyr
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0886
# allowed-tools: Read Grep Bash
---

## When to Use

- Designing the DMZ for a new OT network or a segment redesign.
- Replacing direct IT-to-OT flows with brokered services.
- Deciding between a data diode and a firewall for a specific flow.
- Consolidating scattered boundary services into a defined L3.5.

## Prerequisites

- Zone and conduit design from `ot-network-segmentation-design`.
- List of flows crossing the IT-OT boundary today, from the discovery baseline.
- Data direction and value per flow: which way data flows and what the enterprise does with it.
- Budget envelope: diodes and unidirectional gateways cost more than firewall rules.
- Credentials: none. This skill produces documents.
- Authorization: operations manager and security manager review the completed design.
- Upstream skills: `ot-network-segmentation-design` for the zone map.

### Safety

This skill is passive. It produces design documents only.

## Workflow

1. Inventory every IT-to-OT flow. Requirement: the DMZ design covers all boundary traffic. Anchor: SR 5.1. Criteria: per flow, record data direction, source, destination, protocol, and the business function. Unnamed flows do not get DMZ services. They get denied.
2. Service placement decision. Requirement: every service that both IT and OT need lives in the DMZ, not in either network. Anchor: SR 5.2. Decision: historian replication target, patch staging server, antivirus signature distribution, file exchange, jump hosts, and vendor access termination all place in L3.5. Trade-off accepted: the DMZ becomes a high-value target with its own patching and monitoring obligations. A DMZ nobody patches is worse than the flows it replaced.
3. Data diode versus firewall decision, per flow. Requirement: confidentiality and integrity on the boundary. Anchor: SC-7, SC-8. Criteria: a one-way flow with high value and no return traffic justifies a diode, for example historian push to the enterprise. Bidirectional or low-value flows use firewalled conduits. Trade-off accepted: diodes cost orders of magnitude more than firewall rules and break flows that need return traffic. Firewalls cost little and enforce direction only as well as their operators.
4. Historian replication decision. Requirement: the enterprise gets process data without reaching into OT. Anchor: SR 5.2. Decision: a replication target historian in the DMZ receives one-way pushes from the L3 historian. Enterprise consumers read the DMZ copy, never the L3 source. Trade-off accepted: the enterprise sees a delayed copy and cannot query live tags. Storage in the DMZ duplicates the historian footprint.
5. Jump host decision. Requirement: remote and enterprise administrative access to OT is brokered. Anchor: SR 5.2. Decision: jump hosts in the DMZ terminate sessions per the `safe-remote-access-architecture` design. Trade-off accepted: jump host availability is critical. Two jump hosts behind a load balancer.
6. Patch staging decision. Requirement: patches enter OT through a controlled path with verification. Anchor: CM-3, CM-5. Decision: a staging server in the DMZ receives vendor updates from IT, verifies hashes against vendor-published values, and serves them to OT through an approved pull. Trade-off accepted: update latency gains a staging step. The alternative is vendor update channels reaching into OT directly, which is the supply-chain compromise path.
7. Vendor access termination decision. Requirement: vendor remote access terminates in the DMZ. Anchor: AC-17. Decision: vendor tunnels terminate on DMZ infrastructure per the remote access design. Trade-off accepted: vendor session latency through the broker.
8. Directory and identity decision. Requirement: OT authentication does not depend on the enterprise domain. Anchor: IA-2. Decision: OT systems authenticate against OT-side identity services or local accounts replicated one-way into the DMZ. Trade-off accepted: duplicate identity administration versus an enterprise domain compromise that locks out the control room.
9. Assemble `dmz-architecture.md` from `references/design-template.md`. The service matrix is the core artifact. Every service row names its trade-off.

## Verification

- Correct output: the service matrix covers every boundary flow from step 1 with a placement decision, and every service row names its trade-off.
- Gap pattern: a DMZ design with no patch staging service. Updates will find another path into OT, usually the vendor tunnel, and the supply-chain control is lost.
- Gap pattern: a DMZ design where the DMZ hosts authenticate against the enterprise domain. The identity decision in step 8 was skipped. A domain compromise becomes a control room outage.
- Gap pattern: a diode specified for a bidirectional flow. The diode decision criteria in step 3 were not applied. Diodes break return traffic and the implementation will add a hidden second path.
- OT check: no DMZ service initiates sessions into L1 or L2. Brokers relay; they do not originate controller sessions. A DMZ service that polls controllers directly has become an undocumented L2 node.
- OT check: the DMZ has its own patching and monitoring cadence documented. A DMZ treated as a network closet accumulates the oldest vulnerable systems in the plant.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 5.1 | Network segmentation. The DMZ is the segmentation layer between IT and OT. |
| IEC 62443-3-3 | SR 5.2 | Zone boundary protection. Service placement and broker design enforce the boundary. |
| NIST SP 800-82r3 | SC-7 | Boundary Protection. Diode and firewall decisions per flow. |
| NIST SP 800-82r3 | SC-8 | Transmission Confidentiality and Integrity. One-way transfer designs for high-value flows. |
| NIST SP 800-82r3 | CM-3 | Configuration Change Control. Patch staging path design. |
| NIST SP 800-82r3 | CM-5 | Access Restrictions for Change. Verified hash pull into OT. |
| NIST SP 800-82r3 | AC-17 | Remote Access. Vendor and administrative access termination. |
| NIST SP 800-82r3 | IA-2 | Identification and Authentication. OT-side identity independence. |
| NIST CSF 2.0 | PR | Protect. Family level. Site assigns specific subcategories. |
| ATT&CK for ICS | T0886 | Remote Services. Brokered termination removes direct remote paths. |

