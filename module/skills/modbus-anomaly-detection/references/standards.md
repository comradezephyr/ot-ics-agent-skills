# Framework Mappings: modbus-anomaly-detection

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 6.2

Continuous monitoring.

Applies because the ruleset is the deployed monitoring capability for the Modbus segment. SR 6.2 requires the capability to monitor security-relevant events. The rules cover write commands, scanning, unit abuse, and time-based anomalies. The tuning loop in step 9 keeps the capability calibrated.

### SR 3.1

Communication integrity.

Applies because write function codes outside the authorized pair list are integrity violations of the Modbus communication model. SR 3.1 requires integrity protection for communications. The detection does not enforce it. It exposes violations to the monitoring pipeline.

## ATT&CK for ICS

### T0855

Unauthorized Command Message.

Applies because the write-code rules flag command messages from sources outside the authorized HMI set. T0855 covers an adversary sending unauthorized commands to control devices. A write from a non-HMI source is the direct observable.

### T0806

Brute Force I/O.

Applies because the register scanning rule detects high-rate read and write attempts. T0806 covers an adversary brute forcing I/O values. The detection filter threshold catches enumeration that precedes targeted writes.

### T0861

Point and Tag Identification.

Applies because scanning behavior is how an adversary maps points and tags before acting. The scan rule detects the enumeration phase of T0861.

## NIST SP 800-82r3

### SI-4

System Monitoring.

Applies because the deployed ruleset is the SI-4 sensor for the Modbus segment. SI-4 requires monitoring to detect unauthorized activity. Alert coverage per attack class and the 72 hour zero-hit calibration test are the SI-4 verification actions.

## NIST CSF 2.0

### DE (Detect)

Family level. The skill is a detection capability. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

