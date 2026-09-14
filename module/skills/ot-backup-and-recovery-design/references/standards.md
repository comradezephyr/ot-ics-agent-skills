# Framework Mappings: ot-backup-and-recovery-design

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a design decision in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 7.2

Control system backup.

Applies to decisions 2, 4, and 5. Asset class coverage, offline copies, and architecturally enforced air gaps are the SR 7.2 design. SR 7.2 requires backup of control system information sufficient for recovery.

### SR 7.3

Control system recovery and reconstitution.

Applies to decision 6. The restore test schedule per class is the SR 7.3 design. SR 7.3 requires the capability to restore and reconstitute. A restore that has never been tested is an assumption about that capability.

### SR 3.1

Communication integrity.

Applies to decision 7. Hashing at creation and verification at test is the integrity check on the backup set.

## NIST SP 800-82r3

### CP-9

System Backup.

Applies to decisions 2, 4, and 5. Asset class coverage, offline storage, and air-gap mechanisms are the CP-9 implementations. CP-9 requires backup of system-level information.

### CP-10

System Recovery.

Applies to decisions 3 and 6. RTO targets and restore testing are the CP-10 design. CP-10 requires recovery capability with defined timeframes, which is what the RTO column records.

### CP-2

Business Continuity Plan.

Applies to decision 3. The per-class targets feed the site continuity plan with recovery expectations that operations has accepted.

### AU-9

Protection of Audit Information.

Applies to decision 7. Backup integrity and custody protect the recovery evidence set.

## NIST CSF 2.0

### RC (Recover)

Family level. The skill is a recovery design. CSF subcategories are site specific and are not pinned by this file.

## ATT&CK for ICS

### T0889

Modify Program.

Applies to decision 2. PLC logic backups are the recovery path from a T0889 event. Logic backed up without project files leaves the modified-program state hard to prove and harder to revert.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

