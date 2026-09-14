---
name: conduit-security-design
description: Design the security specification for each conduit between OT zones, covering protocol, direction, source and destination pairs, session limits, and the encryption or inspection decision. Use when hardening zone-to-zone communication paths.
version: 0.1.0
license: Apache-2.0
metadata:
  author: your-github-username
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0855
# allowed-tools: Read Grep Bash
---

## When to Use

- Specifying security controls for conduits defined in the zone design.
- Hardening an existing conduit found permissive during audit.
- Designing a new zone-to-zone flow before it is deployed.
- Producing the conduit register that firewall teams implement from.

## Prerequisites

- Zone and conduit design from `ot-network-segmentation-design` with the conduit list.
- Observed traffic baseline from `passive-ot-network-discovery` for each conduit.
- Protocol capability per conduit: which protocols support TLS, signing, or authentication natively.
- Firewall platform capability for the boundary device.
- Credentials: none. This skill produces documents.
- Authorization: security manager and network owner review the completed register.
- Upstream skills: `ot-network-segmentation-design` for the conduit list.

### Safety

This skill is passive. It produces design documents only.

## Workflow

1. Per conduit, record the traffic ground truth from the baseline: protocol, direction, source and destination pairs, session rate. A conduit spec that contradicts observed traffic will fail at implementation.
2. Flow direction decision. Requirement: sessions originate from the more trusted zone where the protocol allows it. Anchor: SR 5.2. Decision: controller responses to HMI polls are replies, not sessions. New-session initiation from L1 or L2 toward L3 is denied unless a named function requires it. Trade-off accepted: some legacy protocols need the controller to open the connection. Where that is true, the conduit documents the exception with its owner.
3. Source and destination pinning decision. Requirement: conduits carry explicit pairs, not subnets. Anchor: SR 5.2. Decision: per-host pairs where the host count is under 20, smallest usable subnets otherwise. Trade-off accepted: rule maintenance cost per host change versus a broad conduit that any compromised host can use.
4. Session limit decision. Requirement: each conduit states a session rate limit. Anchor: SR 7.1. Decision: limits sized from the baseline plus 25 percent headroom. Trade-off accepted: a legitimate burst above the limit drops traffic during process upsets. Size limits from upset-condition captures, not idle baselines.
5. Encryption versus inspection decision. Requirement: confidentiality and integrity on the conduit where the protocol supports it, visibility where it does not. Anchor: SR 3.1. Decision: protocols with native TLS or signing use it, for example OPC UA with Basic256Sha256. Protocols without it, Modbus and DNP3 commonly, stay cleartext inside OT zones and get inspection and pinning at the L3.5 boundary instead. Trade-off accepted: cleartext inside the zone is readable by anything in the zone. That is a zone compromise problem, not a conduit problem, and it is bounded by the zone design.
6. Inspection decision at the L3.5 boundary. Requirement: deep inspection where the platform supports the protocol. Anchor: SR 3.3. Decision: Modbus and DNP3 function-code filtering at the boundary. Trade-off accepted: inspection latency and platform cost. Do not proxy protocols the firewall dissects poorly; a broken proxy is worse than a filtered conduit.
7. Default deny statement. Requirement: the conduit register defines what is allowed. Anchor: SR 5.2. Decision: everything not in the register is denied. The register is the allow list. Trade-off accepted: new flows require a register change. That friction is the control.
8. Assemble `conduit-register.md` from `references/design-template.md`. One row per conduit, every column filled, every decision trade-off named.

## Verification

- Correct output: one register row per conduit from the zone design, each with pinned pairs, direction, session limits, and the encryption or inspection decision with its trade-off.
- Gap pattern: a register with any/any or whole-zone destination pairs. Pinning was skipped. A conduit specified as a whole zone is a permit between zones, not a conduit.
- Gap pattern: a register with no session limits. SR 7.1 has no design. A flood on an unlimited conduit crosses zones unchecked.
- Gap pattern: TLS mandated on Modbus. The decision in step 5 was not applied. Encryption on protocols that cannot carry it produces a broken design that implementers will quietly weaken.
- OT check: every register row matches observed traffic direction. A conduit designed for HMI-to-PLC polling that also carries PLC-initiated sessions is missing its exception row.
- OT check: safety conduit flows have the same or higher scrutiny than control flows. A register that hardens historian sync but leaves the SIS link unfiltered has its priorities inverted.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 5.2 | Zone boundary protection. Pinning, direction, and default deny. |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. Encryption and signing decisions per conduit. |
| IEC 62443-3-3 | SR 3.3 | Security functionality verification. Inspection placement where platforms support it. |
| IEC 62443-3-3 | SR 7.1 | Resilience against denial of service. Session limits per conduit. |
| NIST SP 800-82r3 | SC-7 | Boundary Protection. The register is the boundary allow list. |
| NIST SP 800-82r3 | SC-10 | Network Disconnect. Session limits and direction control. |
| NIST SP 800-82r3 | SC-8 | Transmission Confidentiality and Integrity. Encryption where the protocol supports it. |
| NIST SP 800-82r3 | AC-4 | Information Flow Enforcement. Flow direction and pair enforcement. |
| NIST CSF 2.0 | PR | Protect. Family level. Site assigns specific subcategories. |
| ATT&CK for ICS | T0855 | Unauthorized Command Message. Function-code filtering at the boundary blocks unauthorized commands. |

