# Framework Mappings: historian-data-flow-mapping

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 5.1

Network segmentation.

Applies because step 6 places each historian at L3, or L3.5 when it fronts remote access. SR 5.1 requires segmentation to limit event effects. The flow map is the evidence that a given placement is correct. A historian with direct L1 flows fails the placement check.

### SR 7.6

Network and service availability.

Applies because step 5 requires each historian to receive sustained reads from its sources. SR 7.6 requires essential services to remain available. A collector with no observed sources has an availability problem, and the provider is the capture or the interface.

## NIST SP 800-82r3

### SC-7

Boundary protection.

Applies because step 7 flags any link that crosses zones in the wrong direction. SC-7 requires defined boundaries and enforcement. The flagged cross-zone links are the evidence an administrator must rule on. The skill flags. It does not change the network.

## ATT&CK for ICS

### T0811

Data from Information Repositories.

Applies as adversarial-model context. Historians are the Information Repository in the Purdue model. The flow map shows which hosts legitimately reach the repository, which is the baseline for spotting a T0811 exfiltration path. The mapping is traceability, not a step in an attack.

### T0882

Theft of Operational Information.

Applies as a detection mapping. Step 5 treats unexpected stream consumers as flag candidates. T0882 describes an adversary collecting operational data for theft. The consumer list is the detection input.

## NIST CSF 2.0

### ID (Identify)

Family level. The skill output is a historian and flow inventory. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.
