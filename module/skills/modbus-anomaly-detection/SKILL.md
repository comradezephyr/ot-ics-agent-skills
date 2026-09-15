---
name: modbus-anomaly-detection
description: Build and run Modbus TCP anomaly detection with Suricata and Zeek rules covering unauthorized write function codes, register scanning, unit ID spoofing, and out-of-hours PLC writes. Use when monitoring port 502 traffic for PLC abuse.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-MON-modbus-anomaly-detection
  author: comradezephyr
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0855
# allowed-tools: Read Grep Bash
---

## When to Use

- Monitoring a Modbus TCP segment for unauthorized write function codes.
- Hunting for register scanning or a new master-slave pair on port 502.
- Investigating operator reports of unexplained setpoint changes.
- Hardening an existing IDS deployment that has no OT-specific rules.

## Prerequisites

- Suricata 7.x. Verify with `suricata --build-info`. The `modbus` keyword requires libhtp-independent protocol support and a `stream.memcap` sized for the segment.
- Zeek 5.x. Verify with `zeek --version`.
- Baseline pair list from `passive-ot-network-discovery` (`modbus_profile.txt`, `hosts.csv`).
- Site variables for the ruleset: `$PLC_SERVERS`, `$HMI_SERVERS`, `$UNIT_WHITELIST`.
- Python 3.10 or newer for the triage script.
- Credentials: none for analysis. IDS reload rights for deployment.
- Authorization: segment owner sign-off for rule deployment. Live test traffic is gated.
- Upstream skills: `passive-ot-network-discovery` for the baseline pair list.

### Safety

This skill is passive by default. Active steps are gated in the Workflow section.

- Passive. Authors rules and analyzes captures and IDS logs. Safe to run during normal operations.

## Workflow

1. Extract the authorized master-slave pairs from the discovery baseline:
   `tshark -r baseline.pcapng -Y "modbus" -T fields -e ip.src -e ip.dst -e modbus.unit_id | sort -u > pairs.txt`
2. Author the ruleset from `references/detection-rules.md`. Fill the site variables. Every write-code rule uses the native `modbus:` keyword, not raw content matches.
3. Validate the ruleset offline:
   `suricata -T -c /etc/suricata/suricata.yaml`
   Exit code 0 and no rule-load errors are required before deployment.
4. Validate the Zeek policy offline against the baseline capture:
   `zeek -C -r baseline.pcapng scripts/modbus-anomaly`
   No script errors and a populated `modbus.log` are required.
5. Deploy the ruleset to the IDS:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   Copy the rules file to the sensor, then `suricatasc -c reload-rules`. Confirm the reload with `suricatasc -c ruleset-stats`.
6. Prove each rule fires using offline replay only:
   `suricata -r modbus-test.pcapng -c /etc/suricata/suricata.yaml -l test-output/`
   Each rule must produce its alert in `test-output/eve.json` with the expected `signature_id`. Replay captures, not live traffic.
7. Generate live test traffic only if replay cannot exercise a rule:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   `python3 -c "from pymodbus.client.sync import ModbusTcpClient; c=ModbusTcpClient('<plc-ip>', timeout=5); c.connect(); c.write_register(<addr>, 0)"` from an approved test host, to one PLC, inside the maintenance window.
8. Triage production alerts:
   `python3 scripts/modbus_triage.py /var/log/suricata/eve.json --out modbus-triage.md`
9. Tune. Any rule that fires on the 72 hour baseline is a false positive. Fix the rule or the site variable, then repeat steps 3 and 8. Do not disable rules silently.

## Verification

- Correct output: `modbus-triage.md` has one row per alert group with source, destination, unit ID, function code, first and last seen, and count. Every deployed rule has a replay test result.
- Failure mode: `suricata -T` fails on the `modbus:` keyword. The installed Suricata build lacks Modbus support. Fix the build or use raw content matches anchored per the rule-discipline notes in `references/detection-rules.md`.
- Failure mode: the write-code rules fire on every HMI poll. The HMI subnet is missing from `$HMI_SERVERS`. Fix the variable, not the rule.
- OT check: zero hits over a 72 hour baseline capture. A rule that fires during normal polling is misconfigured.
- OT check: the test-fire write in step 7 targets a scratch register on one PLC. Confirm the register value before and after, and confirm the PLC stayed in RUN (state 8).

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 6.2 | Continuous monitoring. The ruleset is the monitoring capability for the Modbus segment. |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. Write-code alerts flag integrity violations on register traffic. |
| ATT&CK for ICS | T0855 | Unauthorized Command Message. Write function codes from non-HMI sources. |
| ATT&CK for ICS | T0806 | Brute Force I/O. Register scanning rule. |
| ATT&CK for ICS | T0861 | Point and Tag Identification. Scanning and enumeration detection. |
| NIST SP 800-82r3 | SI-4 | System Monitoring. The deployed ruleset is the SI-4 sensor for Modbus. |
| NIST CSF 2.0 | DE | Detect. Family level. Site assigns specific subcategories. |

