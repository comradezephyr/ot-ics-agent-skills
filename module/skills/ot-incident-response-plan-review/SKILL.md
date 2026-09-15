---
name: ot-incident-response-plan-review
description: Review an OT incident response plan against the NIST SP 800-61 phases and NIST SP 800-82r3 IR requirements, covering decision authority, safety gates, escalation, contacts, playbooks, and enterprise integration. Use when a plan needs review or improvement.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-GOV-ot-incident-response-plan-review
  author: comradezephyr
  frameworks:
    - NIST SP 800-61
    - NIST SP 800-82r3
    - IEC 62443-2-1
# allowed-tools: Read Grep Bash
---

## When to Use

- Reviewing an OT incident response plan against a recognized structure.
- After an incident, to review whether the plan matched what responders actually needed.
- Before an exercise, to confirm the plan covers the scenarios being tested.
- Integrating an OT plan with the enterprise IR plan.

## Prerequisites

- The current OT incident response plan and any linked playbooks.
- The enterprise IR plan, for the integration review.
- Incident records from the last 24 months, where they exist.
- Contact list with dates of last verification.
- Credentials: none. This skill produces assessment documents.
- Authorization: the plan owner and operations manager accept the review findings.
- Upstream skills: `ot-incident-triage` for the decision structure the plan should match.

### Safety

This skill is passive. It produces assessment and governance documents only.

## Workflow

1. Review the plan structure against the four phases. Requirement: the plan covers the full lifecycle. Anchor: NIST SP 800-61 phases. Decision: Preparation, Detection and Analysis, Containment, Eradication and Recovery, and Post-Incident Activity each have a named section with actionable content. Trade-off accepted: a plan written in phase order reads well and is hard to use at 03:00. The fix is playbooks, not a rewrite. Flag both.
2. Review the decision authority. Requirement: the plan names who decides. Anchor: IR-1. Decision: for each incident class, the plan names the decision authority for isolation, shutdown, and notification. In OT this is the operations manager, and the plan must say so. Trade-off accepted: naming one authority concentrates decision load during an incident. A plan with a committee as the authority is a plan with no authority.
3. Review the safety gates. Requirement: the plan states that human safety and process integrity outrank containment. Anchor: 62443-2-1 4.3.4.5. Decision: the plan contains an explicit safety-first statement and every containment action references a safety check. Trade-off accepted: safety-first language slows aggressive containment decisions. In OT that slowness is the design.
4. Review escalation paths and contacts. Requirement: contacts are current and the paths are unambiguous. Anchor: IR-6. Decision: verify the contact list against reality. Names, phone numbers, and after-hours paths checked for currency with a recorded verification date. Trade-off accepted: contact verification is manual and must be repeated. An unverified contact list is the most common plan failure.
5. Review playbook coverage. Requirement: the plan has playbooks for the incident types the site will actually face. Anchor: IR-4. Decision: minimum playbook set from incident history and detection coverage: ransomware, HMI compromise, controller integrity, vendor remote access abuse, and safety system anomaly. Each playbook names its decision authority and its safety constraint. Trade-off accepted: playbooks for rare incident types are speculative and rot. Five current playbooks beat twenty stale ones.
6. Review the post-incident activity process. Requirement: lessons learned change the plan. Anchor: IR-4, IR-8. Decision: the plan defines a post-incident review with a named owner, a required output that updates the plan or its playbooks, and a deadline. Trade-off accepted: reviews cost engineering time after an event when everyone wants to move on. The deadline is what makes the review happen.
7. Review enterprise integration. Requirement: OT and enterprise plans reference each other without overwriting authority. Anchor: IR-8. Decision: the OT plan states which enterprise actions require operations review before touching OT, for example credential resets and EDR pushes. Trade-off accepted: integration creates a review dependency on the enterprise SOC. That dependency is cheaper than two SOCs acting against the same plant independently.
8. Assemble `ir-plan-review.md` from `references/assessment-template.md`. One row per review item with a finding and a fix.

## Verification

- Correct output: one review row per item with a finding and a fix, contact list verification date recorded, playbook coverage stated against incident history.
- Gap pattern: a review with all items passing and no findings. A first-time review that finds nothing was not performed against the plan text.
- Gap pattern: contact list verified with no date. Verification without a date is unverifiable.
- Gap pattern: playbooks listed by count with no titles. A playbook inventory without named scenarios does not prove coverage of the top incident types.
- OT check: the plan names the operations manager as the isolation authority. A plan naming only the CISO as the authority is unworkable in OT regardless of how well written it is.
- OT check: the plan contains an explicit safety-first statement. A plan with aggressive containment language and no safety gate is the review's top finding.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| NIST SP 800-61 | Preparation | Phase review in step 1. |
| NIST SP 800-61 | Detection and Analysis | Phase review in step 1. |
| NIST SP 800-61 | Containment, Eradication, and Recovery | Phase review in step 1. |
| NIST SP 800-61 | Post-Incident Activity | Phase review in steps 1 and 6. |
| NIST SP 800-82r3 | IR-1 | Policy. The plan is the IR-1 artifact. |
| NIST SP 800-82r3 | IR-4 | Incident Handling. Playbook coverage in step 5. |
| NIST SP 800-82r3 | IR-6 | Incident Reporting. Escalation paths in step 4. |
| NIST SP 800-82r3 | IR-7 | Incident Response Assistance. Contact currency in step 4. |
| NIST SP 800-82r3 | IR-8 | Incident Response Plan. The plan maintenance process in step 6. |
| IEC 62443-2-1 | 4.3.4.5 | Incident response capability. Safety gates in step 3. |

