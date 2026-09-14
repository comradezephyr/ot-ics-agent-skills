# Framework Mappings: plc-recovery-from-backup

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-2-1

### 4.3.4.5

Incident response.

Applies because recovery is a defined part of the response capability. 4.3.4.5 requires the incident response capability to restore systems to an operational state. The restore workflow with its gates is that capability for controllers.

## IEC 62443-3-3

### SR 7.2

Resource management.

Applies because the verified backup set is the managed resource. SR 7.2 requires managing resources so protection mechanisms function when needed. Step 1 verifies the resource before use. A restore from an unverified backup is the SR 7.2 failure mode.

### SR 7.1

Denial of service protection.

Applies because the rollback plan bounds the outage. SR 7.1 requires protection against denial of service. A failed restore without a rollback plan extends the controller outage indefinitely. Step 2 makes the rollback plan mandatory.

### SR 3.1

Communication integrity.

Applies because the hash comparison in step 6 verifies the integrity of the restored program. SR 3.1 requires integrity protection for communications. The MATCH result is the integrity evidence.

## NIST SP 800-82r3

### CP-9

System Backup.

Applies because the procedure consumes the CP-9 backup. CP-9 requires backup of system-level information. The hash files and the second backup for rollback are the CP-9 artifacts the workflow requires.

### CP-10

System Recovery.

Applies because the restore is the CP-10 action. CP-10 requires recovery capability with defined timeframes and verification. The verification and rollback steps satisfy the CP-10 testing expectation.

### IR-4

Incident Handling.

Applies because recovery runs inside the response procedure. IR-4 requires defined handling procedures. The gates and approvals are the handling discipline.

## NIST CSF 2.0

### RC (Recover)

Family level. The skill is a recovery procedure. CSF subcategories are site specific and are not pinned by this file.

## ATT&CK for ICS

### T0889

Modify Program.

Applies because the restore removes tampered or corrupted logic and reinstates approved logic. The hash verification proves the T0889 state is gone. A post-restore MISMATCH means the adversary path is still open and the incident is not contained.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

