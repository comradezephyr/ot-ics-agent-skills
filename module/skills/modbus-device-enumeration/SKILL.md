---
name: modbus-device-enumeration
description: Enumerate Modbus TCP devices, unit IDs, register maps, and allowed function codes from capture and targeted reads. Use when building a register map for a segment that carries Modbus on port 502.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-DIS-modbus-device-enumeration
  author: comradezephyr
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0861
# allowed-tools: Read Grep Bash
---

## When to Use

- Building a register map for a Modbus segment with no existing documentation.
- Cataloging unit IDs and function codes before deploying a protocol monitor.
- Investigating operator reports of unexpected register writes (0x05, 0x06, 0x0F, 0x10).
- Extending a Passive OT Network Discovery inventory with register-level detail.

## Prerequisites

- tshark 4.x. Verify with `tshark --version`.
- pymodbus 3.x. Verify with `pip show pymodbus`.
- mbpoll 1.5 or newer. Verify with `mbpoll -V`.
- SPAN port or network TAP on the segment.
- Endpoint list from `passive-ot-network-discovery`, or an approved device list.
- Credentials: none for read-only queries. Some devices reject unauthenticated reads.
- Authorization: segment owner sign-off. Active reads require a maintenance window.
- Upstream skills: `passive-ot-network-discovery` for the endpoint list.

### Safety

This skill is passive by default. Active steps are gated in the Workflow section.

- Passive. Captures and inspects traffic. Sends no packets. Safe to run during normal operations.

## Workflow

1. Build `devices.txt` from the endpoint list. One IP per line.
2. Extract the passive Modbus profile from an existing capture:
   `tshark -r capture.pcapng -Y "modbus" -T fields -e ip.src -e modbus.unit_id -e modbus.func_code -e modbus.word_count | sort -u > modbus_profile.txt`
   Decision point: if a profile row shows a write function code (0x05, 0x06, 0x0F, 0x10) to an address the operator did not authorize, flag it for incident review and remove the row from the inventory set.
3. Merge `modbus_profile.txt` into `register_candidates.csv`. Key by `(ip, unit_id)`.
4. Read the register windows for units that appeared in capture but have no register data:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   `mbpoll -m tcp -a <unit_id> -t3 -r 0 -c 100 <ip>`
   Response gate: exception 0x01 means the device does not support function 0x03. Try `-t4` for input registers. If both fail, record the unit as limited and move on.
5. Run the bundled enumerator for the standard address windows:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   `python3 scripts/modbus_enumerate.py --host <ip> --unit <unit_id> --out registers.csv`
   The script reads holding and input register windows 0-9999, 10000-19999, and 30000-39999 in 125-register chunks. It records exception codes per chunk instead of stopping.
6. Decision point: exception 0x0B on every chunk means the gateway cannot reach the target. Report the unit as unreachable. Do not retry more than twice.
7. Merge active and passive data into `report.md`. One row per unit: ip, unit id, register ranges, function codes observed, source (passive or active).

## Verification

- Correct output: `report.md` has one row per unit and `registers.csv` has register values or explicit exception codes for every chunk.
- Failure mode: exception 0x0B on all reads. The Modbus gateway cannot reach the target unit. The unit may sit behind a serial bridge.
- Failure mode: timeouts on more than 30 percent of targets. The capture or span path is underprovisioned. Report, do not rerun.
- Failure mode: reads succeed but the capture shows no Modbus for that unit. The unit is alive but idle.
- OT check: confirm the PLC did not enter fault state after the reads. Read the diagnostics register from `modbus_profile.txt` and verify the fault bit is clear.
- OT check: run a post-query capture. It must show no new write function codes. A write to a register this session did not touch indicates session replay or hijack.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. The function code baseline is the expected behavior set for later monitoring. |
| IEC 62443-3-3 | SR 7.6 | Network and service availability. Reads verify each unit answers within timeout. |
| IEC 62443-4-2 | CR 3.1 | Communication integrity for the component. The skill records which functions a device actually supports. |
| ATT&CK for ICS | T0861 | Point & Tag Identification. The register map is the point map an adversary enumerates. Built here for defense. |
| ATT&CK for ICS | T0855 | Unauthorized Command Message. Write function code detection in step 2 flags candidate T0855 traffic. |
| NIST SP 800-82r3 | RA-5 | Vulnerability scanning. Read-only enumeration feeds the assessment input. |
| NIST CSF 2.0 | ID | Identify. Family level. Site assigns specific subcategories. |

Row-by-row justification lives in `references/standards.md`.
