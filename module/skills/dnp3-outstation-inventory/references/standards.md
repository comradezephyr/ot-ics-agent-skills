# Framework Mappings: dnp3-outstation-inventory

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 3.1

Communication integrity.

Applies because steps 2 and 3 record which function codes each outstation actually accepts. SR 3.1 requires integrity protection for communications. The per-outstation function set is the baseline an anomaly detector later uses. The skill observes. It does not enforce.

## NIST SP 800-82r3

### CA-7

Continuous monitoring.

Applies because the outstation map is a repeatable capture artifact. CA-7 requires monitoring and reassessment of controls. The address and function inventory is the source data for the segment assessment. A one-time map is a baseline, not a monitoring program.

## ATT&CK for ICS

### T0848

Rogue Master.

Applies as a detection mapping. Step 5 treats repeated link resets as a candidate second master. T0848 describes an adversary posing as a master to control an outstation. The reset pattern is the telemetry that flags the behavior. The mapping is traceability, not a verdict.

### T0855

Unauthorized Command Message.

Applies as a detection mapping. Step 3 records the function set. A SELECT or OPERATE toward an outstation that normally only receives READ is candidate T0855 traffic. The flag is the detection input.

## NIST CSF 2.0

### ID (Identify)

Family level. The skill output is an outstation and master inventory. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.
