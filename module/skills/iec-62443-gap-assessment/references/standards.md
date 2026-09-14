# Framework Mappings: iec-62443-gap-assessment

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 1.1

Identification and authentication of human users.

Questionnaire block A1, workflow steps 2 and 3. SR 1.1 requires that human access be identified and authenticated. The block records the mechanism per asset class and flags shared accounts. The evidence artifact is the account or policy document.

### SR 1.2

Software process and device identification.

Block A2. SR 1.2 requires software processes and devices to be uniquely identified. The block records which identity mechanisms the zone supports. The gap register entry states which devices cannot be identified.

### SR 2.1

Authorization enforcement.

Block B1. SR 2.1 requires authorization enforcement for all users. The block records role enforcement and approval paths for engineering access.

### SR 2.8

Auditable events.

Block B2. SR 2.8 requires that security-relevant events be audited. The block records what is logged, where, and for how long. Retention under 90 days is a finding.

### SR 3.1

Communication integrity.

Block C1. SR 3.1 requires integrity protection for communication channels. The block records which protocols carry integrity and which do not. Unprotected protocols are findings.

### SR 3.3

Security functionality verification.

Block C2. SR 3.3 requires verification that security functionality operates. The block records the last functional test of firewalls, backups, and monitors. The verifier's record is the evidence.

### SR 4.1

Information confidentiality.

Block D1. SR 4.1 requires confidentiality of information. The block records data classification and access to engineering and historian archives. Classified sets that leave L3 are findings.

### SR 4.3

Use of cryptography.

Block D2. SR 4.3 requires cryptographic protection where the risk demands it. The block records encryption points and cipher sets. Weak or absent cipher sets are findings.

### SR 5.1

Network segmentation.

Block E1. SR 5.1 requires network segmentation. The block records boundary enforcement points and undocumented links. The enforcement device list feeds the zone and conduit audit.

### SR 5.2

Zoning.

Block E2. SR 5.2 requires documented zones. The block records membership lists and owners. Zones without owners are findings.

### SR 5.4

General purpose person-to-person communication restriction.

Block E3. SR 5.4 restricts general purpose communications between zones. The block records whether email, web, or chat services reach L1 and L2.

### SR 6.1

Audit log accessibility.

Block F1. SR 6.1 requires that audit logs be accessible in time. The block records log reachability and retention for auditors.

### SR 6.2

Continuous monitoring.

Block F2. SR 6.2 requires continuous monitoring. The block records what is monitored and the triage cadence. Monitoring gaps are findings.

### SR 7.1

Resilience against denial of service.

Block G1. SR 7.1 requires resilience against resource exhaustion. The block records boundary protections such as rate limiting and priority queuing.

### SR 7.2

Control system backup and recovery.

Block G2. SR 7.2 requires backup and recovery that preserves the last known secure state. The block records the last verified restore of PLC logic, historian data, and EWS images.

### SR 7.6

Network and service availability.

Block G3. SR 7.6 requires that essential services remain available. The block records redundancy paths and measured failover times.

## NIST CSF 2.0

### GV (Govern)

Family level. Workflow step 1 assigns a register owner per zone, which is the governance action. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.
