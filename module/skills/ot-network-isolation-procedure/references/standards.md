# Framework Mappings: ot-network-isolation-procedure

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-2-1

### 4.3.4.5

Incident response.

Applies because isolation is a defined containment action in the response capability. 4.3.4.5 requires an incident response capability. This skill is the mechanical execution of the containment decisions made by triage or ransomware response.

## IEC 62443-3-3

### SR 5.2

Zone boundary protection.

Applies because the isolation enforces a zone boundary from the zone model. SR 5.2 requires denial of unauthorized communication across zone boundaries. Under incident conditions the boundary is enforced manually through the procedure.

### SR 7.1

Denial of service protection.

Applies because the procedure bounds the denial. SR 7.1 requires protection against denial of network-accessible resources. The two-sided verification in steps 6 and 7 confirms the denial hit the isolated segment and nothing else.

### SR 7.6

Network and service availability.

Applies because step 7 verifies the control room retained its paths. SR 7.6 requires protection of network and service availability. The containment must not degrade the services the process depends on outside the isolated segment.

## NIST SP 800-82r3

### IR-4

Incident Handling.

Applies because the gated workflow is the handling action. IR-4 requires defined handling procedures. The boundary approval, notification, and verification steps are the procedure.

### SC-7

Boundary Protection.

Applies because the deny rules are SC-7 enforcement applied under incident conditions. SC-7 requires managed interfaces with deny by default. The isolation makes the documented boundary real.

## NIST CSF 2.0

### RS (Respond)

Family level. The skill is a response procedure. CSF subcategories are site specific and are not pinned by this file.

## ATT&CK for ICS

### T0881

Service Stop.

Applies as a response-failure guard. An isolation that cuts the control room path or a safety-critical flow is a self-inflicted service stop. The rollback rules and the process state check exist to prevent that outcome.

### T0885

Commonly Used Port.

Applies because the verification and rule design key on the standard OT protocol ports. T0885 covers an adversary hiding in common ports. Rules per flow direction on explicit ports avoid a blanket cut that T0885 activity would exploit.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

