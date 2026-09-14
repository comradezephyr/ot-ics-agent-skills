# Framework Mappings: safety-instrumented-system-anomaly-detection

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 6.2

Continuous monitoring.

Applies because the ruleset and the audit trail review are the deployed monitoring capability for the SIS segment. SR 6.2 requires the capability to monitor security-relevant events. On a SIS the monitoring capability is also a process safety input.

### SR 6.1

Audit log accessibility.

Applies because the workflow requires read access to the SIS event logs. SR 6.1 requires that audit logs be accessible to authorized personnel and tools. Where a platform cannot expose its audit trail, the gap is recorded and the affected checks report not-covered.

### SR 2.8

Auditable events.

Applies because bypass activation, override set, and trip setpoint modification are the security-relevant events SR 2.8 expects to be auditable. A bypass without an audit record is a double failure: the safety event and the missing evidence.

## ATT&CK for ICS

### T0878

Alarm Suppression.

Applies because bypass and override activation suppress the safety function that generates alarms and trips. T0878 covers an adversary suppressing alarms and safety responses. Every bypass without a permit number is the T0878 observable.

### T0831

Loss of Control.

Applies because manipulated trip setpoints transfer control authority away from the SIS. T0831 covers an adversary taking control of the process. Setpoint modification on a safety controller is the precondition.

### T0855

Unauthorized Command Message.

Applies because a SIS controller initiating writes into BPCS registers is an unauthorized command in the wrong direction. The SIS is a consumer of process data, not a writer.

### T0836

Manipulation of Reporting.

Applies as a threat mapping for the sensor disagreement check. Spoofed or frozen SIS sensor reporting is the observable condition the check detects.

## NIST SP 800-82r3

### SI-4

System Monitoring.

Applies because the deployed ruleset is the SI-4 sensor for the SIS segment. SI-4 requires monitoring to detect unauthorized activity. The SIS segment is typically the most sensitive and least monitored segment in the plant.

## NIST CSF 2.0

### DE (Detect)

Family level. The skill is a detection capability. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

