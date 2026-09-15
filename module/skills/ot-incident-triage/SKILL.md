---
name: ot-incident-triage
description: Triage an OT security incident in the first hour with safety-first decision gates, classifying impact type and choosing isolate or monitor. Use when an OT alert, operator report, or enterprise SOC notification needs a response decision.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-IRR-ot-incident-triage
  author: comradezephyr
  frameworks:
    - IEC 62443-2-1
    - NIST SP 800-82r3
    - ATT&CK for ICS T0880
# allowed-tools: Read Grep Bash
---

## When to Use

- First-hour response to an OT alert before a full investigation exists.
- Operator report of unexplained process behavior or controller state changes.
- Enterprise SOC notification with a confirmed path into OT.
- Deciding between isolation and monitoring when information is incomplete.

## Prerequisites

- Zone and conduit map with Purdue levels.
- On-call contacts: operations manager, safety engineer, controls engineer, IT SOC.
- Current detection alerts from `modbus-anomaly-detection`, `dnp3-anomaly-detection`, or the SIEM.
- Remote read access to the boundary firewall and the historian.
- Credentials: read-only telemetry access. No engineering access is required for triage.
- Authorization: operations manager owns every decision that touches a running process.
- Upstream skills: `passive-ot-network-discovery` output as the asset baseline.

### Safety

This skill is passive by default. Triage collects telemetry and makes decisions. Active containment steps belong to the downstream skills and carry their own gates.

- Passive. Reads telemetry and writes the triage report. Safe to run during normal operations.

## Workflow

> SAFETY: If at any point the action risks human safety or process integrity, halt and escalate to the operations lead before continuing.

1. Confirm the decision authority. The operations manager decides isolate or monitor. Record the name, contact, and the time of confirmation in the report.
2. Collect the initial facts in five minutes: what fired, which zone, which process, operator observations, current controller states.
3. Classify the impact type using `references/decision-matrix.md`:
   - Safety: human or equipment safety at risk. Highest priority. Escalate to the safety engineer immediately.
   - Availability: process control or visibility degraded.
   - Integrity: control data, logic, or historian data untrusted.
   - Confidentiality: OT data exposed. Lowest response priority. Never outranks the other three.
4. Determine the affected zone from the asset baseline. Record Purdue level per affected asset.
5. Decision point: isolate or monitor. Branch criteria in the matrix:
   - Isolate when: integrity impact confirmed on a controller-facing system, or active adversary actions are observed, and isolation does not interrupt the process.
   - Monitor when: evidence is ambiguous, or isolation would interrupt a running process, or the impact is confidentiality only.
   When in doubt, monitor and escalate. A wrong isolation decision is often worse than a wrong monitor decision in OT.
6. Choose the next action skill:
   - Isolation decision: `ot-network-isolation-procedure`.
   - HMI compromise: `scada-hmi-incident-containment`.
   - Controller integrity concern: `plc-logic-integrity-check`.
   - Ransomware indicators: `ransomware-response-in-ot`.
7. Produce `ot-triage-report.md`. Sections: decision authority, impact classification, affected zone, evidence summary, isolate or monitor decision with reasoning, next action, timestamps.

## Verification

- Correct output: `ot-triage-report.md` names the decision authority, classifies impact, records the isolate or monitor decision with reasoning, and routes a next action.
- Failure mode: no operator or telemetry confirmation available in the first hour. Triage proceeds on the classification alone with the uncertainty recorded. Do not let missing evidence stall the decision.
- Failure mode: the report classifies impact as integrity with no evidence source named. The classification is unsupported. Downgrade to unknown and keep monitoring.
- OT check: the triage process itself generated no write traffic to any controller or SIS. Verify on the span that no packets originated from the triage host.
- OT check: controller states recorded in step 2 match the operator's view. A discrepancy between telemetry and operator observation is itself an integrity finding.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-2-1 | 4.3.4.5 | Incident response. Triage is the first step of the response capability. |
| IEC 62443-3-3 | SR 6.2 | Continuous monitoring. Triage consumes the monitoring output. |
| IEC 62443-3-3 | SR 2.8 | Auditable events. The report is the audit record of the response decision. |
| NIST SP 800-82r3 | IR-4 | Incident Handling. The triage decision is the first IR-4 handling action. |
| NIST SP 800-82r3 | IR-6 | Incident Reporting. The report initiates formal reporting. |
| NIST SP 800-82r3 | IR-5 | Incident Monitoring. The reassessment loop tracks status. |
| NIST CSF 2.0 | RS | Respond. Family level. Site assigns specific subcategories. |
| ATT&CK for ICS | T0880 | Loss of Safety. Safety-classified incidents route to the safety engineer first. |
| ATT&CK for ICS | T0889 | Modify Program. Unexplained controller state changes route to logic integrity checks. |

