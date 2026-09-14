# Framework Mappings: stuxnet-style-attack-detection

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 6.2

Continuous monitoring.

Applies because the strategy defines the monitoring set for control logic: downloads, safety block changes, sensor writes, and engineering sessions. SR 6.2 requires the capability to monitor security-relevant events. Each indicator names its telemetry source and owner, which is the monitoring capability definition.

### SR 2.8

Auditable events.

Applies because indicators 2 and 4 depend on vendor audit trails and HMI session logs. SR 2.8 requires that security-relevant events be auditable. Where the audit trail does not exist, the workflow reports the indicator as not-covered, which surfaces the SR 2.8 gap.

### SR 3.1

Communication integrity.

Applies because indicator 3 detects masters that both read and write sensor registers, the network condition behind spoofed reporting. SR 3.1 requires integrity protection for communications. The detection does not provide the protection. It verifies whether the property is being violated.

## ATT&CK for ICS

### T0843 / T0845

Program Download / Program Upload.

Applies to indicators 1 and 5. The network rules watch download-class requests on TCP 102. The controller-side check is the hash MISMATCH. The two sources together cover both the observed transfer and the resulting state change.

### T0889

Modify Program.

Applies to indicators 1, 2, and 5. A MISMATCH outside a change window is the residual state of T0889 regardless of how the change arrived. Indicator 2 raises severity when the modified block feeds a safety interlock.

### T0856

Spoof Reporting Message.

Applies to indicator 3. Constant sensor clusters across redundant sensors while the process is dynamic is the observable effect of spoofed reporting. The read-write register overlap is the network preconditions check.

### T0855

Unauthorized Command Message.

Applies to indicator 4. A setpoint write with no matching operator session is an unauthorized command regardless of source. The Suricata rule narrows the source set. The audit correlation confirms authorization.

### T0821

Modify Controller Tasking.

Applies to indicator 2. Safety-related block changes alter controller tasking. A change to an interlock-feeding block maps here as well as T0889.

## NIST SP 800-82r3

### SI-4

System Monitoring.

Applies because the strategy is the monitoring plan SI-4 expects for the control logic layer. SI-4 requires monitoring to detect attacks and indicators. Each indicator row in the output is a monitoring capability with an owner and a test date.

## NIST CSF 2.0

### DE (Detect)

Family level. The skill is a detection strategy. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

