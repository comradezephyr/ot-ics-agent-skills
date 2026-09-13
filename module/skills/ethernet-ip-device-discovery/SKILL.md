---
name: ethernet-ip-device-discovery
description: Enumerate EtherNet/IP (CIP) devices on TCP 44818 and UDP 2222, capture identity responses, and map the CIP object model. Use when building the CIP asset list for a Rockwell or third-party CIP segment.
version: 0.1.0
license: Apache-2.0
metadata:
  author: your-github-username
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0846
# allowed-tools: Read Grep Bash
---

## When to Use

- Building the CIP-side asset list for a segment.
- Checking which devices expose port 44818 and what identity they advertise.
- Investigating connection storms or unknown CIP nodes reported by the controller.
- Pre-firewall-review flow inventory on an EtherNet/IP island.

## Prerequisites

- tshark 4.x. Verify with `tshark --version`.
- nmap 7.94 or newer with the `enip-info` NSE script.
- SPAN port or network TAP on the island.
- Credentials: none for List Identity or Identity Object reads.
- Authorization: segment owner sign-off for active identity queries.
- Upstream skills: `passive-ot-network-discovery` for the flow baseline.

### Safety

This skill is passive by default. Active steps are gated in the Workflow section.

- Passive. Captures and inspects traffic. Sends no packets. Safe to run during normal operations.

## Workflow

1. Resolve the ENIP and CIP field names for this tshark revision:
   `tshark -G fields | grep -iE "enip|cip" | head -40`
   Use the resolved names in the commands below.
2. Passive flow map:
   `tshark -r capture.pcapng -Y "enip or cip" -T fields -e ip.src -e ip.dst -e tcp.port -E separator=, | sort -u > cip_flows.csv`
3. Extract List Identity responses where present:
   `tshark -r capture.pcapng -Y "enip.command == 0x0063" -T fields -e ip.src -e <resolved-identity-field> | sort -u > identity.txt`
   Decision point: if no List Identity frames exist, the segment has no UDP 2222 broadcast identity traffic in the window. Do not treat it as an empty segment.
4. Query the Identity Object for 44818 listeners missing from the passive data:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   `sudo nmap -sT -Pn -p 44818 --script enip-info <ip>`
5. Decision point: if enip-info returns no identity on an open port, the device requires a full Register Session before identity reads. Record it as `session-gated` and run `sudo nmap -sV -Pn -p 44818 <ip>` for the banner.
6. Write `report.md`: IP, product name, vendor, device type, open TCP sessions from capture, session-gated flag.

## Verification

- Correct output: every 44818 listener has a product name and vendor, or a `session-gated` flag. `cip_flows.csv` lists all detected CIP flows.
- Failure mode: enip-info reports an open port but no identity. The device enforces Register Session. Do not mark it as a false negative.
- Failure mode: UDP 2222 List Identity answers nothing. Some controllers disable broadcast identity. Use the TCP path for those devices.
- OT check: after the queries, read the controller fault queue from the HMI. New major faults indicate the query opened a faulted service.
- OT check: a post-query capture shows the two expected query sessions and no sustained 44818 connection left open.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 5.1 | Network segmentation. The CIP island inventory defines zone boundaries. |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. The flow map is the expected CIP session baseline. |
| NIST SP 800-82r3 | SC-7 | Boundary protection. 44818 and 2222 exposure drives boundary rules. |
| ATT&CK for ICS | T0846 | Remote System Discovery. Identity queries are the same discovery an adversary runs. |
| NIST CSF 2.0 | ID | Identify. Family level. Site assigns specific subcategories. |
