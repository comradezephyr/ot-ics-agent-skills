# OT Incident Triage Decision Matrix

Branching logic for the first-hour triage. The operations manager makes every decision that touches a running process.

## Impact Classification

| Impact | Definition | Priority | Immediate Escalation |
| --- | --- | --- | --- |
| Safety | Human or equipment safety at risk | 1 | Safety engineer, operations manager |
| Availability | Process control or visibility degraded | 2 | Operations manager |
| Integrity | Control data, logic, or historian data untrusted | 3 | Operations manager, OT security |
| Confidentiality | OT data exposed, no control impact | 4 | OT security, IT SOC |

## Isolate or Monitor

| Condition | Decision | Reasoning |
| --- | --- | --- |
| Integrity impact confirmed on controller-facing system, isolation does not interrupt process | Isolate | Containment beats further compromise. |
| Active adversary actions observed on an OT host | Isolate that host | One host is containable without process impact. |
| Isolation would interrupt a running process | Monitor | A wrong isolation can be more damaging than the incident. |
| Evidence ambiguous, telemetry incomplete | Monitor | Triage continues. Reassess every 15 minutes. |
| Confidentiality impact only | Monitor | Data exposure does not justify process risk. |
| Safety impact of any kind | Halt triage, escalate | Safety outranks containment. Safety engineer leads. |

## Reassessment

Reassess every 15 minutes while monitoring. Escalate to isolate when any of:
- A second system shows the same indicator.
- Operator reports of process behavior change.
- Controller state changes without an operator action.
- The telemetry source itself becomes untrusted.

## Next Action Routing

| Finding | Skill |
| --- | --- |
| Segment compromise | ot-network-isolation-procedure |
| HMI compromise | scada-hmi-incident-containment |
| Controller integrity concern | plc-logic-integrity-check |
| Ransomware indicators | ransomware-response-in-ot |
| Vendor component involved | supply-chain-compromise-response-ot |
| Containment complete, evidence needed | post-incident-ot-forensics |

