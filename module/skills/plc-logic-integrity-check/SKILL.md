---
name: plc-logic-integrity-check
description: Compare running PLC logic against a known-good baseline using snap7 uploads, vendor compare tools, and register-level checks. Use when verifying that no unauthorized program change hit a controller.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-ASM-plc-logic-integrity-check
  author: comradezephyr
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0889
# allowed-tools: Read Grep Bash
---

## When to Use

- Verifying that no unauthorized program change hit a controller.
- Capturing a known-good baseline before a firmware or logic change.
- Investigating process behavior that does not match the operator control narrative.
- Closing out a change record that claims a program download.

## Prerequisites

- python-snap7 1.3 or newer. Verify with `python -c "import snap7; print(snap7.__version__)"`.
- Network route to the controller and the correct rack and slot numbers.
- Known-good baseline from a previous approved capture.
- Connection type: S7-300/400 use 1. S7-1200/1500 use 3 via `client.set_connection_type(3)`.
- Vendor tools where applicable: TIA Portal online compare, Studio 5000 Compare Tool. Optional cross-check.
- plcscan for legacy S7 devices. Optional. Check `python3 plcscan.py --help` for the installed flag set.
- pymodbus 3.x for register-level checks on Modbus controllers.
- Credentials: engineering access where the controller enforces it.
- Authorization: change control approval. Every step that touches the controller is active.
- Upstream skills: `passive-ot-network-discovery` for the reachable controller list.

### Safety

This skill is active. Every step that touches the controller is gated in the Workflow section.

- Active. Sends requests to live PLCs. Requires change control approval and a tested rollback plan. Run inside an approved maintenance window.

## Workflow

1. Verify the baseline hash files before any online step:
   `cd baseline && sha256sum -c *.sha256 && cd ..`
   If verification fails, rebuild the baseline inside the same maintenance window. Never compare against a corrupt baseline.
2. Confirm the CPU identity online:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   `python3 -c "import snap7; c=snap7.client.Client(); c.Connect('<ip>',0,<slot>); print(c.GetCpuInfo().ModuleTypeName)"`
   Record the module type and CPU state. Proceed only when the CPU is in RUN (8).
3. Capture a fresh baseline when none exists or when the change is intentional:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   `python3 scripts/plc_logic_integrity.py --ip <ip> --rack 0 --slot 1 --blocks OB1 DB1 DB100 --baseline-dir baseline/ --capture`
   Correct output: `baseline/DB1.bin` and `baseline/DB1.sha256` for every requested block.
4. Run the compare:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   `python3 scripts/plc_logic_integrity.py --ip <ip> --rack 0 --slot 1 --blocks OB1 DB1 DB100 --baseline-dir baseline/ --out logic-integrity-report.md`
5. Decision point: a block reported NEW has no baseline file. Confirm with the operator that a change record covers it. If no record exists, escalate to incident.
6. Vendor online compare where the site requires it. TIA Portal: Online and Diagnostics, then Compare. Studio 5000: Logic, Compare Tool. Document the vendor result as a cross-check on the hash method.
7. Register-level check for Modbus controllers that do not expose S7 blocks:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   `python3 -c "from pymodbus.client.sync import ModbusTcpClient; c=ModbusTcpClient('<ip>', timeout=5); c.connect(); print(c.read_holding_registers(40000, 10, device_id=1).registers)"`
   Compare the returned setpoints against `baseline/registers-40000.csv`. Values outside tolerance are findings.
8. Write `logic-integrity-report.md`. Per block: name, type, size, sha256, status (MATCH, MISMATCH, or NEW), CPU identity, start and end CPU state, overall PASS or FAIL, and the change record cross-reference.

## Verification

- Correct output: the report lists every requested block with a status of MATCH, MISMATCH, or NEW. Start and end CPU state both read 8. Baseline hashes verified in step 1.
- Failure mode: Upload fails with an access error on every block. The controller enforces engineering access. Report as access-restricted, not as tampered.
- Failure mode: MISMATCH on a block with no matching change record. Candidate unauthorized program modification. Escalate per the incident plan.
- OT check: start and end CPU state must both be RUN (8). A drop to STOP (4) means the pass took the process down.
- OT check: the change counter from step 5 must match the change record timestamp. A block that changed outside the recorded window is a finding.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. The compare is the integrity check on the running program set. |
| IEC 62443-3-3 | SR 2.8 | Auditable events. The report, baseline hashes, and CPU state form the audit record. |
| ATT&CK for ICS | T0889 | Modify Program. A MISMATCH outside a change record is the detection signal for logic tampering. |
| ATT&CK for ICS | T0843 | Program Download. The compare detects the state a download leaves behind. |
| NIST SP 800-82r3 | SI-7 | Software, firmware, and information integrity. Hash comparison is the SI-7 control action for PLC programs. |
| NIST CSF 2.0 | PR | Protect. Family level. Site assigns specific subcategories. |

Row-by-row justification lives in `references/standards.md`.
