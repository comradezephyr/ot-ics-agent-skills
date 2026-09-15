# Framework Mappings: ot-security-program-maturity-assessment

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a workflow step. Keep both files in sync.

## C2M2

### Asset, Change, and Configuration Management

Applies to step 1. Asset inventory, configuration baselines, and change control maturity. Evidence references: asset inventory with OT coverage, change records, configuration baselines.

### Identity and Access Management

Applies to step 1. Account management, authentication, and access review maturity. Evidence references: account lists covering controllers and HMIs, access reviews, MFA coverage.

### Threat and Vulnerability Management

Applies to step 1. Threat identification, vulnerability scanning, and remediation maturity. Evidence references: vulnerability assessments for OT systems, remediation records, threat sources tracked.

### Risk Management

Applies to step 1. Risk assessment and risk register maturity. Evidence references: risk registers per zone, assessment dates, accepted risk records with owners.

### Situational Awareness

Applies to step 1. Monitoring and detection maturity. Evidence references: IDS deployment, alert triage records, monitoring coverage of OT segments.

### Event and Incident Response

Applies to step 1. Response plan, exercises, and incident records. Evidence references: IR plan, exercise records, incident reports with timelines.

### Third-Party Risk Management

Applies to step 1. Vendor assessment and contract maturity. Evidence references: vendor risk register, contract clause maps, remote access model per vendor.

### Workforce Management

Applies to step 1. Training and personnel security maturity. Evidence references: training records per role, assessment results, background check process.

### Cybersecurity Architecture

Applies to step 1. Zone and conduit design maturity. Evidence references: zone map with SL-T targets, conduit registers, DMZ design.

### Cybersecurity Program Management

Applies to step 1. Program governance, policy, and metrics maturity. Evidence references: policy set, program metrics, management review records.

This file maps C2M2 domains at domain level and does not cite C2M2 practice identifiers, per the assessment scope. Where a detailed C2M2 practice assessment exists, extend this file with the practice-level scores and note the source.

## NIST SP 800-82r3

### CM-8

System Component Inventory.

Evidence anchor for the asset domain. The inventory with OT coverage is the CM-8 artifact the asset domain maturity rests on.

### SI-4

System Monitoring.

Evidence anchor for the situational awareness domain. IDS deployment and alert records are the SI-4 artifacts.

### PM family

Program management controls.

Evidence anchor for the Cybersecurity Program Management domain. Policy set and management review records are the PM artifacts.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real domain and control identifiers. Do not invent C2M2 practice identifiers.
- If a mapping cannot be verified from skill output, remove it.
