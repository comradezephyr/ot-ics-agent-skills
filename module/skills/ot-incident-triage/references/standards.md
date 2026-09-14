# Framework Mappings: ot-incident-triage

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-2-1

### 4.3.4.5

Incident response.

Applies because triage is the entry point of the response capability. 4.3.4.5 requires an incident response capability for the ICS. The triage skill defines how that capability starts: authority confirmed, impact classified, decision recorded.

## IEC 62443-3-3

### SR 6.2

Continuous monitoring.

Applies because triage consumes monitoring output and feeds decisions back into it. SR 6.2 requires the capability to monitor security-relevant events. The 15 minute reassessment loop is the monitoring-to-decision cycle.

### SR 2.8

Auditable events.

Applies because the triage report is the audit record of the response decision. SR 2.8 requires that events relevant to security be auditable. The report records who decided, what was decided, and why.

## NIST SP 800-82r3

### IR-4

Incident Handling.

Applies because the triage decision is the first handling action. IR-4 requires that incidents be handled per defined procedures. The decision matrix is the defined procedure for the first hour.

### IR-5

Incident Monitoring.

Applies because the reassessment loop tracks incident status. IR-5 requires tracking and reporting. The 15 minute cycle and the escalation triggers are the tracking mechanism.

### IR-6

Incident Reporting.

Applies because the triage report initiates formal reporting to stakeholders. IR-6 requires reporting consistent with the response plan. The report format and routing satisfy that requirement for the first hour.

## NIST CSF 2.0

### RS (Respond)

Family level. The skill is the response entry point. CSF subcategories are site specific and are not pinned by this file.

## ATT&CK for ICS

### T0880

Loss of Safety.

Applies because safety-classified incidents route to the safety engineer before any other action. T0880 is the worst outcome in OT. The triage matrix makes it the highest priority classification.

### T0889

Modify Program.

Applies because unexplained controller state changes route to `plc-logic-integrity-check`. T0889 is the likely technique behind a state change the operators did not cause.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

