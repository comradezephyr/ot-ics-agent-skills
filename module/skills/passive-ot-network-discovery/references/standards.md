# Framework Mappings: passive-ot-network-discovery

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 5.1

Network segmentation.

Applies because step 9 assigns every asset a segment placement at Purdue levels L0 through L3.5. SR 5.1 requires networks to be segmented to limit the effect of an event. The inventory is the input data for that segmentation. If the site already maintains a zone map, the inventory still validates it against observed traffic.

### SR 3.1

Communication integrity.

Applies because steps 5 and 6 record which function codes and which devices actually talk. SR 3.1 requires integrity protection for communications. The recorded baseline is what anomaly detection later compares against. This skill only observes. It does not protect. The mapping is traceability, not compliance evidence.

## NIST SP 800-82r3

### CA-7

Continuous monitoring.

Applies because the skill produces a repeatable capture artifact. CA-7 requires the organization to monitor and assess control effectiveness. The capture is the source data for that assessment on the inventoried segment. A one-time capture is a baseline, not a monitoring program.

### SC-7

Boundary protection.

Steps 4 through 7 record flows between assets. SC-7 requires defined boundaries and communication paths. The flow data is the evidence used to write and review boundary rules. If the segment has no boundary rules, this skill does not create them. It produces the data needed to define them.

## ATT&CK for ICS

### T0842

Network Sniffing.

Applies as telemetry. Steps 2 through 7 collect the same frames an adversary reads under T0842. The purpose is defensive inventory. The capture is also the sensor an incident responder reuses. T0842 is not performed by this skill. The baseline makes T0842 behavior visible to detection.

## NIST CSF 2.0

### ID (Identify)

Family level. CSF 2.0 subcategories are site specific. This skill maps to the Identify function because its output is an asset inventory. The site assigns the specific ID subcategories, for example asset management and baseline configuration, at deployment time. This file deliberately does not pin a subcategory ID.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.
