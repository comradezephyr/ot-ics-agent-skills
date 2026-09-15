---
name: ot-security-awareness-training-plan
description: Design role-based security awareness training for OT operators, engineers, and contractors, covering topics per role, delivery, frequency, assessment, and tracking. Use when designing or improving OT security training.
version: 0.1.0
license: Apache-2.0
metadata:
  author: your-github-username
  frameworks:
    - IEC 62443-2-1
    - NIST SP 800-82r3
# allowed-tools: Read Grep Bash
---

## When to Use

- Designing OT security training for a new site or program.
- Fixing a training program after a phishing or USB-borne incident.
- Adding contractor and vendor training to an existing program.
- Aligning training with an audit or certification requirement.

## Prerequisites

- Role inventory: operators, control engineers, EWS users, contractors, executives, and their OT touchpoints.
- Incident history: which behaviors caused or enabled past incidents.
- Production schedule constraints that limit training windows.
- Assessment capability: how comprehension will be measured.
- Credentials: none. This skill produces design documents.
- Authorization: operations manager accepts the time commitment per role. Training that competes with production time is an operations decision.
- Upstream skills: `ot-incident-response-plan-review` for incident-derived topics.

### Safety

This skill is passive. It produces assessment and governance documents only.

## Workflow

1. Define the role set from OT touchpoints. Requirement: topics match what each role can actually break or protect. Anchor: IEC 62443-2-1 4.3.2.4.3. Decision: roles are operators, control engineers, EWS users, contractors, and executives. Trade-off accepted: finer role granularity improves relevance and multiplies the content maintenance burden. A role with a distinct OT touchpoint gets its own topic set.
2. Topic decision per role. Requirement: every topic is one the role can act on. Anchor: AT-3. Decision: operators get phishing, USB discipline, alarm response, and reporting paths. Control engineers get change discipline, logic backup, and remote access hygiene. EWS users get patching and software installation rules. Contractors get site access rules, USB policy, and incident reporting. Executives get their authority limits and the cost of over-broad response actions. Trade-off accepted: role-specific topics cost more to build than a single general course. A general course teaches operators nothing about controller change discipline.
3. Delivery decision. Requirement: delivery fits production schedules. Anchor: AT-3. Decision: operators get shift-aligned short modules at shift handover. Engineers get hands-on sessions tied to the change workflow. Contractors get gate-side onboarding. Trade-off accepted: distributed delivery is harder to track than a training day. Training days pull operators off production, which operations will not approve.
4. Frequency decision. Requirement: frequency matches exposure decay. Anchor: AT-2. Decision: annual baseline for all roles, plus event-driven refreshers after incidents or near misses, plus onboarding for new roles and contractors. Trade-off accepted: event-driven training competes with incident cleanup. The incident cleanup is exactly when the lesson is fresh, and the plan states the refresher happens within two weeks.
5. Assessment decision. Requirement: comprehension is measured, not attendance. Anchor: AT-4. Decision: short scenario-based assessments per role. A phishing simulation for office and operator roles with results recorded as a metric. Hands-on verification for control engineers through the change workflow. Trade-off accepted: assessments create pressure and failure records. Without assessment the plan cannot demonstrate AT-4 compliance and the records are attendance lists.
6. Tracking decision. Requirement: completion and assessment results are recorded per person. Anchor: AT-4. Decision: a tracking record with name, role, module, date, score, and due next. Trade-off accepted: tracking is admin effort and becomes a personal data record subject to retention rules. State the retention period.
7. Assemble `training-plan.md` from `references/plan-template.md`. The role-topic matrix is the core artifact.

## Verification

- Correct output: every role from the inventory has a topic set, delivery method, frequency, assessment method, and tracking record design.
- Gap pattern: a plan with no assessment method. Attendance is not comprehension. AT-4 requires security awareness techniques to be assessed.
- Gap pattern: a single generic course covering all roles. Role topics were not derived from touchpoints. Operators and executives need different content.
- Gap pattern: training frequency stated as annual with nothing event-driven. Exposure does not decay on a calendar. Post-incident refreshers are where the plan changes behavior.
- OT check: the plan covers contractors and vendors at the gate, not after they are inside. Contractor onboarding at access granting is where training changes behavior most.
- OT check: the plan states where training time comes from in the production schedule. A training plan with no named time source will not be executed.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-2-1 | 4.3.2.4.3 | Training requirement. The role-topic matrix is the 4.3.2.4.3 implementation. |
| NIST SP 800-82r3 | AT-2 | Security Awareness. The topic decision per role. |
| NIST SP 800-82r3 | AT-3 | Security Training. The delivery and role specificity decisions. |
| NIST SP 800-82r3 | AT-4 | Security Training Records. The assessment and tracking decisions. |
| NIST SP 800-82r3 | PS family | Personnel Security. Contractor onboarding coverage. |
| NIST CSF 2.0 | PR.AT | Awareness and Training. Family level. Site assigns specific subcategories. |

