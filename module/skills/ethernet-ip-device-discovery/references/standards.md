# Framework Mappings: ethernet-ip-device-discovery

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 5.1

Network segmentation.

Applies because the inventory in steps 2 and 4 defines which CIP hosts belong to the same zone. SR 5.1 requires segmentation to limit event effects. The 44818 and UDP 2222 exposure map is the input for that segmentation.

### SR 3.1

Communication integrity.

Applies because the flow map in step 2 records the expected CIP session set. SR 3.1 requires integrity for communications. The session baseline is what later monitoring compares against. The skill observes. It does not protect.

## NIST SP 800-82r3

### SC-7

Boundary protection.

Applies because steps 4 and 5 measure which hosts accept 44818 connections from outside the zone. SC-7 requires defined boundaries. The set of 44818 listeners is the evidence used to write the boundary rule. `session-gated` devices need a different rule shape than open Identity responders.

## ATT&CK for ICS

### T0846

Remote System Discovery.

Applies as adversarial-model telemetry. Enumeration of the CIP identity is what an adversary performs under T0846 before a targeted CIP attack. The skill runs the same query for inventory. The result is a defensive baseline. The mapping is traceability, not permission to perform the technique.

## NIST CSF 2.0

### ID (Identify)

Family level. The skill output is a CIP device inventory. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.
