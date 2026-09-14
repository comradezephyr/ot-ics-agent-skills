# Questionnaire: IEC 62443-3-3 Gap Assessment

For each block, record current state, target state, evidence artifact, and evidence owner. Answers without evidence are scored as gaps.

## Block A: Access Control

### A1 SR 1.1 Identification and Authentication of Human Users

- Q1. How do users authenticate at HMIs, EWS, and engineering tools? List the mechanism per asset class.
- Q2. Are shared or default accounts in use anywhere in the zone? Name every account.
- Q3. Is re-authentication enforced after a session timeout? What timeout is configured?

### A2 SR 1.2 Software Process and Device Identification

- Q1. Is software and device identity verified before communication? Which mechanism (802.1X, S7 certificate, OPC UA application certificate)?
- Q2. Which devices in the zone have no identity mechanism? List them.

## Block B: Use Control

### B1 SR 2.1 Authorization Enforcement

- Q1. Is access enforced per role at each asset? Who approves role changes?
- Q2. Are authorization records kept for engineering software and historian access?

### B2 SR 2.8 Auditable Events

- Q1. Which events are logged (login, logout, config change, program download)?
- Q2. Where are the logs stored and what is the retention period?

## Block C: System Integrity

### C1 SR 3.1 Communication Integrity

- Q1. Which protocols carry integrity protection (DNP3 SA, OPC UA signing, signed firmware)?
- Q2. Which unprotected protocols run in the zone?

### C2 SR 3.3 Security Functionality Verification

- Q1. When was the security functionality last verified (firewall rules, backup restore, monitors)?
- Q2. Whose record proves the verification?

## Block D: Data Confidentiality

### D1 SR 4.1 Information Confidentiality

- Q1. Are zone data sets classified? Which data never leaves L3?
- Q2. Who has access to engineering project files and historian archives?

### D2 SR 4.3 Use of Cryptography

- Q1. Where is encryption in use (VPN, OPC UA, file transfer)?
- Q2. Which ciphers are configured at each point?

## Block E: Restricted Data Flow

### E1 SR 5.1 Network Segmentation

- Q1. Where are the zone boundaries and what enforces them (firewall, switch ACL)?
- Q2. Are there documented or undocumented links between zones?

### E2 SR 5.2 Zoning

- Q1. Is each zone documented with a membership list?
- Q2. Who is the zone owner for each documented zone?

### E3 SR 5.4 General Purpose Person-to-Person Communication Restriction

- Q1. Are email, web, or chat services reachable from L1 and L2?
- Q2. What restricts those services?

## Block F: Timely Response

### F1 SR 6.1 Audit Log Accessibility

- Q1. Can auditors read the logs within the required time without a production outage?
- Q2. Are logs retained for 90 days or more?

### F2 SR 6.2 Continuous Monitoring

- Q1. What is monitored continuously in the zone (network capture, HMI alarms, system events)?
- Q2. Who triages the monitor output and on what cadence?

## Block G: Resource Availability

### G1 SR 7.1 Resilience Against Denial of Service

- Q1. What happens to the process if a protocol flood hits the L1 or L2 segment?
- Q2. Is there rate limiting or priority queuing at the zone boundary?

### G2 SR 7.2 Control System Backup and Recovery

- Q1. When was the last verified restore of PLC logic, historian data, and EWS images?
- Q2. Where are the backups stored and how are they protected from the production network?

### G3 SR 7.6 Network and Service Availability

- Q1. Which links carry the maintenance window durations? Are redundancy paths tested?
- Q2. What is the last measured failover time for redundant links?

## Scoring

- Pass: evidence shows the control in place.
- Partial: some evidence, full control not shown.
- Absent: no evidence.
- Copy each block result into `gap-register.md` with severity, evidence, and owner.
