# Framework Mappings: ot-network-segmentation-design

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a design decision in the Workflow section. Keep both files in sync.

## IEC 62443-3-2

### zone and conduit design

Applies because the workflow produces the 62443-3-2 outputs: zone partitioning, conduit definitions, and SL-T assignment. Steps 1 through 4 are the zone and conduit design process.

### risk assessment

Applies because step 3 derives SL-T from consequence of compromise. 62443-3-2 requires a risk assessment per zone before SL-T assignment. An SL-T without the consequence statement is an unsupported target.

## IEC 62443-3-3

### SR 5.1

Network segmentation.

Applies to steps 1 through 4. The zone and conduit structure is the SR 5.1 design. Segmentation limits the effect of an event to the zone it starts in.

### SR 5.2

Zone boundary protection.

Applies to step 6. Naming the enforcement mechanism per zone makes SR 5.2 implementable rather than aspirational.

### SR 7.1

Resilience against denial of service.

Applies to step 4. Conduits bound flood propagation between zones. The design documents which conduits carry rate-limiting or priority handling.

## NIST SP 800-82r3

### SC-7

Boundary Protection.

Applies to steps 4 through 6. The conduit enforcement design is the SC-7 implementation for the OT boundary.

### RA-2

Security Categorization.

Applies to step 3. The consequence-of-compromise classification per zone is the RA-2 action that feeds SL-T.

## NIST CSF 2.0

### GV (Govern)

Family level. Zone ownership and SL-T acceptance are governance decisions. CSF subcategories are site specific and are not pinned by this file.

## ATT&CK for ICS

### T0886

Remote Services.

Applies to step 5. The L3.5 boundary decision bounds the reach of a compromised remote path. A remote access compromise at L4 cannot touch controllers when the boundary holds.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

