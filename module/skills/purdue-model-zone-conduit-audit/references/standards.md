# Framework Mappings: purdue-model-zone-conduit-audit

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 5.1

Network segmentation.

Applies because steps 2 and 5 verify that zones are segmented and that no flow crosses level boundaries except through approved conduits. SR 5.1 requires segmentation to limit event effects. The zone map review produces the boundary evidence. A missing enforcement device for a zone is a finding.

### SR 5.2

Zoning.

Applies because step 2 validates the zone membership list and a named owner per zone. SR 5.2 requires zone definition. Undocumented zones and flows flagged in step 4 are the direct evidence that zoning is incomplete.

## IEC 62443-4-2

### CR 5.2

Zoning for components.

Applies as the component-level counterpart of SR 5.2. Step 2 records the enforcement devices per zone boundary, which is the component view of zoning. The audit does not verify the firmware inside the device. It verifies the boundary role the device plays.

## ATT&CK for ICS

### T0886

Remote Services.

Applies as a detection mapping. Step 5 flags remote desktop and remote service traffic across level boundaries. Such traffic is the vector for T0886. The flagged flow pair is the detection input.

### T0842

Network Sniffing.

Applies as telemetry reuse. The `flows.csv` baseline from `passive-ot-network-discovery` shows the normal conduit set. A new or undocumented conduit that matches no map row is candidate T0842-era reconnaissance or a device an adversary sees. The mapping is traceability, not a verdict.

## NIST SP 800-82r3

### SC-7

Boundary protection.

Applies because step 2 records the enforcement device at each boundary and step 6 checks the conduit protocol scope. SC-7 requires defined boundaries and enforcement. The enforcement device list is the SC-7 evidence.

## NIST CSF 2.0

### ID (Identify)

Family level. The audit output is zone, conduit, and flow inventory. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.
