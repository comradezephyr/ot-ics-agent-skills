# Framework Mappings: nerc-cip-compliance-check

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a workflow step. Keep both files in sync.

## NERC CIP

### CIP-002-5.1a R1

BES Cyber System categorization.

Applies to steps 1 and 2. Applicability and impact level determine which requirements the matrix covers. A matrix built without a current categorization is assessing the wrong requirement set.

### CIP-007-6 R1 through R5

Systems security management.

Applies to step 4. R1 ports and services, R2 security patch management, R3 malicious code prevention, R4 security event monitoring, and R5 system access control are the requirement rows with the most per-device evidence burden. These five are also the rows most often marked compliant on a policy document rather than device evidence.

### CIP-010-3 R1

Configuration change management.

Applies to step 4. The change management evidence for BES Cyber Systems. This row connects to the site change process: where the site has no OT change workflow, this requirement is where the missing process surfaces.

### CIP-013-1 R1 through R3

Supply chain risk management.

Applies to step 4. Vendor risk processes and procurement obligations. The `ot-vendor-risk-assessment` register is reusable evidence for these rows when its scope covers the registered entity's vendors.

### Standard-level rows

CIP-003, CIP-004, CIP-005, CIP-006, CIP-008, CIP-009, CIP-011, and CIP-014 appear in the matrix at standard level because the applicable sub-requirement identifiers vary by impact level and by current version. Each row carries the note to verify the sub-requirement against the current standard document. Do not fill in sub-requirement identifiers from memory.

## NIST SP 800-82r3

### SI-2

Flaw Remediation.

Applies to step 5. Maps to CIP-007-6 R2. The NIST control describes the remediation requirement. The CIP requirement adds entity-specific evidence and retention obligations. Use the NIST mapping to explain the control to engineers and the CIP language to report to the regulator.

### SC-7

Boundary Protection.

Applies to step 7. Maps to the electronic security perimeter requirement. The reality check compares the documented perimeter to observed traffic, which is the SC-7 enforcement question asked in CIP language.

### IR-4

Incident Handling.

Applies to step 4. Maps to CIP-008 incident reporting and response planning.

### CP-9

System Backup.

Applies to step 4. Maps to CIP-009 recovery plan requirements.

### CM-3

Configuration Change Control.

Applies to step 4. Maps to CIP-010-3 R1.

### RA-3

Risk Assessment.

Applies to step 2. Maps to the categorization basis. The impact level assignment is a risk assessment output.

### SA-9

External Information System Services.

Applies to step 4. Maps to CIP-013 vendor obligations.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real standard and control IDs. Do not invent sub-requirement identifiers.
- Standard version numbers and sub-requirement identifiers must be verified against the current published standard before external use.
- If a mapping cannot be verified from skill output, remove it.
