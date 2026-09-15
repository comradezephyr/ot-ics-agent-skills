---
name: profinet-device-inventory
description: Discover and fingerprint PROFINET devices on Layer 2 through DCP frames, then verify them with the profinet-cm-lookup NSE script. Use when a PROFINET island has no controller device list.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-DIS-profinet-device-inventory
  author: your-github-username
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0846
# allowed-tools: Read Grep Bash
---

## When to Use

- A PROFINET island with no controller-supplied device list.
- A segment that runs only PROFINET (Ethertype 0x8892) with no IP layer to scan.
- A duplicate station name conflict reported by the IO controller.
- Validating station names against the IO supervisor configuration.

## Prerequisites

- tshark 4.x. Verify with `tshark --version`.
- nmap 7.94 or newer with the `profinet-cm-lookup` NSE script.
- SPAN port or network TAP on the island.
- No IP address is required. DCP runs at Layer 2.
- Credentials: none.
- Authorization: segment owner sign-off. The DCP identity burst is an active Layer 2 step and needs a maintenance window.
- Upstream skills: `passive-ot-network-discovery` for the segment capture.

### Safety

This skill is passive by default. Active steps are gated in the Workflow section.

- Passive. Captures and inspects traffic. Sends no packets. Safe to run during normal operations.

## Workflow

1. Resolve the DCP field names for this tshark revision:
   `tshark -G fields | grep -i nameofstation`
   `tshark -G fields | grep -i pn_dcp`
   Field names change across tshark releases. Use the resolved names in the commands below.
2. Passive device list from a capture that holds controller boot or address-resolver traffic:
   `tshark -r capture.pcapng -Y "pn_dcp" -T fields -e eth.src -e <nameofstation-field> | sort -u > dcp_devices.txt`
3. Decision point: if no DCP frames exist in the capture, the island has no station naming traffic in the window. Do not treat the list as empty. Record the window as DCP-silent.
4. Run the DCP identity burst only when the passive list is incomplete:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   `sudo nmap --script profinet-cm-lookup -v <ip-of-any-host-on-the-island>`
   The script broadcasts a DCP Identify Request and lists every answering device. The target IP is only a trigger for the broadcast.
5. Merge passive and burst results into `inventory.md`. Columns: MAC, station name, role (IO controller, IO device, supervisor), DCP response source.
6. Confirm every IO device appears in cyclic IO data in the capture. A device that answers DCP but never appears in cyclic frames is not in normal operation.

## Verification

- Correct output: `inventory.md` lists every answering MAC and station name, and every IO device appears in cyclic IO data.
- Failure mode: the DCP burst returns nothing. Broadcast is filtered by the switch, or the island is VLAN isolated. DCP requires membership in the same Layer 2 broadcast domain.
- Failure mode: two MACs answer with the same station name. The IO controller cannot resolve duplicates. Flag it for arbitration. This is a name conflict, not an inventory hit.
- OT check: after the burst, rerun the capture and confirm cyclic IO data flows to every inventoried device. Missing cyclic frames mean the burst disrupted a neighbor relation.
- Failure mode: a device stops answering DCP after the burst. Some devices rate-limit DCP. Wait and retry once, then report.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 5.1 | Network segmentation. The island inventory defines the L1/L2 zone boundary. |
| NIST SP 800-82r3 | SC-7 | Boundary protection. DCP broadcast scope marks the practical zone boundary. |
| ATT&CK for ICS | T0846 | Remote System Discovery. DCP enumeration is the same Layer 2 discovery an adversary runs. |
| NIST CSF 2.0 | ID | Identify. Family level. Site assigns specific subcategories. |
