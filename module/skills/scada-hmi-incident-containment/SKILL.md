---
name: scada-hmi-incident-containment
description: Contain a compromised SCADA HMI without disrupting process control by isolating it at the firewall, preserving session logs, and switching operators to a backup HMI path. Use when an HMI shows compromise indicators or receives untrusted input.
version: 0.1.0
license: Apache-2.0
metadata:
  author: your-github-username
  frameworks:
    - IEC 62443-2-1
    - NIST SP 800-82r3
    - ATT&CK for ICS T0886
# allowed-tools: Read Grep Bash
---

## When to Use

- Compromise indicators on an HMI: unexpected screens, unresponsive setpoint controls, unknown sessions.
- Unexplained setpoint changes traced to an HMI session.
- Malware alerts on an HMI host.
- An operator reports the HMI behaving outside its commissioned design.

## Prerequisites

- Backup HMI or a local control path that can take over visualization and manual control.
- Firewall access to isolate the HMI segment from controllers.
- HMI session logs and audit trail access.
- Zone map showing the HMI segment and its controller connections.
- Credentials: read-only for log preservation, admin on the boundary firewall for isolation.
- Authorization: operations manager approves the isolation and the operator switch. Confirm the backup HMI path is live before isolating the primary.
- Upstream skills: `ot-incident-triage` for the decision record.

### Safety

This skill is active. Firewall isolation changes a live system and is gated in the Workflow section.

- Active. Applies firewall changes to live segments. Requires operations manager approval. Process continuity is the constraint the containment works inside.

## Workflow

> SAFETY: If at any point the action risks human safety or process integrity, halt and escalate to the operations lead before continuing.

1. Confirm the decision authority. The operations manager owns the operator switch and the isolation. Record name, contact, and time.
2. Preserve evidence before any change. Export the HMI session logs, audit trail, and screen event history to the forensic share. Hash the exports:
   `sha256sum hmi-sessions.log hmi-audit.log > evidence.sha256`
   Logs on a compromised host may be tampered with after this point. Copy first, act second.
3. Verify the backup HMI path. Confirm the backup HMI or local control station reads current process values and can issue commands. If no backup path exists, this step will interrupt operator control when the HMI is isolated. Confirm with operations before proceeding.
4. Isolate the HMI at the firewall:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   Apply a deny between the HMI segment and the controller network. Do not power off the HMI. The deny is on new controller-bound sessions; the operators have already switched.
5. Confirm controllers are unaffected. Verify on the span that controller traffic flows at the baseline rate and that no session from the HMI segment remains established:
   `tshark -i <iface> -c 20 -Y "ip.src == <hmi-segment> and (tcp.port == 502 or tcp.port == 102 or tcp.port == 44818)"`
   Any remaining established session is a containment failure. Terminate it at the firewall.
6. Switch operators to the backup HMI. Confirm operators can read values and issue commands from the backup path before declaring containment.
7. Verify controller response from the backup path. Issue a low-risk operator action, such as a screen refresh of a non-critical setpoint, and confirm the controller acknowledges. Do not test with a critical setpoint.
8. Produce `hmi-containment-record.md`. Sections: decision authority, evidence export hashes, isolation rule details with timestamps, backup HMI switch time, controller response verification, follow-up actions.

## Verification

- Containment confirmed: no session from the HMI segment reaches any controller, the firewall deny is active, and the HMI host remains powered for forensics.
- Process safety confirmed: operators read current values and issue commands from the backup path, and controller traffic runs at the baseline rate without the HMI segment.
- No new problems confirmed: the deny rule touches only the affected HMI segment, the backup HMI switch introduced no setpoint changes, and no controller alarm fired during the switch.
- OT check: no write command reached a controller from the compromised HMI during the incident window. Cross-check the controller's change log against the HMI session log. An acknowledged write with no operator session is a logic integrity concern and routes to `plc-logic-integrity-check`.
- OT check: the evidence exports hash-match the source files. A hash mismatch after export means the host tampered with its own logs after the copy.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-2-1 | 4.3.4.5 | Incident response. Containment is a defined response action. |
| IEC 62443-3-3 | SR 2.8 | Auditable events. The session log export preserves the audit evidence. |
| IEC 62443-3-3 | SR 6.2 | Continuous monitoring. The span check verifies the containment held. |
| IEC 62443-3-3 | SR 5.2 | Zone boundary protection. The firewall deny enforces the HMI zone boundary. |
| NIST SP 800-82r3 | IR-4 | Incident Handling. The workflow is the containment procedure. |
| NIST SP 800-82r3 | IR-5 | Incident Monitoring. The span and backup path checks track containment status. |
| NIST CSF 2.0 | RS | Respond. Family level. Site assigns specific subcategories. |
| ATT&CK for ICS | T0886 | Remote Services. The deny closes the HMI session path. |
| ATT&CK for ICS | T0882 | Theft of Operational Information. Log preservation captures what the adversary accessed. |

