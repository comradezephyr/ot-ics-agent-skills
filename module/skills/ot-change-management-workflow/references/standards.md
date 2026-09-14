# Framework Mappings: ot-change-management-workflow

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a design decision in the Workflow section. Keep both files in sync.

## IEC 62443-2-1

### 4.3.4.3

Change management.

Applies to decisions 1 through 7. Class routing, request fields, approval gates, rollback requirement, verification, and retention are the 4.3.4.3 implementation. 4.3.4.3 requires that changes to the ICS follow a defined process with authorization and verification.

## IEC 62443-3-3

### SR 7.2

Control system backup.

Applies to decision 5. The rollback requirement consumes the backup capability. A change process that does not reference backups cannot roll back.

### SR 2.8

Auditable events.

Applies to decision 7. The change record is the audit trail of who changed what with whose approval.

## NIST SP 800-82r3

### CM-3

Configuration Change Control.

Applies to decisions 2, 5, and 8. Request fields, mandatory rollback, and the emergency path with retroactive records are the CM-3 implementations.

### CM-4

Impact Analysis.

Applies to decisions 3 and 6. The security review step and the post-change verification analyze the impact of changes before and after they land.

### CM-5

Access Restrictions for Change.

Applies to decision 4. Gate authority per class restricts who can authorize changes to what.

### IR-4

Incident Handling.

Applies to decision 8. The emergency path is the IR-4 provision for changes required during incident handling.

## NIST CSF 2.0

### GV (Govern)

Family level. Gate authority and class definitions are governance decisions. CSF subcategories are site specific and are not pinned by this file.

## ATT&CK for ICS

### T0889

Modify Program.

Applies to decision 6. Hash comparison against the approved version detects program changes that did not ride the process. A change workflow without hash verification is itself a T0889 path.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

