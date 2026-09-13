# Framework Mappings: modbus-device-enumeration

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 3.1

Communication integrity.

Applies because steps 2 and 4 record the function code set each unit actually uses. SR 3.1 requires integrity protection for communications. The recorded function set is the baseline an anomaly monitor compares against. The skill only records. It does not enforce.

### SR 7.6

Network and service availability.

Applies because steps 4 through 6 verify each unit answers within the timeout. SR 7.6 requires that essential services remain available under stress. A unit that returns 0x0B is not available through the gateway. The exception code is the evidence.

## IEC 62443-4-2

### CR 3.1

Communication integrity for the component.

Component level analogue of SR 3.1. The skill records which functions a device supports, which is the input for the device capability statement an integrator writes against CR 3.1. If the device supports no write functions, that is worth recording in the capability set.

## ATT&CK for ICS

### T0861

Point and Tag Identification.

Applies as adversarial-model telemetry. The register map built in steps 4 and 5 is the point map an adversary enumerates under T0861. Building it defensively gives the operator a baseline of legitimate addresses. The mapping is traceability. The skill does not perform T0861.

### T0855

Unauthorized Command Message.

Step 2 flags write function codes (0x05, 0x06, 0x0F, 0x10) against non-authorized targets. A write outside the authorized set is what T0855 looks like on the wire. The flagged row is the detection input, not a verdict.

## NIST SP 800-82r3

### RA-5

Vulnerability scanning.

Read-only register enumeration is the ICS-safe form of assessment input. RA-5 requires scanning for vulnerabilities. The register and function set collected here populates the device profile used in that assessment. This is a family-anchored placement; the site maps the specific RA-5 controls at deployment.

## NIST CSF 2.0

### ID (Identify)

Family level. The output is a register and function inventory. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.
