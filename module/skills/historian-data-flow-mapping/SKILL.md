---
name: historian-data-flow-mapping
description: Map data flows between PLCs, HMIs, and historians such as OSIsoft PI, Honeywell PHD, Wonderware Historian, and Ignition. Use when auditing which sources feed each historian and confirming L3 placement.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-DIS-historian-data-flow-mapping
  author: comradezephyr
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0811
# allowed-tools: Read Grep Bash
---

## When to Use

- Identifying which devices feed which historian.
- Reviewing cross-zone links from L3 historians into L1 and L2 zones.
- Pre-change review before a historian replacement or interface migration.

## Prerequisites

- tshark 4.x. Verify with `tshark --version`.
- zeek 5.x. Verify with `zeek --version`.
- SPAN port or network TAP on the historian subnet and the source subnets.
- Credentials: none for passive flow analysis.
- Authorization: operations sign-off to place a TAP at L3.
- Upstream skills: `passive-ot-network-discovery` for role placement.

### Safety

This skill is passive by default. Active steps are gated in the Workflow section.

- Passive. Captures and inspects traffic. Sends no packets. Safe to run during normal operations.

## Workflow

1. Extract flow pairs:
   `tshark -r capture.pcapng -T fields -e ip.src -e ip.dst -e tcp.dstport -e udp.dstport -E separator=, | sort -u > flow_pairs.csv`
2. Summarize the TCP and UDP conversations:
   `tshark -r capture.pcapng -q -z conv,tcp | head -80`
   `tshark -r capture.pcapng -q -z conv,udp | head -40`
3. Cross-check protocol split with zeek:
   `zeek -C -r capture.pcapng`
   `zeek-cut id.orig_h id.resp_h service conn.log | sort | uniq -c | sort -rn > zeek_services.txt`
4. Run the bundled aggregation script:
   `sh scripts/flow_report.sh capture.pcapng`
   Output file `flows.txt` lists src-dst-protocol/port pairs sorted by packet count.
5. Identify historians. A host that receives sustained 502, 20000, 44818, 4840, or 102 reads from many L1/L2 sources is a collector. Match the host name against the historian list (OSIsoft PI, Honeywell PHD, Wonderware Historian, Ignition).
6. Assign placement. Historians sit at L3. If the historian fronts remote access, it sits at L3.5 behind the DMZ.
7. Decision point: any flow from a historian IP to a PLC carrying write function codes (Modbus 0x05, 0x06, 0x0F, 0x10) is a violation. Flag it.
8. Write `report.md`. One row per historian: name, IP, placement, source list, protocols, and any cross-zone violation flags.

## Verification

- Correct output: every historian row lists sources and placement, and the flow counts balance against the capture totals.
- Failure mode: a historian shows no sources. Its interface runs unsampled protocols, or the capture missed the interface subnet.
- Failure mode: an L3.5 DMZ host talks directly to L1. Zone violation. The relay or historian is mislocated.
- OT check: compare historian sample timestamps with the capture clock. Lag under 5 minutes is healthy. Lag over 1 hour means the interface is failing.
- OT check: no writes from the historian direction toward PLCs. Historians must not issue writes. Flag any 0x05, 0x06, or 0x10 from a historian IP.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 5.1 | Network segmentation. Historian placement at L3 or L3.5 is validated by the flow map. |
| IEC 62443-3-3 | SR 7.6 | Network and service availability. Source reachability is verified per historian. |
| NIST SP 800-82r3 | SC-7 | Boundary protection. Cross-zone historian links are flagged as boundary violations. |
| ATT&CK for ICS | T0811 | Data from Information Repositories. The flow map shows where historian data lives and who reaches it. |
| ATT&CK for ICS | T0882 | Theft of Operational Information. Unexpected consumers of historian streams are flag candidates. |
| NIST CSF 2.0 | ID | Identify. Family level. Site assigns specific subcategories. |

Row-by-row justification lives in `references/standards.md`.
