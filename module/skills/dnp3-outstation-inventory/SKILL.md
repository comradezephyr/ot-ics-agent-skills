---
name: dnp3-outstation-inventory
description: Enumerate DNP3 outstations, data link addresses, and function code use on port 20000. Use when mapping a DNP3 SCADA segment before monitoring or firewall rule work.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-DIS-dnp3-outstation-inventory
  author: comradezephyr
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0848
# allowed-tools: Read Grep Bash
---

## When to Use

- Building the outstation list for a DNP3 segment.
- Checking which outstations answer READ and which accept SELECT or OPERATE.
- Investigating a data link address collision reported by the master.
- Baselining function code distribution before monitoring deployment.

## Prerequisites

- tshark 4.x. Verify with `tshark --version`.
- zeek 5.x. Verify with `zeek --version`.
- SPAN port or network TAP on the segment.
- nmap 7.94 or newer for the gated port confirmation.
- Credentials: none for passive capture.
- Authorization: segment owner sign-off. The gated port check needs a maintenance window.
- Upstream skills: `passive-ot-network-discovery` for the segment capture.

### Safety

This skill is passive by default. Active steps are gated in the Workflow section.

- Passive. Captures and inspects traffic. Sends no packets. Safe to run during normal operations.

## Workflow

1. Resolve the DNP3 field names for this tshark revision:
   `tshark -G fields | grep -i dnp3 | grep -iE "func|dst|src" | head -30`
   Use the resolved function code field in the commands below.
2. Passive address map:
   `tshark -r capture.pcapng -Y "dnp3" -T fields -e ip.src -e ip.dst -e dnp3.func -E separator=, | sort -u > dnp3_flat.csv`
   The endpoint receiving READ requests is the outstation. The sender is the master.
3. Function code distribution:
   `tshark -r capture.pcapng -Y "dnp3" -T fields -e ip.src -e ip.dst -e dnp3.func | sort | uniq -c | sort -rn`
   Function codes appear as decimal values. 1 is READ, 2 is WRITE, 3 is SELECT, 4 is OPERATE, 5 is DIRECT_OPERATE.
4. Zeek cross-check:
   `zeek -C -r capture.pcapng dnp3`
   `head -5 dnp3.log`
   Extract address pairs and function codes with `cut` using the column numbers from the header.
5. Decision point: a master that only READs from an outstation is normal for read-only sites. Record the fact. Do not flag it as an anomaly.
6. Confirm reachability for outstations absent from the capture window:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   `nmap -sT -Pn -p 20000 <ip>`
   This verifies the port. It does not verify DNP3 semantics.
7. Write `outstations.csv`: ip, data link address, role (master or outstation), function codes used per pair.

## Verification

- Correct output: every outstation address is mapped with its function set and a master is identified. `dnp3_flat.csv` has one row per observed pair.
- Failure mode: repeated link reset frames in the capture. A second master is contending for the outstation. Candidate rogue master.
- Failure mode: two sources answer the same data link address. Address collision. The genuine outstation may be unreachable.
- OT check: the master reports all links ONLINE after the window. Any LINK_STATUS mismatch is a field failure.
- OT check: a post-window capture shows no new persistent master sessions.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. The function set per outstation is the baseline for monitoring. |
| NIST SP 800-82r3 | CA-7 | Continuous monitoring. The outstation map is the segment baseline source. |
| ATT&CK for ICS | T0848 | Rogue Master. Link reset detection in step 5 flags matching behavior. |
| ATT&CK for ICS | T0855 | Unauthorized Command Message. Unexpected SELECT or OPERATE targets flag candidate T0855 traffic. |
| NIST CSF 2.0 | ID | Identify. Family level. Site assigns specific subcategories. |

Row-by-row justification lives in `references/standards.md`.
