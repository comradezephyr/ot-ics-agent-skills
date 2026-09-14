---
name: dnp3-anomaly-detection
description: Build and run DNP3 anomaly detection with Suricata and Zeek rules covering unauthorized function codes, outstation impersonation, unsolicited responses, cold restart, time sync changes, and auth bypass attempts. Use when monitoring port 20000 traffic.
version: 0.1.0
license: Apache-2.0
metadata:
  author: your-github-username
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0855
# allowed-tools: Read Grep Bash
---

## When to Use

- Monitoring a DNP3 segment for unauthorized master or outstation behavior.
- Hunting for outstation impersonation or unsolicited response injection.
- Detecting cold restart or time sync manipulation on SCADA links.
- Investigating operator reports of stale or frozen telemetry.

## Prerequisites

- Suricata 7.x. Verify with `suricata --build-info`. The `dnp3:` keyword is native.
- Zeek 5.x with the DNP3 analyzer. Verify with `zeek -NN dnp3`.
- Baseline from `passive-ot-network-discovery`: master and outstation pair list, polling schedule, normal function code counts.
- Site variables for the ruleset: `$DNP3_MASTERS`, `$DNP3_OUTSTATIONS`.
- Python 3.10 or newer for the triage script.
- Credentials: none for analysis. IDS reload rights for deployment.
- Authorization: segment owner sign-off for rule deployment. Live test traffic is gated.
- Upstream skills: `passive-ot-network-discovery` for the pair list and polling baseline.

### Safety

This skill is passive by default. Active steps are gated in the Workflow section.

- Passive. Authors rules and analyzes captures and IDS logs. Safe to run during normal operations.

## Workflow

1. Extract the authorized pairs and function code profile from the baseline:
   `tshark -r baseline.pcapng -Y "dnp3" -T fields -e ip.src -e ip.dst -e dnp3.func | sort | uniq -c > dnp3_profile.txt`
   Function codes appear as decimal values. 1 READ, 2 WRITE, 3 SELECT, 4 OPERATE, 5 DIRECT_OPERATE, 13 COLD_RESTART, 24 WRITE time sync class.
2. Author the ruleset from `references/detection-rules.md`. Fill the site variables. All rules use the native `dnp3:` keyword.
3. Validate the ruleset offline:
   `suricata -T -c /etc/suricata/suricata.yaml`
4. Validate the Zeek policy offline against the baseline capture:
   `zeek -C -r baseline.pcapng scripts/dnp3-anomaly`
5. Deploy the ruleset to the IDS:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   Copy the rules to the sensor, then `suricatasc -c reload-rules`.
6. Prove each rule fires using offline replay only:
   `suricata -r dnp3-test.pcapng -c /etc/suricata/suricata.yaml -l test-output/`
   Each rule must produce its alert in `test-output/eve.json` with the expected `signature_id`.
7. Generate live test traffic only if replay cannot exercise a rule:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   Issue a READ to one outstation from an approved test master inside the maintenance window. Never test DIRECT_OPERATE or COLD_RESTART rules against a live outstation. Use replay for those.
8. Triage production alerts:
   `python3 scripts/dnp3_triage.py /var/log/suricata/eve.json --out dnp3-triage.md`
9. Correlate with Zeek. Outstation impersonation shows as one DNP3 address with two source IPs. Verify in zeek `dnp3.log`:
   `cat dnp3.log | awk '{print $5, $6, $7}' | sort | uniq -c | sort -rn | head`
   An address column with multiple source IPs is an impersonation candidate. Escalate to incident response.

## Verification

- Correct output: `dnp3-triage.md` has one row per alert group with source, destination, function code, first and last seen, and count. Every deployed rule has a replay test result.
- Failure mode: rules on DIRECT_OPERATE or COLD_RESTART never fire in replay. The test capture lacks those codes. Build the replay capture from scapy-generated DNP3 frames on a bench segment, never from a live outstation.
- Failure mode: unsolicited-response rules fire during normal startup. Some outstations send unsolicited data on link recovery. Confirm the polling baseline in step 1 and add the startup window to the rule schedule.
- OT check: zero hits over a 72 hour baseline capture excluding the approved startup window.
- OT check: confirm the outstation under test stayed in service. A COLD_RESTART test is replay-only. Any live restart request is a process safety event.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 6.2 | Continuous monitoring. The ruleset is the monitoring capability for the DNP3 segment. |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. Impersonation and rogue master alerts flag integrity violations. |
| IEC 62443-3-3 | SR 7.6 | Network and service availability. Cold restart and denial rules guard outstation availability. |
| ATT&CK for ICS | T0855 | Unauthorized Command Message. DIRECT_OPERATE and WRITE from non-masters. |
| ATT&CK for ICS | T0848 | Rogue Master. Impersonation detection, one outstation address from two sources. |
| ATT&CK for ICS | T0856 | Spoof Reporting Message. Unsolicited response injection outside the polling window. |
| ATT&CK for ICS | T0881 | Service Stop. COLD_RESTART detection. |
| NIST SP 800-82r3 | SI-4 | System Monitoring. The deployed ruleset is the SI-4 sensor for DNP3. |
| NIST CSF 2.0 | DE | Detect. Family level. Site assigns specific subcategories. |

