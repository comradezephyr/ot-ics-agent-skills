# Framework Mappings: profinet-device-inventory

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 5.1

Network segmentation.

Applies because the island inventory in steps 2 through 6 defines where a PROFINET zone starts and stops. SR 5.1 requires networks to be segmented. The broadcast scope of DCP is the practical boundary: devices that answer the burst belong to the same zone. The inventory is the input, not the zone policy itself.

## NIST SP 800-82r3

### SC-7

Boundary protection.

Applies because step 4 measures which devices share a Layer 2 broadcast domain. SC-7 requires defined boundaries and enforcement at those boundaries. A DCP-answerer inside the island and a DCP-answerer outside it must be in different zones. The burst result is the evidence for that boundary rule.

## ATT&CK for ICS

### T0846

Remote System Discovery.

Applies as adversarial-model telemetry. DCP Identify enumeration is how an adversary profiles a PROFINET island at Layer 2. The skill runs the same queries for inventory. The result is a baseline of every MAC and station name an adversary would see. T0846 is not performed for offense. The baseline makes the technique visible to detection rather than being the technique.

## NIST CSF 2.0

### ID (Identify)

Family level. The skill output is a station name and MAC inventory. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.
