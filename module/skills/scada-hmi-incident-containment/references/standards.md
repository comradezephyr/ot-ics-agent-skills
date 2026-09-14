# Framework Mappings: scada-hmi-incident-containment

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-2-1

### 4.3.4.5

Incident response.

Applies because the workflow is a defined containment action inside the response capability. 4.3.4.5 requires an incident response capability for the ICS. HMI containment with operator continuity is the capability applied to the HMI case.

## IEC 62443-3-3

### SR 2.8

Auditable events.

Applies because step 2 exports the session logs and audit trail before any containment action. SR 2.8 requires that security-relevant events be auditable. A compromised host can erase its own logs after detection, so preservation precedes isolation.

### SR 6.2

Continuous monitoring.

Applies because step 5 verifies containment through span traffic. SR 6.2 requires the capability to monitor security-relevant events. The span is the independent verification that the deny held.

### SR 5.2

Zone boundary protection.

Applies because the firewall deny enforces the boundary between the HMI zone and the controller zone. SR 5.2 requires denial of unauthorized communication across zone boundaries. The containment makes an existing boundary violation impossible to continue.

## NIST SP 800-82r3

### IR-4

Incident Handling.

Applies because the workflow is the containment procedure. IR-4 requires that incidents be handled per defined procedures. The gates and the evidence-first ordering are the handling discipline.

### IR-5

Incident Monitoring.

Applies because the span check and the backup path verification track containment status. IR-5 requires tracking and reporting. The record captures both.

## NIST CSF 2.0

### RS (Respond)

Family level. The skill is a response procedure. CSF subcategories are site specific and are not pinned by this file.

## ATT&CK for ICS

### T0886

Remote Services.

Applies because the firewall deny closes the HMI session path. T0886 covers an adversary using remote services for access and staging. A compromised HMI session is that path into controller networks.

### T0882

Theft of Operational Information.

Applies because the preserved session logs record what the adversary viewed or exported. T0882 covers collection of operational data. The log review after containment determines the scope of the theft.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

