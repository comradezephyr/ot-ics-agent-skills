# Framework Mappings: ot-lateral-movement-detection

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 5.1

Network segmentation.

Applies because a non-adjacent level crossing is a segmentation violation observed at runtime. SR 5.1 requires networks to be segmented to limit the effect of an event. The monitor verifies that the segmentation holds in traffic, not only in diagrams.

### SR 5.2

Zone boundary protection.

Applies because the rules watch the boundary crossings SR 5.2 defines. A flow from L4 into L1 without an L3.5 hop means the boundary control did not enforce.

### SR 6.2

Continuous monitoring.

Applies because the ruleset is the deployed boundary monitoring capability. SR 6.2 requires the capability to monitor security-relevant events. Adjacent-conduit tuning and the 72 hour baseline keep the capability calibrated.

## ATT&CK for ICS

### T0886

Remote Services.

Applies because RDP, SSH, and SMB crossings are the remote service path an adversary uses to stage between zones. The rules key on service ports and level pairs.

### T0884

Connection Proxy.

Applies because vendor tunnels and jump hosts are the proxy points. Tunnel reuse outside the approved window is the observable.

### T0888

Remote System Information Discovery.

Applies as a sequencing mapping. Crossing traffic frequently precedes discovery scanning from the newly reached level. A crossing alert raises the priority of discovery-class alerts on the destination subnet.

## NIST SP 800-82r3

### SC-7

Boundary Protection.

Applies because the crossing monitor verifies SC-7 enforcement at runtime. SC-7 requires managed interfaces with deny by default. A non-adjacent crossing is a managed-interface failure caught in operation.

## NIST CSF 2.0

### DE (Detect)

Family level. The skill is a detection capability. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

