# Post-Incident OT Forensics Evidence Matrix

Ranking of evidence sources by volatility and process risk. Collect top to bottom. The order balances evidence perishability against process disruption.

## Source Ranking

| Rank | Source | Volatility | Process Risk | Gate |
| --- | --- | --- | --- | --- |
| 1 | Network capture of ongoing activity | Very high, adversary may stop or encrypt | None | None |
| 2 | Firewall, switch, boundary router logs | High, overwritten on rotation | None | None |
| 3 | Historian audit trail and archives | Medium, retained but mutable by admins | None | None |
| 4 | HMI session logs and audit trails | Medium, host may be compromised | None | None |
| 5 | Host memory and disk images | High volatility for memory | Low, read-only imaging | Operations manager |
| 6 | Controller logic and configuration | High, overwritten on next download | High, controller interaction | Operations manager plus safety engineer |

## Controller Evidence Rules

- Collection uses the `plc-logic-integrity-check` upload path in capture mode. It reads. It does not write.
- Confirm the CPU stays in RUN (8) before and after the upload. A state change during collection is a process event, not a forensic step.
- Never run a forensic tool that reboots, stops, or forces a controller into download mode. If evidence requires stopping the controller, that is a process shutdown decision owned by the operations manager with the safety engineer.
- If collection is not possible without process impact, record the source as not-covered with the reason. An incomplete register is better than a process trip.

## Clock Discipline

| Source | Clock Source | Offset Handling |
| --- | --- | --- |
| Network capture | Capture host NTP | Reference clock |
| Firewall and switch logs | Device internal clock | Record offset against capture host |
| Historian | Server clock | Record offset |
| HMI | Workstation clock | Record offset |
| Controller | No NTP on most platforms | Record observed offset from event logs |

## Escalation Triggers

- Any controller state change during collection.
- Any artifact hash mismatch on acquisition or re-verification.
- Evidence on a safety instrumented system. Safety engineer leads collection there.
- Legal hold requirements. Route to the site's legal contact before collection.

