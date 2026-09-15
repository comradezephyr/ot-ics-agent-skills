---
name: profinet-anomaly-detection
description: Build and run Layer 2 PROFINET detection with a Zeek policy covering DCP Set commands, duplicate device names, ARP spoofing, cycle time disruption, and missing RT frames. Use when monitoring PROFINET controller and IO device traffic.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-MON-profinet-anomaly-detection
  author: your-github-username
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0848
# allowed-tools: Read Grep Bash
---

## When to Use

- Monitoring a PROFINET segment for device rename or IP reassignment attacks.
- Hunting for duplicate device names or rogue IO devices on Layer 2.
- Investigating cycle time disruption or missing RT frames reported as network glitches.
- Detecting ARP spoofing between controllers and IO devices.

## Prerequisites

- Zeek 5.x. Verify with `zeek --version`.
- SPAN of the PROFINET VLAN. PROFINET RT and DCP are Layer 2. The span must carry full Ethernet frames, not just IP.
- Device name and MAC inventory from `profinet-device-inventory`.
- Packet capture of at least one full production cycle window for baseline statistics.
- tshark 4.x for capture analysis.
- Credentials: none. Layer 2 detection reads frames.
- Authorization: network owner sign-off for policy deployment.
- Upstream skills: `profinet-device-inventory` for the device name and MAC baseline.

### Safety

This skill is passive by default. Active steps are gated in the Workflow section.

- Passive. Deploys a Zeek policy and analyzes captures. Safe to run during normal operations.

## Workflow

1. Capture the baseline on the PROFINET VLAN:
   `sudo tshark -i <iface> -Y "pn_rt or pn_dcp" -w pn-baseline.pcapng -b filesize:1048576 -a duration:1800`
2. Extract the device name announcements and MACs:
   `tshark -r pn-baseline.pcapng -Y "pn_dcp && pn_dcp.service_id == 5" -T fields -e eth.src -e pn_dcp.device_name | sort -u > dcp-names.txt`
   DCP service ID 5 is Identify. Every legitimate device announces here.
3. Compute RT frame cycle statistics per controller-device pair:
   `tshark -r pn-baseline.pcapng -Y "pn_rt" -T fields -e eth.src -e eth.dst -e frame.time_epoch | sort -u > rt-frames.txt`
   Convert to inter-arrival deltas with the bundled analysis or a short python script. Record the mean and standard deviation per pair.
4. Deploy the Zeek policy from `references/detection-rules.md` into the Zeek site scripts directory:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   Copy `profinet-detection-rules.zeek` to `site/` and reload Zeek with `zeekctl deploy`.
5. Prove the policy fires using offline replay only:
   `zeek -C -r pn-anomaly-test.pcapng site/profinet-detection-rules.zeek`
   Build the test capture on a bench segment: a DCP SET NAME with a duplicate name, an ARP reply pair with conflicting MACs, and a truncated RT stream.
6. Triage production output. Zeek writes `profinet-anomaly.log`. Each entry names the anomaly class: `dcp_set`, `duplicate_name`, `arp_conflict`, `cycle_disruption`, `rt_gap`.
7. Decision point: a `dcp_set` or `duplicate_name` entry on a production device is a High finding. Escalate to incident response. A `cycle_disruption` entry is first a network fault candidate, then a security candidate. Check switch error counters before escalating.
8. Record the baseline file and the policy version deployed. Rerun the baseline after every legitimate device change.

## Verification

- Correct output: `profinet-anomaly.log` exists after policy deployment, and every anomaly class in the policy has a replay test result recorded.
- Failure mode: no `profinet-anomaly.log` after deployment. The span is not carrying Layer 2 frames. Verify with `tshark -i <iface> -Y "ether proto 0x8892" -c 5`. An IP-only span misses DCP and RT entirely.
- Failure mode: `cycle_disruption` entries during a production ramp. Motor starts change RT load. Compare against the baseline statistics before treating it as an attack.
- OT check: zero `dcp_set` and `duplicate_name` entries over a 24 hour baseline. Legitimate commissioning is the only authorized source. Confirm the commissioning window with the controls engineer.
- OT check: confirm no RT frame gap beyond 3 standard deviations persists across a full shift. A persistent gap means the loop is degraded. Escalate to the controls engineer as a process safety input.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 6.2 | Continuous monitoring. The Zeek policy is the monitoring capability for the PROFINET segment. |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. DCP Set and duplicate name detection guard device identity integrity. |
| IEC 62443-3-3 | SR 7.6 | Network and service availability. Cycle disruption and RT gap detection guard IO availability. |
| ATT&CK for ICS | T0848 | Rogue Master. Duplicate device names and rogue IO devices. |
| ATT&CK for ICS | T0881 | Service Stop. DCP Set commands that reassign or rename devices take IO out of service. |
| NIST SP 800-82r3 | SI-4 | System Monitoring. The deployed policy is the SI-4 sensor for Layer 2. |
| NIST CSF 2.0 | DE | Detect. Family level. Site assigns specific subcategories. |

