# Ransomware Response Decision Matrix

Classification and branching for the response workflow. The operations manager makes every decision that touches a running process.

## Zone Classification

| Zone | Definition | Default Response |
| --- | --- | --- |
| 1 | IT only, no conduit to OT | IT SOC leads. Monitor the OT boundary for spread. No OT isolation. |
| 2 | DMZ or L4 with a conduit into OT | Suspend all L4-to-OT sync and remote access immediately. No OT isolation yet. |
| 3 | OT L3: historian, domain controller, engineering network | Network-isolate affected hosts at the firewall. Keep collectors running. Prepare controller-side recovery. |
| 4 | OT L1 or L2: controllers, HMIs | Process protection first. Isolate at the network layer only. Powering off a controller is a process shutdown decision owned by the operations manager. |

## Branch Decisions

| Condition | Action | Authority |
| --- | --- | --- |
| Ransomware in IT, OT boundary clean | Suspend L4-to-OT sync. Monitor. | IT security lead |
| Ransomware in DMZ | Deny DMZ-to-L3 flows. Keep L3.5 interfaces up for forensics. | IT security lead with OT owner |
| Ransomware on historian | Isolate historian network port. Historian data loss is acceptable. Process data loss is not. | Operations manager |
| Ransomware on EWS | Isolate EWS. Process continues on last downloaded logic. Verify no unauthorized download occurred. | Operations manager |
| Ransomware on HMI | Isolate HMI at the firewall. Switch operators to backup HMI. | Operations manager |
| Ransomware on controller network | Escalate to operations manager and safety engineer immediately. Controller isolation may require a process shutdown. | Operations manager and safety engineer jointly |
| Backup mounted on network | Do not restore from it. Locate offline backups only. | Operations manager |
| IT requests enterprise-wide credential reset | Review OT service account impact first. Reset IT-only accounts. | Operations manager with IT security lead |
| Enterprise IT pushes an EDR or antivirus update into OT | Hold the update at the boundary. OT hosts require vendor certification before security agent changes. | Operations manager with OT security |

## Escalation Triggers

- Any Zone 4 classification.
- Any interlock trip, bypass, or override after the response began.
- Backup integrity verification failure.
- Ransomware in a safety instrumented system network segment.

