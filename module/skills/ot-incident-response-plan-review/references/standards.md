# Framework Mappings: ot-incident-response-plan-review

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a workflow step. Keep both files in sync.

## NIST SP 800-61

### Preparation

Applies to step 1. The plan must cover preparation: prerequisites, contacts, playbooks, and training. The review checks that this phase has actionable content rather than policy statements.

### Detection and Analysis

Applies to step 1. The plan must state how incidents are detected, analyzed, and triaged. Cross-reference to the detection skills is acceptable evidence.

### Containment, Eradication, and Recovery

Applies to step 1. The plan must cover containment with safety constraints, eradication, and recovery with verification. The review checks that these sections name decision authorities.

### Post-Incident Activity

Applies to steps 1 and 6. The plan must define a post-incident review process that produces plan changes. A plan without a post-incident feedback loop has no IR-8 maintenance mechanism.

## NIST SP 800-82r3

### IR-1

Policy.

Applies to step 1. The plan is the IR-1 policy artifact. The review checks it against the 800-61 structure and the OT safety requirements.

### IR-4

Incident Handling.

Applies to step 5. Playbook coverage is the IR-4 requirement that handling procedures exist for the incident types the site will face.

### IR-6

Incident Reporting.

Applies to step 4. Escalation paths and notification obligations are the IR-6 content the review verifies.

### IR-7

Incident Response Assistance.

Applies to step 4. Contact currency is the IR-7 requirement that assistance is reachable. The verification date is the evidence.

### IR-8

Incident Response Plan.

Applies to step 6. The plan maintenance process, including the post-incident update loop, is the IR-8 requirement.

## IEC 62443-2-1

### 4.3.4.5

Incident response capability.

Applies to step 3. The safety gate requirement is the 62443-2-1 contribution to the review: the plan must protect safety and process integrity during response, not just describe containment.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real publication and control identifiers. Do not invent 800-61 phase names or IR identifiers.
- If a mapping cannot be verified from skill output, remove it.
