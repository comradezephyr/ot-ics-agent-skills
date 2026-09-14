# Framework Mappings: historian-tampering-detection

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 2.8

Auditable events.

Applies because every query in the workflow reads an audit trail. SR 2.8 requires that security-relevant events be auditable. Where the audit trail is disabled, the skill cannot operate and reports the gap as a High finding. The disabled audit trail is itself the SR 2.8 failure.

### SR 3.1

Communication integrity.

Applies because the approved writer list defines the trusted data path into the archive. SR 3.1 requires integrity protection for communications. An INSERT or UPDATE from outside the collector path bypasses that trust and is the integrity violation the queries detect.

## ATT&CK for ICS

### T0882

Theft of Operational Information.

Applies because unapproved read access surfaces in the same audit review. T0882 covers an adversary collecting operational data. The audit trail shows access patterns alongside writes, and the review records both.

### T0889

Modify Program.

Applies as a support mapping. Modified historian data supports the deception layer of a broader campaign that includes program modification. A historian finding raises the severity of any concurrent `plc-logic-integrity-check` MISMATCH.

## NIST SP 800-82r3

### AU-6

Audit Record Review.

Applies because the query set is the AU-6 review procedure for the historian tier. AU-6 requires that audit records be reviewed for indications of inappropriate activity. The bundled queries make the review repeatable and scoped.

## NIST CSF 2.0

### DE (Detect)

Family level. The skill is a detection procedure. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

