---
name: historian-tampering-detection
description: Detect tampering with historian data including direct SQL writes outside the collector path, backfilled values, timestamp anomalies, retention deletion, and unapproved writer sources. Use when auditing OSIsoft PI, Wonderware, Honeywell PHD, or Ignition data integrity.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-MON-historian-tampering-detection
  author: comradezephyr
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0882
# allowed-tools: Read Grep Bash
---

## When to Use

- Auditing historian data integrity after a suspected compromise.
- Verifying that values in reports and dashboards came through the collector path.
- Investigating gaps or backfilled data in a tag history.
- Reviewing the approved writer list on the historian servers.

## Prerequisites

- Historian platform: OSIsoft PI, Wonderware Historian, Honeywell PHD, or Ignition.
- Database audit access: PI audit trail, Wonderware audit views, SQL Server audit logs, or PostgreSQL pgaudit.
- Approved writer list: collector service accounts and their source hosts.
- Baseline tag archive snapshot from before the review window.
- Credentials: read-only database access on the historian SQL tier.
- Authorization: historian owner sign-off. Query review is passive.
- Upstream skills: `passive-ot-network-discovery` for the collector source list.

### Safety

This skill is passive. Queries run read-only against the audit trail and archive.

- Passive. Analyzes audit logs and archive data. Sends no packets to control devices. Safe to run during normal operations.

## Workflow

1. Collect the approved writer list. One row per tag group: tags, writer account, source host. Export from the collector configuration.
2. Collect the audit trail for the review window. PI: `piarchmanager` audit trail. Wonderware: audit views. SQL Server: `sys.fn_get_audit_file`. PostgreSQL: pgaudit logs. The bundled `historian_audit_queries.sql` file has the working queries per platform.
3. Run the out-of-path write query. Any INSERT or UPDATE on a tag table from an account or source host not on the approved writer list is a finding.
4. Run the backfill query. Values written with timestamps older than the collector scan interval are backfill candidates. Backfill with no maintenance record is a finding.
5. Run the timestamp anomaly query. Timestamps out of order within a tag, duplicate timestamps with different values, or values at sub-scan intervals indicate direct manipulation.
6. Run the retention deletion query. Early deletion of archive blocks or events is a finding. Compare the retention policy against actual archive extents.
7. Compare the current archive against the baseline snapshot for the target tags:
   `diff tags-baseline.csv tags-current.csv > tag-diff.txt`
   A value change with no matching collector event in the audit trail is a finding.
8. Decision point: an out-of-path write touching safety-relevant tags is a High finding. Escalate to incident response. A backfill with a maintenance record is Low and closed with the record reference.
9. Produce `historian-tamper-detection.md`. One row per finding: tag or table, query ID, account, source host, timestamp, severity, evidence reference.

## Verification

- Correct output: `historian-tamper-detection.md` has one row per finding with evidence references, and the query set covers out-of-path writes, backfill, timestamp anomalies, and retention deletion.
- Failure mode: the audit trail is disabled on the historian SQL tier. Out-of-path writes cannot be detected. Report the audit gap as a High finding in its own right.
- Failure mode: the approved writer list is stale. Legitimate collectors flag as findings. Confirm the list against the collector configuration before reporting.
- OT check: run the out-of-path query against a clean 30 day window with zero rows expected. Rows on a clean window mean the writer list is wrong, not that tampering occurred.
- OT check: verify no safety-relevant tag lost data during the review window. A gap in a safety tag archive is a process safety concern before it is a security one.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 2.8 | Auditable events. The historian audit trail is the evidence source for every query. |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. Out-of-path writes violate the trusted collector data path. |
| ATT&CK for ICS | T0882 | Theft of Operational Information. Unapproved read access surfaces alongside write review. |
| ATT&CK for ICS | T0889 | Modify Program. Historian data modification supports downstream deception. |
| NIST SP 800-82r3 | AU-6 | Audit Record Review. The query set is the AU-6 review procedure for the historian. |
| NIST CSF 2.0 | DE | Detect. Family level. Site assigns specific subcategories. |


Row-by-row justification lives in `references/standards.md`.
