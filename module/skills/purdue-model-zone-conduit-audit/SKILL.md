---
name: purdue-model-zone-conduit-audit
description: Audit zone and conduit definitions against the IEC 62443 zones and conduits model and Purdue level boundaries, using diagrams and captured flow data. Use when validating segmentation before a remediation program.
version: 0.1.0
license: Apache-2.0
metadata:
  author: your-github-username
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0886
# allowed-tools: Read Grep Bash
---

## When to Use

- Validating zone definitions before a remediation program.
- Reviewing segmentation after a network change.
- Auditing conduit protocols against the approved list.
- Pre-purchase review of a proposed L3.5 DMZ design.

## Prerequisites

- Zone map and conduit list from the site, or from `iec-62443-gap-assessment`.
- Network diagrams at L0 through L4.
- Flow data: `flows.csv` from `passive-ot-network-discovery`.
- Firewall and switch configs that enforce the boundaries.
- Credentials: none.
- Authorization: site security manager sign-off.
- Upstream skills: `passive-ot-network-discovery` for flow data.

### Safety

This skill is passive by default. Active steps are gated in the Workflow section.

- Passive. Document and flow analysis. Sends no packets. Safe to run during normal operations.

## Workflow

1. Load the zone map, diagram set, and `flows.csv`.
2. For each zone record: name, level (L0 through L4, L3.5), membership list, and the enforcement device for its boundary.
3. For each conduit record: endpoints, protocols, and purpose.
4. Decision point: a flow in `flows.csv` that matches no zone or conduit record is an undocumented conduit. It is a finding.
5. Check Purdue level separation:
   - No flow from L0 or L1 directly to L4.
   - No L3.5 to L1 conduit except through gateway devices.
   - The DMZ is the only path between L3 and L4.
   Each violation is a finding with the flow pair as evidence.
6. Check conduit protocol scope. A conduit carrying protocols outside its approved list is a finding.
7. Produce `zone-conduit-report.md` in three sections: zone map review, conduit review, violation list. Every violation names its evidence: a map row, a flow pair, or a config line.

## Verification

- Correct output: the report covers every zone and conduit in the map, and every flow in `flows.csv` resolves to a zone, a conduit, or a flagged undocumented path.
- Failure mode: a flow pair resolves to two conduits. The map is ambiguous. Re-open the map before scoring.
- Failure mode: the zone map lists a level with no membership. Empty zones usually indicate missing inventory, not real boundaries.
- OT check: every violation cites a flow pair with source and destination IP. A finding without a flow pair cannot be triaged.
- OT check: a DMZ conduit that carries remote desktop to L2 is flagged as a direct interactive path, not accepted as a conduit.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 5.1 | Network segmentation. The audit decides whether segmentation exists and holds. |
| IEC 62443-3-3 | SR 5.2 | Zoning. Zone membership and owner checks are this audit. |
| IEC 62443-4-2 | CR 5.2 | Zoning for components. Component boundary feeds the zone map. |
| ATT&CK for ICS | T0886 | Remote Services. Interactive remote desktop across zones is flagged in steps 5 and 7. |
| ATT&CK for ICS | T0842 | Network Sniffing. Flow baseline reuse shows new conduits from unauthorized behavior. |
| NIST SP 800-82r3 | SC-7 | Boundary protection. Enforcement device checks map to SC-7. |
| NIST CSF 2.0 | ID | Identify. Family level. Site assigns specific subcategories. |
