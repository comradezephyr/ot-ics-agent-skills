# Framework Mappings: dnp3-anomaly-detection

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 6.2

Continuous monitoring.

Applies because the ruleset is the deployed monitoring capability for the DNP3 segment. SR 6.2 requires the capability to monitor security-relevant events. The rules cover rogue commands, restarts, time sync, file transfer, and authentication probing.

### SR 3.1

Communication integrity.

Applies because outstation impersonation and rogue master detection are integrity violations of the master-outstation communication model. SR 3.1 requires integrity protection for communications. The address-sharing check exposes the violation.

### SR 7.6

Network and service availability.

Applies because COLD_RESTART and service stop detection guard outstation availability. SR 7.6 requires protection against denial of network-accessible services. A restart command from a non-master is a denial precondition.

## ATT&CK for ICS

### T0855

Unauthorized Command Message.

Applies because DIRECT_OPERATE and WRITE function codes from non-master sources are unauthorized commands. The rules key on source set and function code.

### T0848

Rogue Master.

Applies because the address-sharing check detects a second source addressing one outstation. T0848 covers an adversary injecting commands as a rogue master station.

### T0856

Spoof Reporting Message.

Applies because unsolicited responses outside the polling window may carry spoofed reporting data. The Zeek policy flags the timing condition.

### T0881

Service Stop.

Applies because COLD_RESTART detection covers an adversary stopping outstation service. A cold restart takes the outstation out of its operating state.

## NIST SP 800-82r3

### SI-4

System Monitoring.

Applies because the deployed ruleset is the SI-4 sensor for the DNP3 segment. SI-4 requires monitoring to detect unauthorized activity. The replay tests and the 72 hour zero-hit calibration are the SI-4 verification actions.

## NIST CSF 2.0

### DE (Detect)

Family level. The skill is a detection capability. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

