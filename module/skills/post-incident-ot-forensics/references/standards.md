# Framework Mappings: post-incident-ot-forensics

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-2-1

### 4.3.4.5

Incident response.

Applies because evidence collection supports the response capability and its post-incident review. 4.3.4.5 requires an incident response capability. The register and timeline are the capability's evidence layer.

## IEC 62443-3-3

### SR 2.8

Auditable events.

Applies because the collected artifacts are the audit record of the incident. SR 2.8 requires that events relevant to security be auditable. Collection preserves those records before rotation, tampering, or restore destroys them.

### SR 6.1

Audit log accessibility.

Applies because collection depends on the logs being accessible. SR 6.1 requires that audit logs be accessible to authorized personnel and tools. Where a source's logs are inaccessible or disabled, the register records the source as not-covered, which surfaces the SR 6.1 gap.

### SR 3.1

Communication integrity.

Applies because the hash verification chain is the integrity check on the evidence itself. SR 3.1 requires integrity protection for communications. The same property applied to evidence makes the register trustworthy.

## NIST SP 800-82r3

### IR-4

Incident Handling.

Applies because collection is an IR-4 handling activity. IR-4 requires defined handling procedures. The ranked order and gates are the procedure for the OT case.

### IR-5

Incident Monitoring.

Applies because the timeline tracks the incident end to end. IR-5 requires tracking and reporting. The timeline is the tracking artifact.

### AU-9

Protection of Audit Information.

Applies because hashes and controlled storage protect the evidence. AU-9 requires protecting audit information from unauthorized access, modification, and deletion. Write-once storage and the custody chain are the AU-9 controls.

## NIST CSF 2.0

### RS (Respond)

Family level. The skill supports the response function. CSF subcategories are site specific and are not pinned by this file.

## ATT&CK for ICS

### T0889

Modify Program.

Applies because controller logic evidence is the record of T0889 activity. The upload in step 8 captures the program state that a modify-program technique changed.

### T0873

Project File Infection.

Applies because project file artifacts are the T0873 evidence. Engineering workstations and controller project stores are collected in steps 7 and 8.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

