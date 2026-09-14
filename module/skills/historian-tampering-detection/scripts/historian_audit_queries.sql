# Historian Audit Queries

Working queries per platform. Run read-only. Replace placeholders before executing. Query IDs are referenced from the workflow and from `historian-tamper-detection.md`.

## OSIsoft PI

Out-of-path writes. The PI audit trail records configuration and archive changes. Filter to the approved collector identities.

```sql
-- Q1: PI audit trail, writes from unapproved identities
SELECT Time, Action, Details, PIServer
FROM piarchive..piaudit
WHERE Time > :review_start AND Time < :review_end
  AND Action IN ('insert','update','delete')
  AND UserOrProgram NOT IN (/* approved writer accounts */ 'pidelta', 'picollector')
ORDER BY Time;
```

Backfill detection. Values written with timestamps older than the collector scan interval.

```sql
-- Q2: backfilled values per tag
SELECT tag, time, value, questionable
FROM piarchive..piinterp2
WHERE tag = :tag AND time > :review_start
  AND questionable = 1
ORDER BY tag, time;
```

Timestamp anomalies within a tag.

```sql
-- Q3: duplicate timestamps with differing values
SELECT tag, time, COUNT(DISTINCT value) AS variants
FROM piarchive..picomp
WHERE tag = :tag AND time > :review_start
GROUP BY tag, time
HAVING COUNT(DISTINCT value) > 1
ORDER BY tag, time;
```

## SQL Server (Wonderware Historian, Ignition on MSSQL)

Requires SQL Server audit configured. Confirm with `SELECT * FROM sys.server_audits`.

```sql
-- Q4: out-of-path writes from sys.fn_get_audit_file
SELECT event_time, sequence_number, action_id, session_server_principal_name,
       client_ip, object_name, statement
FROM sys.fn_get_audit_file('\\audit-share\SqlAudit\*.sqlaudit', DEFAULT, DEFAULT)
WHERE action_id IN ('IN','UP','DL')
  AND session_server_principal_name NOT IN (/* approved writers */ 'ww_collector', 'ignition')
  AND event_time > :review_start
ORDER BY event_time;
```

```sql
-- Q5: direct writes to the history table from interactive sessions
SELECT session_server_principal_name, client_ip, object_name, COUNT(*) AS writes
FROM sys.fn_get_audit_file('\\audit-share\SqlAudit\*.sqlaudit', DEFAULT, DEFAULT)
WHERE object_name LIKE '%History%'
  AND action_id = 'IN'
  AND session_server_principal_name NOT LIKE '%collector%'
GROUP BY session_server_principal_name, client_ip, object_name
ORDER BY writes DESC;
```

## PostgreSQL (Ignition on PostgreSQL, pgaudit)

Confirm pgaudit is loaded: `SHOW shared_preload_libraries;` must include `pgaudit`.

```sql
-- Q6: pgaudit writes to historian tables from unapproved roles
SELECT log_time, user_name, client_addr, audit_type, statement
FROM pgaudit_analysis_v1(:review_start, :review_end)  -- or read csvlog directly
WHERE audit_type = 'WRITE'
  AND user_name NOT IN (/* approved writers */ 'ignition')
ORDER BY log_time;
```

Where no analysis function exists, read the csvlog directly:

```sql
-- Q6b: csvlog scan for WRITE class entries outside the collector role
SELECT log_time, user_name, client_addr, message
FROM postgres_log
WHERE command_tag IN ('INSERT','UPDATE','DELETE')
  AND user_name NOT IN ('ignition')
  AND log_time > :review_start
ORDER BY log_time;
```

## Honeywell PHD

PHD audit runs on its Oracle or SQL Server backend. Use Q4 or Q6 against the PHD schema, substituting the PHD collector account for the approved writer. Record the platform and account in the report.

## Retention deletion

```sql
-- Q7: archive extent deletion events (SQL Server variant)
SELECT event_time, session_server_principal_name, client_ip, statement
FROM sys.fn_get_audit_file('\\audit-share\SqlAudit\*.sqlaudit', DEFAULT, DEFAULT)
WHERE statement LIKE '%DROP%' OR statement LIKE '%TRUNCATE%'
   OR statement LIKE '%DELETE FROM%Archive%'
ORDER BY event_time DESC;
```

Compare archive extents against the retention policy. An extent removed before policy age is a finding.

