# Framework Mappings: nist-800-82-control-mapping

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## NIST SP 800-82r3

All rows in this file map at family level. The Reason column states the control family objective and the questionnaire block that produces the evidence. A specific control ID is named in a family row only where a single 800-53 control carries the requirement, as with AC-2 in the AC row.

### AC

Access Control. Block AC. Requires that access to systems and data be limited to authorized users. The block records account processes, privilege review, and access approvals.

### AU

Audit and Accountability. Block AU. Requires logging and log review capabilities. The block records what is logged, retention, and who reviews.

### CA

Assessment, Authorization, and Monitoring. Block CA. Requires continuous monitoring and board-level authorization. The block records the monitoring program and the authorization status of the OT network.

### CM

Configuration Management. Block CM. Requires documented baselines and change control. OT configuration artifacts are required here. An IT configuration policy is not acceptable evidence for an OT control.

### CP

Contingency Planning. Block CP. Requires recovery plans and tested restores. The block records the last verified restore and the plan owner.

### IA

Identification and Authentication. Block IA. Requires identities and authentication mechanisms. The block records credential stores and MFA coverage.

### IR

Incident Response. Block IR. Requires detection and response capabilities. The block records the OT IR plan and its last exercise.

### MA

Maintenance. Block MA. Requires controlled maintenance access. The block records vendor and maintenance access processes.

### MP

Media Protection. Block MP. Requires control over removable media. The block records USB policy and media inventory.

### PE

Physical and Environmental Protection. Block PE. Requires physical access control for OT assets. The block records cabinet and zone-door controls.

### PL

Planning. Block PL. Requires security planning documents. The block records the security architecture and deployment documents.

### PS

Personnel Security. Block PS. Requires screening and training. The block records OT security awareness training.

### RA

Risk Assessment. Block RA. Requires documented risk assessments. The block records the last assessment and its scope.

### SA

System and Services Acquisition. Block SA. Requires secure acquisition of OT systems and services. The block records procurement security requirements.

### SC

System and Communications Protection. Block SC. Requires segmentation and encryption. The block records firewall, DMZ, and crypto controls.

### SI

System and Information Integrity. Block SI. Requires integrity checking and malicious code protection. The block records antivirus, whitelisting, and baseline checks.

## NIST CSF 2.0

### GV (Govern)

Family level. Workflow step 1 assigns the control owner and step 6 assigns the matrix review cadence. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.
