---
name: safety-instrumented-system-anomaly-detection
description: Detect anomalies on safety instrumented systems including bypass activation, override set, trip setpoint modification, sensor disagreement, and SIS to BPCS writes. Use when monitoring Triconex, HIMA, ProSafe, Safety Manager, or DeltaV SIS platforms.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-MON-safety-instrumented-system-anomaly-detection
  author: comradezephyr
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0878
# allowed-tools: Read Grep Bash
---

## When to Use

- Monitoring SIS controllers for bypass or override manipulation.
- Hunting for trip setpoint modification on safety controllers.
- Investigating sensor disagreement between SIS and BPCS measurements.
- Reviewing SIS audit trails during an incident or a periodic safety review.

## Prerequisites

- SIS platform inventory: Triconex, HIMA, Yokogawa ProSafe, Honeywell Safety Manager, Emerson DeltaV SIS. One row per controller: platform, model, IP, engineering protocol and port.
- Suricata 7.x on the span covering the SIS network segment.
- SIS audit trail access: Triconex TriStation event log, HIMA audit, ProSafe event journal, Safety Manager log, DeltaV SIS event log.
- Trip setpoint and bypass register baseline from the safety engineer.
- Approved proof test schedule.
- Credentials: read-only SIS event log access. Engineering access is not required and must not be requested.
- Authorization: safety engineer sign-off. SIS traffic analysis is passive. Any live interaction with a SIS controller requires the safety engineer and change control together.
- Upstream skills: `passive-ot-network-discovery` for the SIS segment span validation.

### Safety

This skill is passive by default. Active steps are gated in the Workflow section.

- Passive. Analyzes SIS audit logs and span traffic. Safe to run during normal operations.

## Workflow

1. Validate the span on the SIS segment:
   `tshark -i <iface> -c 10 -Y "tcp.port == 5001 or tcp.port == 1233 or tcp.port == 2114"`
   Adjust the port list to the controller inventory. TriStation uses 5001. If no frames appear, the span is not on the SIS segment. Stop and fix the span. Do not proceed without SIS visibility.
2. Author the ruleset from `references/detection-rules.md`. Every rule keys on the SIS controller variable `$SIS_SERVERS` and the approved engineering station variable `$SIS_ENG_HOSTS`.
3. Validate offline: `suricata -T -c /etc/suricata/suricata.yaml`.
4. Deploy the ruleset:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   Copy the rules to the sensor and reload with `suricatasc -c reload-rules`.
5. Prove the rules fire using offline replay only:
   `suricata -r sis-test.pcapng -c /etc/suricata/suricata.yaml -l test-output/`
   Build the replay capture on a bench segment. Never replay a bypass or override command toward a live SIS controller.
6. Review the SIS audit trail for the review window:
   - Bypass or override activations. Every entry needs a permit number. Entries without permits are findings.
   - Trip setpoint changes. Every entry needs an approved MOC record.
   - Proof test outcomes. Failures are findings routed to the safety engineer.
   - Communication loss between SIS and BPCS. Repeated loss pairs with network faults.
7. Run the sensor disagreement check. Compare SIS sensor readings against BPCS readings for the same process points in the historian. Sustained disagreement beyond sensor tolerance is a finding.
8. Check for SIS to BPCS writes. The SIS is a consumer of process data. A SIS controller writing into BPCS registers is architecturally wrong and is a High finding.
9. Produce `sis-anomaly-detection.md`. One row per finding: controller, finding type, timestamp, permit or MOC reference, severity, evidence.

## Verification

- Correct output: `sis-anomaly-detection.md` covers bypass, override, setpoint change, sensor disagreement, proof test, and SIS to BPCS write checks for every controller in the inventory.
- Failure mode: the SIS span carries no frames. The segment span is wrong. Do not report the SIS as clean. Report no-visibility and fix the span first.
- Failure mode: bypass entries without permits on every controller. The permit workflow is not enforced. Report as an estate-wide safety governance gap.
- OT check: zero bypass or override activations outside the approved proof test windows over a 30 day baseline.
- OT check: confirm no SIS controller accepted a connection from a station outside `$SIS_ENG_HOSTS`. Engineering access to a SIS is restricted by design. A foreign connection is a High finding.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 6.2 | Continuous monitoring. The ruleset and audit review are the SIS monitoring capability. |
| IEC 62443-3-3 | SR 6.1 | Audit log accessibility. SIS event logs must be readable for the review to operate. |
| IEC 62443-3-3 | SR 2.8 | Auditable events. Bypass and setpoint changes must leave audit records. |
| ATT&CK for ICS | T0878 | Alarm Suppression. Bypass and override activation suppress the safety function. |
| ATT&CK for ICS | T0831 | Loss of Control. Manipulated trip setpoints transfer control authority away from the SIS. |
| ATT&CK for ICS | T0855 | Unauthorized Command Message. Writes into BPCS registers from the SIS. |
| NIST SP 800-82r3 | SI-4 | System Monitoring. The deployed ruleset is the SI-4 sensor for the SIS segment. |
| NIST CSF 2.0 | DE | Detect. Family level. Site assigns specific subcategories. |


Row-by-row justification lives in `references/standards.md`.
