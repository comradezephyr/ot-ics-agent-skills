---
name: ot-network-isolation-procedure
description: Isolate a compromised OT network segment with minimal process impact, covering boundary selection, process flow enumeration, operations notification, firewall or VLAN enforcement, and two-sided verification. Use when a segment must be cut from OT.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-IRR-ot-network-isolation-procedure
  author: your-github-username
  frameworks:
    - IEC 62443-2-1
    - NIST SP 800-82r3
    - ATT&CK for ICS T0881
# allowed-tools: Read Grep Bash
---

## When to Use

- Isolating a compromised segment from the rest of OT during an incident.
- Executing an isolation decision from `ot-incident-triage` or `ransomware-response-in-ot`.
- Cutting a DMZ or L3 host away from controllers.
- Post-compromise quarantine of any OT zone.

## Prerequisites

- Zone and conduit map with Purdue levels.
- Observed flow baseline from `passive-ot-network-discovery` showing which process flows cross the proposed boundary.
- Firewall or switch configuration access for the boundary device.
- Operations manager contact available for the isolation decision.
- Credentials: admin on the boundary firewall or switch.
- Authorization: operations manager approves every isolation. The safety engineer confirms process flows that cross the boundary are not safety-critical.
- Upstream skills: `ot-incident-triage` or `ransomware-response-in-ot` for the decision record.

### Safety

This skill is active. Isolation changes live network enforcement and is gated in the Workflow section.

- Active. Applies firewall or VLAN changes to live segments. Requires operations manager approval. A wrong boundary is a process outage.

## Workflow

> SAFETY: If at any point the action risks human safety or process integrity, halt and escalate to the operations lead before continuing.

1. Confirm the decision authority and the isolation scope. The operations manager approves the boundary. Record the approved boundary in the report before any change.
2. Identify the isolation boundary. List the subnets, VLANs, or firewall zones on each side. The boundary must match a zone boundary from the zone map. Isolating across a zone boundary splits a control function.
3. Enumerate the process flows that cross the boundary from the discovery baseline:
   `tshark -r baseline.pcapng -Y "ip.addr == <isolated-subnet>" -T fields -e ip.src -e ip.dst -e _ws.col.Protocol | sort -u`
   For each flow, record whether the process depends on it. Flows the safety engineer marks safety-critical change the boundary, not the decision.
4. Notify operations. The control room must know which visualization, data, or control paths will drop. Record the notification time. Never isolate without the control room aware.
5. Apply the isolation:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   Apply the firewall deny or move the port to the quarantine VLAN. Prefer explicit denies over broad cuts. One rule per flow direction, reversible, with the rollback noted in the change record.
6. Verify the isolated segment cannot reach controllers:
   `ping -c 3 <controller-ip>` from a host in the isolated segment, or read the firewall deny counters.
   Counters incrementing on every deny rule confirms the enforcement is live.
7. Verify the controllers are still reachable from the control room:
   `tshark -i <iface> -c 20 -Y "tcp.port == 502 or tcp.port == 102 or tcp.port == 44818"`
   Controller traffic at baseline rate from the control room side confirms the cut did not touch the control path.
8. Confirm process state with the control room. Process values inside the operating band, no new interlock trips, operators on the expected screens.
9. Produce `isolation-record.md`. Sections: decision authority, approved boundary, crossing flows and their process impact, notification time, rules applied with timestamps, both verification results, rollback rules.

## Verification

- Containment confirmed: deny counters increment on the boundary device, no session from the isolated segment reaches a controller, and the enforcement survives a firewall policy reload.
- Process safety confirmed: controllers respond to the control room, process values stay in the operating band, and no new interlock trips occur after the change.
- No new problems confirmed: no flow outside the approved boundary was cut, the control room retains every path it had before except the isolated segment, and the rollback rules are tested and documented.
- OT check: a safety-critical flow that crossed the boundary was either moved to a backup path or the isolation was redesigned. Cutting a safety-critical flow silently is an isolation failure even if the containment succeeded.
- OT check: the isolated segment's own controllers, if any, stayed in RUN (8) throughout. A controller in the isolated segment that dropped to STOP means the boundary cut something it should not have.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-2-1 | 4.3.4.5 | Incident response. Isolation is a defined containment action. |
| IEC 62443-3-3 | SR 5.2 | Zone boundary protection. The isolation enforces a zone boundary under incident conditions. |
| IEC 62443-3-3 | SR 7.1 | Denial of service protection. The two-sided verification bounds the denial to the isolated segment. |
| IEC 62443-3-3 | SR 7.6 | Network and service availability. The control room path check preserves service availability. |
| NIST SP 800-82r3 | IR-4 | Incident Handling. The gated procedure is the handling action. |
| NIST SP 800-82r3 | SC-7 | Boundary Protection. The deny rules implement SC-7 enforcement under incident conditions. |
| NIST CSF 2.0 | RS | Respond. Family level. Site assigns specific subcategories. |
| ATT&CK for ICS | T0881 | Service Stop. The rollback rules and process check prevent a self-inflicted service stop. |
| ATT&CK for ICS | T0885 | Commonly Used Port. Isolation rules keyed on the OT protocol ports rather than blanket denies. |

