# Framework Mappings: ot-security-awareness-training-plan

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a workflow step. Keep both files in sync.

## IEC 62443-2-1

### 4.3.2.4.3

Training requirement.

Applies to decision 2. The role-topic matrix is the 4.3.2.4.3 implementation. 62443-2-1 requires that personnel with OT responsibilities be trained for their role, which means the content is role-derived rather than generic.

## NIST SP 800-82r3

### AT-2

Security Awareness.

Applies to decision 2. The topics per role are the awareness content. Awareness covers what people should recognize and report.

### AT-3

Security Training.

Applies to decisions 3 and 4. Delivery method and frequency are the AT-3 design. Training covers what people should be able to do, which for control engineers means hands-on change discipline.

### AT-4

Security Training Records.

Applies to decisions 5 and 6. Assessment and tracking are the AT-4 requirements that make the program verifiable. Attendance lists do not satisfy AT-4 because they record presence, not capability.

### PS family

Personnel Security.

Applies to decision 2. Contractor onboarding at access granting is the PS coverage for third-party personnel.

## NIST CSF 2.0

### PR.AT

Awareness and Training.

Family level. The plan is the PR.AT implementation. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control identifiers. Do not invent AT or PR subcategories.
- If a mapping cannot be verified from skill output, remove it.
