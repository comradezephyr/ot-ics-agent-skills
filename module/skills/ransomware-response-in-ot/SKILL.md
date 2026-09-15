---
name: ransomware-response-in-ot
description: Respond to ransomware in an OT environment without shutting down production, isolating only affected systems and preserving controller and historian operations. Use when ransomware indicators appear on SCADA, HMI, historian, or Purdue L3 systems.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-IRR-ransomware-response-in-ot
  author: your-github-username
  frameworks:
    - IEC 62443-2-1
    - NIST SP 800-82r3
    - ATT&CK for ICS T0880
# allowed-tools: Read Grep Bash
---

## When to Use

- Ransomware indicators on an OT host: renamed files, ransom notes, encrypted historian archives.
- Ransomware confirmed in IT or the DMZ with any path into OT.
- Reports from operators of unreadable HMI screens or corrupt project files.
- Enterprise SOC notification of ransomware in a shared service.

## Prerequisites

- Zone and conduit map with Purdue levels for every affected host.
- Approved conduit list from `ot-firewall-rule-review`.
- Backup inventory: what is backed up, where, and whether the backup is offline.
- Emergency contact list: operations manager, safety engineer, IT SOC, vendor contacts.
- Firewall or VLAN access to apply isolation changes.
- Credentials: read-only on OT hosts for confirmation, admin on the boundary firewall for isolation.
- Authorization: operations manager approves isolation. IT security lead owns enterprise-side containment.
- Upstream skills: `ot-network-isolation-procedure` for the isolation mechanics. This skill decides, that skill executes.

### Safety

This skill is active. Isolation changes a live system and is gated in the Workflow section.

- Active. Applies firewall or VLAN changes to live segments. Requires operations manager approval. Human safety and process integrity outrank containment.

## Workflow

> SAFETY: If at any point the action risks human safety or process integrity, halt and escalate to the operations lead before continuing.

1. Confirm the decision authority. The operations manager owns any action that touches a running process. Record the name and contact at the top of the incident record. Do not proceed without one.
2. Confirm ransomware presence without shutting anything down. Check for renamed file clusters, ransom notes, encrypted extensions, or extortion contact. Do not power off the suspected host yet. A powered-off host loses volatile evidence.
3. Classify affected systems using `references/decision-matrix.md`:
   - Zone 1: IT only. No OT impact path.
   - Zone 2: DMZ or L4, with a conduit into OT.
   - Zone 3: OT L3 systems, historian, domain controller, engineering network.
   - Zone 4: OT L1 or L2 controllers or HMIs.
   Record the zone per affected host. Zone 4 changes the response priority to process protection.
4. Zone 3 or 4 decision point: before any isolation, answer two questions with the operations manager.
   - Does the process depend on the affected host for control, visualization, or data?
   - What happens if the host goes offline for one hour?
   If the answer to the second question is unsafe or unknown, isolate at the network layer only and keep the host running.
5. Isolate affected OT systems at the network layer:
   > STOP: Confirm change control approval and operations manager sign-off before executing this step. If approval is missing, halt and report.
   Apply a firewall deny or VLAN move between the affected host and the rest of OT. Never power off a host that a process depends on. This step will interrupt process if the host feeds a control loop. Confirm with operations before proceeding.
6. Cut the IT-to-OT paths before anything else. Suspend any enterprise-side backup or replication process that writes INTO OT systems or reads FROM OT systems to the enterprise. Do not suspend offline backups of OT systems. The recovery point must survive the response. Also disable remote access paths from L4. These cuts do not touch process control. This is the highest-value containment move in OT ransomware.
7. Preserve unaffected OT operations. Confirm from the boundary firewall that controller-to-controller and HMI-to-controller traffic is still flowing:
   `tshark -i <iface> -c 20 -Y "tcp.port == 502 or tcp.port == 102 or tcp.port == 44818"`
   Zero controller traffic after isolation means the cut was too broad. Roll back the last rule immediately.
8. Block lateral movement paths. Deny SMB and RDP crossing from affected zones to unaffected zones. Ransomware spreads over SMB. This is a targeted deny, not a general lockdown.
9. Identify the safe recovery point. Use the most recent verified offline backup. Do not trust backups mounted on the network. Confirm backup integrity with `sha256sum -c` before any restore decision.
10. Coordinate with IT on enterprise containment. Share indicators of compromise. Do not let IT push enterprise-wide actions into OT without operations manager review. An enterprise credential reset can lock out OT service accounts and stop the process.
11. Produce `ransomware-response-record.md`. Sections: decision authority, affected systems by zone, isolation actions with timestamps, process continuity status, recovery point, IT coordination log.

## Verification

- Containment confirmed: the affected host has no network path to unaffected OT zones, IT-to-OT sync paths are suspended, and the boundary firewall shows the denies active.
- Process safety confirmed: controller traffic flows at the baseline rate, controllers respond to operator commands, and the process shows no new interlock trips. A trip after isolation is a containment failure even if the malware is contained.
- No new problems confirmed: the isolation deny list matches only the affected hosts, no unaffected host lost connectivity, and historian writes from live collectors continue. An accidental over-block is a new problem introduced by the response.
- OT check: SIS and safety systems show no new bypasses or overrides after the response began. Ransomware response actions must not touch safety systems.
- OT check: backup restore point verification completed before any restore is scheduled. Restoring from an infected backup restarts the incident.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-2-1 | 4.3.4.5 | Incident response. This skill is the OT ransomware response procedure. |
| IEC 62443-3-3 | SR 7.1 | Denial of service protection. Isolation decisions balance containment against process availability. |
| IEC 62443-3-3 | SR 7.2 | Resource management. Recovery point selection protects backup resources from re-infection. |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. Encrypted or renamed files are integrity violations. |
| NIST SP 800-82r3 | IR-4 | Incident Handling. The workflow is the handling procedure for OT ransomware. |
| NIST SP 800-82r3 | IR-5 | Incident Monitoring. Process continuity checks track incident status. |
| NIST SP 800-82r3 | CP-9 | System Backup. Recovery point selection uses CP-9 backup controls. |
| NIST SP 800-82r3 | CP-10 | System Recovery. The restore path is the CP-10 action. |
| NIST CSF 2.0 | RS | Respond. Family level. Site assigns specific subcategories. |
| ATT&CK for ICS | T0880 | Loss of Safety. Ransomware or response actions that touch safety systems. |
| ATT&CK for ICS | T0881 | Service Stop. Over-broad isolation is a self-inflicted service stop. |
| ATT&CK for ICS | T0886 | Remote Services. Ransomware staging through remote access paths. |
| ATT&CK for ICS | T0889 | Modify Program. Ransomware on engineering stations can corrupt project files. |

