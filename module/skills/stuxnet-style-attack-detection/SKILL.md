---
name: stuxnet-style-attack-detection
description: Detect logic tampering, sensor spoofing, and EWS-driven PLC writes consistent with Stuxnet-style attacks. Use when hunting for covert PLC modification where network controls show nothing and process behavior does not match operator intent.
version: 0.1.0
license: Apache-2.0
metadata:
  author: your-github-username
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0889
# allowed-tools: Read Grep Bash
---

## When to Use

- Hunting for covert PLC logic modification where the network shows no alerts.
- Investigating process behavior that matches setpoints no operator entered.
- Correlating a `plc-logic-integrity-check` MISMATCH with other telemetry.
- Building a detection baseline for safety-related controllers.

## Prerequisites

- Zeek logs from a SPAN of the segment: `conn.log`, `modbus.log` or S7comm captures.
- Suricata `eve.json` from the same span, if deployed.
- Historian export for the sensors and setpoints on the target controllers.
- Change window calendar. Every detection below keys on the approved change schedule.
- Output from `passive-ot-network-discovery` for the master-slave pair list.
- Credentials: read-only historian access, read-only HMI audit logs.
- Authorization: none for analysis. Every live controller check is gated upstream.
- Upstream skills: `plc-logic-integrity-check` for the hash baseline. This skill interprets its output.

### Safety

This skill is passive. No step in this workflow sends packets to a live device.

- Passive. Analyzes logs, captures, and historian exports. Safe to run during normal operations.

## Workflow

This skill is a detection strategy, not a single rule. It maps each Stuxnet-style indicator to a detection source and an escalation path. Record findings per indicator in `logic-tamper-detection-strategy.md`.

1. Build the change window table. One row per controller: approved change windows, approved engineering stations, approved logic versions.
2. Indicator 1: PLC program downloads. Detection sources:
   - Network: Suricata on TCP 102. Anchor on TPKT, then COTP, then the S7comm header before matching the download function code:
     `alert tcp any any -> $PLC_SERVERS 102 (msg:"ICS s7 download attempt outside change window"; flow:to_server,established; content:"|03 00|"; depth:2; content:"|02 f0 80|"; content:"|32 01|"; within:12; content:"|1a|"; within:8; sid:1000301; rev:1;)`
   - Host: the `plc-logic-integrity-check` MISMATCH report. Any MISMATCH outside a change window is an Indicator 1 hit.
   - Technique mapping: T0843 Program Download, T0845 Program Upload, T0889 Modify Program.
3. Indicator 2: function block changes on safety-related logic. Detection sources:
   - Vendor audit: TIA Portal project audit trail, Studio 5000 change history export. Diff against the last approved project file.
   - Controller: the S7 block hash baseline. A change in an OB or FB that feeds a safety interlock escalates one severity level above a standard MISMATCH.
   - Technique mapping: T0889 Modify Program, T0821 Modify Controller Tasking.
4. Indicator 3: sensor value clusters at the same constant. Detection sources:
   - Historian export. For each redundant sensor group, compute the variance across sensors over rolling windows. Distinct sensors reporting identical values for more than one scan cycle while the process is dynamic is a hit.
   - Network: `tshark -r capture.pcapng -Y "modbus.func_code == 3" -T fields -e ip.src -e modbus.unit_id` to list which masters read the sensor registers, then check whether any master also writes them. A master that reads and writes the same sensor register set is a T0856 pattern.
   - Technique mapping: T0856 Spoof Reporting Message.
5. Indicator 4: HMI setpoint changes without operator action. Detection sources:
   - HMI audit log export. Correlate setpoint writes in the Modbus or S7 stream with operator session records. A write with no matching logged operator session is a hit.
   - Network: Suricata rule on write function codes from non-HMI sources, using the native modbus keyword: `alert tcp !$HMI_SERVERS any -> $PLC_SERVERS 502 (msg:"ICS modbus write from non-HMI source"; flow:to_server,established; modbus: function 0x06; sid:1000302; rev:1;)`
   - Technique mapping: T0855 Unauthorized Command Message.
6. Indicator 5: EWS to PLC writes outside change windows. Detection sources:
   - Network: Zeek `conn.log` filtered to engineering station source IPs and controller destinations. Any long-lived session with write traffic outside the change window table from step 1 is a hit.
   - Controller: pair with the Indicator 1 MISMATCH to confirm the write landed.
   - Technique mapping: T0843 Program Download, T0889 Modify Program.
7. Correlate. Two or more indicators on the same controller inside 30 days is a candidate campaign. Escalate to incident response. One indicator alone is a tuning input.
8. Produce `logic-tamper-detection-strategy.md`. One row per indicator: detection sources, telemetry owner, rule or query ID, escalation path, last tested date.

## Verification

- Correct output: `logic-tamper-detection-strategy.md` covers all five indicators with at least one working detection source each, and every rule or query ID resolves to a tested artifact.
- Failure mode: the historian export lacks redundant sensor groups. Indicator 3 cannot be evaluated. Report the indicator as not-covered rather than clear.
- Failure mode: HMI audit logging is disabled. Indicator 4 cannot be evaluated. Report as not-covered and raise the logging gap as its own finding.
- OT check: prove each rule fires without touching a live process. Replay a captured change-window download into the IDS offline with `suricata -r capture.pcapng -c suricata.yaml`. The alert must appear in `eve.json` with the expected `sid`.
- OT check: run each rule against a 72 hour baseline capture with zero hits. A rule that fires on normal polling is misconfigured and must be tuned before deployment.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 6.2 | Continuous monitoring. The strategy defines what to monitor on safety-related controllers. |
| IEC 62443-3-3 | SR 2.8 | Auditable events. HMI and controller audit trails are the evidence sources. |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. Sensor spoofing detection guards reported data integrity. |
| ATT&CK for ICS | T0843 | Program Download. Indicator 1 network detection. |
| ATT&CK for ICS | T0845 | Program Upload. Indicator 1 controller-side detection. |
| ATT&CK for ICS | T0889 | Modify Program. Indicators 1, 2, and 5. |
| ATT&CK for ICS | T0856 | Spoof Reporting Message. Indicator 3 sensor spoofing. |
| ATT&CK for ICS | T0855 | Unauthorized Command Message. Indicator 4 unattended setpoint writes. |
| ATT&CK for ICS | T0821 | Modify Controller Tasking. Indicator 2 safety-related block changes. |
| NIST SP 800-82r3 | SI-4 | System Monitoring. The strategy is the SI-4 monitoring plan for control logic. |
| NIST CSF 2.0 | DE | Detect. Family level. Site assigns specific subcategories. |

