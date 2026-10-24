---
name: passive-ot-network-discovery
description: Passively captures and analyzes OT traffic from a SPAN port or TAP to inventory PLCs, HMIs, and historians. Use when assessing an unfamiliar OT network segment where active scanning is not approved.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-DIS-passive-ot-network-discovery
  author: comradezephyr
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0842
# allowed-tools: Read Grep Bash
---

## When to Use

- Initial assessment of an unfamiliar OT network where no asset list exists.
- Baseline capture before an active assessment or a firewall rule review.
- Investigating anomalous PLC or historian behavior reported by operators.
- Validating an existing inventory against observed traffic.
- Rogue device hunt. Rogue devices appear as unknown MACs, unknown IPs, or duplicate IPs.

## Prerequisites

- tshark 4.x. Verify with `tshark --version`.
- zeek 5.x. Verify with `zeek --version`.
- scapy 2.5 or newer. Verify with `python -c "import scapy; print(scapy.__version__)"`.
- SPAN port or network TAP on the target segment. Without a TAP the capture is incomplete.
- Capture storage. Budget 1 GB per hour per 100 Mbps of span utilization.
- Root or Administrator rights on the capture host. Required to open the interface.
- Credentials: none for the capture itself.
- Authorization: written approval from the segment owner before the first frame is captured.
- Upstream skills: none.
- nmap 7.94 or newer with NSE OT scripts. Only required for the gated identity confirmation step.

### Safety

This skill is passive by default. Active steps are gated in the Workflow section.

- Passive. Captures and inspects traffic. Sends no packets. Safe to run during normal operations.

## Workflow

1. Verify the capture interface and the span:
   `ip link show <iface>`
   `tcpdump -i <iface> -c 10 -nn`
   If tcpdump prints nothing after 30 seconds, the SPAN or TAP is not delivering frames. Stop here.
2. Start the capture:
   `sudo tshark -i <iface> -f "tcp port 502 or tcp port 20000 or tcp port 4840 or tcp port 44818 or tcp port 102 or udp port 2222 or udp port 20000 or udp port 4840 or ether proto 0x8892" -w capture.pcapng -b filesize:1048576 -a duration:3600`
   Rotation prevents disk exhaustion on long captures. The `-a duration` flag stops the capture at 3600 seconds regardless of file rotation.
   Alternative capture with the bundled scapy script. It does not rotate. It writes a single output file:
   `sudo python3 scripts/ot_capture.py -i <iface> -o capture.pcapng -d 3600`
3. Confirm the capture produces data. Wait 60 seconds, then:
   `tshark -r capture.pcapng -q -z io,stat,0`
   If the packet counter is zero, recheck the SPAN or TAP. Do not analyze an empty capture.
4. Extract candidate assets:
   `tshark -r capture.pcapng -T fields -e eth.src -e ip.src -e ip.dst -E separator=, | sort -u > hosts.csv`
5. Build the Modbus profile:
   `tshark -r capture.pcapng -Y "modbus" -T fields -e ip.src -e modbus.unit_id -e modbus.func_code | sort -u > modbus_profile.txt`
   Decision point: if a write function code (0x05 single coil, 0x06 single register, 0x0F multiple coils, 0x10 multiple registers) targets an address the operator did not authorize, flag the row for incident review. Do not place it in the inventory.
6. Build the DNP3 outstation profile:
   `tshark -r capture.pcapng -Y "dnp3" -T fields -e ip.src -e ip.dst -e dnp3.func | sort | uniq -c`
   Function codes appear as decimal values. 1 is READ, 2 is WRITE, 3 is SELECT, 4 is OPERATE, 5 is DIRECT_OPERATE.
7. Cross-check with zeek analyzers:
   `zeek -C -r capture.pcapng modbus dnp3 enip`
   Correct output: `conn.log` plus `modbus.log`, `dnp3.log`, and `enip.log` when those analyzers fire. `-C` ignores link-layer checksum errors, which are common on span taps.
8. Optional identity confirmation. Use only for devices passive data could not type:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   `sudo nmap -sV -Pn -p 502,44818 --script modbus-discover,enip-info <ip>`
   Run for one or two devices at most. Requires a maintenance window. nmap has no OPC UA discovery script, so servers on 4840 go to `opc-ua-endpoint-discovery` instead.
9. Write `inventory.md`. One row per asset. Columns: MAC, IP, protocols, role, Purdue level. Role inference rules:
   - PLC: Modbus, DNP3, or S7 port 102 server. Purdue L1.
   - HMI or EWS: initiates many 502, 20000, or 102 sessions toward multiple servers. Purdue L2.
   - Historian: polls many 502 or 20000 sources, or runs an OPC UA server on 4840. Purdue L3.
   - DMZ service: remote access gateway reached from L4. Purdue L3.5.
   - Mark unresolved rows `role: unknown`. Do not guess.

## Verification

- Correct output: `inventory.md` has one row per asset with MAC, IP, protocols, role, and Purdue level. `hosts.csv` and `capture.pcapng` exist. `capinfos capture.pcapng` reports a nonzero `Number of packets`.
- Failure mode: the io,stat counter stays zero for 60 seconds. The SPAN or TAP is not attached. An empty capture is not evidence of an empty network.
- Failure mode: the capture stops early with no rollover file. Disk filled. Rotation with `-b filesize:1048576` prevents this on long captures.
- Failure mode: many assets end as `role: unknown`. Passive data alone cannot type the segment. Use the gated NSE step for the untyped devices.
- OT check: the capture host sent no packets during the window. `tshark -r capture.pcapng -Y "ip.src == <capture-ip> and tcp.flags.syn == 1"` must return no rows.
- OT check: rerun the capture 24 hours later and diff `hosts.csv`. A stable asset set confirms the segment is not churning. New MACs on the second run are candidate rogue devices.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 5.1 | Network segmentation. The inventory defines zone and conduit boundaries on L0 through L3.5. |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. The capture builds the expected protocol baseline for the segment. |
| NIST SP 800-82r3 | CA-7 | Continuous monitoring. The capture is the baseline source for the segment. |
| NIST SP 800-82r3 | SC-7 | Boundary protection. Flow data drives boundary rule definition. |
| ATT&CK for ICS | T0842 | Network Sniffing. The captured telemetry is the same data used to detect unauthorized sniffing. |
| NIST CSF 2.0 | ID | Identify. Family level. CSF subcategories are site specific and not pinned by this skill. |

Row-by-row justification lives in `references/standards.md`.
