---
name: skill-name-in-kebab-case
description: One or two sentences. State WHAT this skill does and WHEN to use it. Include OT-specific trigger keywords such as "PLC", "Modbus", "historian", "Purdue". Max 1024 characters.
version: 0.1.0
license: Apache-2.0
metadata:
  # skill_id is otics-<CATEGORY>-<name>. CATEGORY is DIS, ASM, MON, IRR, ARC, or GOV.
  skill_id: otics-DIS-skill-name-in-kebab-case
  author: your-github-username
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0800
# allowed-tools: Read Grep Bash
---

## When to Use

- Initial assessment of an unfamiliar OT network.
- Investigating anomalous <device-type> behavior reported by operators. Example: "The HMI shows a pump PLC at 100 percent with no operator input."
- <Describe the trigger condition here. Name the protocol, device class, or scenario.>
- <Add one bullet per distinct trigger. Each must name a concrete scenario an agent can match against.>

## Prerequisites

- pymodbus 3.10 or newer. Verify with `python -c "import pymodbus; print(pymodbus.__version__)"`.
- nmap 7.94 or newer with NSE OT scripts. Verify with `nmap --version`.
- SPAN port or network TAP on the target segment. If unavailable, use <passive-skill-name> instead.
- Credentials: <list accounts and scopes, and where the agent retrieves them>.
- Authorization: <named approver or approval system> sign-off before start.
- Upstream skills: <skill-name> when <condition>. Leave empty if none.

### Safety

This skill is <passive|active>.

- Passive. Captures and inspects traffic. Sends no packets. Safe to run during normal operations.
- Active. Sends packets to live devices. Requires change control approval and a tested rollback plan. Run inside an approved maintenance window.

Delete the line that does not apply.

## Workflow

1. Copy the target list from <source> to `targets.txt`. One IP per line.
2. Sweep the targets:
   `nmap -sS -Pn -p 502 -iL targets.txt -oN results/nmap_502.txt`
   If no port responds, stop and report the SPAN path as suspect.
3. Parse `results/nmap_502.txt` into `devices.csv`. Columns: `ip`, `port`, `unit`, `response_code`.
4. Query device identity:
   `mbpoll -1 -0 -a <unit_id> -t 4 -r 0 -c 1 -o 5 <ip>`
   `-1` polls once, `-0` uses PDU addressing, and `-o 5` sets a 5 second timeout.
   If the reply is unit 0xFF or the query times out, mark the row `unresponsive` and continue. Do not retry more than twice.
5. <Describe the active step here. This step sends packets to live devices.>
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
6. <Describe the decision point. State both paths with concrete codes. Example: "If the response code is 0x05, continue to step 7. If 0x0A, stop and report unauthorized function code.">
7. Produce `report.md` listing findings, evidence files, and any devices left unverified.

## Verification

- Correct output: `devices.csv` has one row per responding device, no null `unit` values, and `report.md` names an evidence file for every finding.
- Failure mode: response code 0x0A on every address. The device enforces authorization. Report the access as blocked, not as a false negative.
- Failure mode: timeouts above 30 percent of targets. Check the SPAN or TAP path before rerunning.
- OT check: confirm the PLC did not enter fault state. Read the diagnostics word and verify the fault bit is clear.
- OT check: verify historian data integrity after the operation. Compare the last 100 samples against the pre-operation snapshot.
- <Add checks specific to this skill. State expected values as concrete fields or codes.>

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 1.1 | Identification and authentication of human users. Justifies the credential check in step 2. |
| ATT&CK for ICS | T0843 | Program Download. Matches the write detection in step 6. |
| NIST SP 800-82r3 | AC-2 | Account Management. Supports the access review in step 5. |
| <Framework> | <ID> | <State which step this maps and why. Use real IDs only.> |

Row-by-row justification lives in `references/standards.md`.
