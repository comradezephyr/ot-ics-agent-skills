# Framework Mappings: iec-62443-certification-readiness

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a workflow step. Keep both files in sync.

## IEC 62443-4-1

### SM-1 through SM-13

Security management practices for the secure development lifecycle. Applies to steps 2 and 3. The evidence register maps each SM practice family to the lifecycle documentation the certification body audits. SM covers security management of requirements, design, implementation, verification, defect management, patch handling, and the supporting practices.

## IEC 62443-4-2

### CR 1.1 through CR 7.8

Component requirement families. Applies to steps 2 and 3. CR families cover identification and authentication, use control, system integrity, data confidentiality, restricted data flow, timely response, and resource availability, each with the component-level requirement detail. The component certificate names the SL and the exact CRs satisfied.

## IEC 62443-3-3

### SR families at target SL

System requirement families. Applies to steps 2 and 4. The system assessment allocates the SRs to system elements against the SL-T from the zone design. Component certificates reduce per-element evidence effort but do not remove the system-level composition assessment.

## IEC 62443-2-4

### service provider requirements

Applies to steps 2 and 3. Covers service delivery, personnel and training, access control, incident handling, and patch management obligations for providers working in customer ICS environments. The remote access scope is the part that matters most to customers.

## IEC 62443-3-2

### zone and conduit design

Prerequisite for the 3-3 scope. Applies to step 2. A system cannot be assessed against 3-3 without the zone model, conduit definitions, and SL-T targets from 62443-3-2.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real part numbers and requirement family identifiers. Do not invent SM or CR identifiers.
- If a mapping cannot be verified from skill output, remove it.
