# Framework Mappings: dmz-architecture-for-ot

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a design decision in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 5.1

Network segmentation.

Applies to decisions 1 and 2. The DMZ is the segmentation layer between L4 and L3. SR 5.1 requires segmentation to limit the effect of an event. The service placement decision keeps enterprise-reachable services out of OT zones.

### SR 5.2

Zone boundary protection.

Applies to decisions 3 through 7. Brokered access, one-way replication, and staged updates enforce the L3.5 boundary. SR 5.2 requires denial of unauthorized communication across zone boundaries.

## NIST SP 800-82r3

### SC-7

Boundary Protection.

Applies to decision 3. The diode versus firewall decision per flow is the SC-7 implementation at the highest-risk boundary in the plant.

### SC-8

Transmission Confidentiality and Integrity.

Applies to decisions 3 and 4. One-way transfer designs for high-value flows are the SC-8 hard boundary where the value justifies the cost.

### CM-3

Configuration Change Control.

Applies to decision 6. The staging path brings patch flow under change control before it touches OT.

### CM-5

Access Restrictions for Change.

Applies to decision 6. The verified-hash pull restricts what can change in OT to artifacts that passed verification in the DMZ.

### AC-17

Remote Access.

Applies to decisions 5 and 7. Termination in the DMZ is the AC-17 architectural decision.

### IA-2

Identification and Authentication, organizational users.

Applies to decision 8. OT-side identity services keep authentication available when the enterprise domain is not.

## NIST CSF 2.0

### PR (Protect)

Family level. The DMZ is a protection architecture. CSF subcategories are site specific and are not pinned by this file.

## ATT&CK for ICS

### T0886

Remote Services.

Applies to decisions 5 and 7. Brokered termination removes direct remote paths into OT, which is the T0886 entry surface.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

