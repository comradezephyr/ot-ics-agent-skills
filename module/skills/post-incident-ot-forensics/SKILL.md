---
name: post-incident-ot-forensics
description: Collect and preserve forensic evidence from OT devices after an incident, ranking sources by volatility and process risk, hashing every artifact, and building the incident timeline. Use after containment when the evidence must be captured without disrupting operations.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-IRR-post-incident-ot-forensics
  author: your-github-username
  frameworks:
    - IEC 62443-2-1
    - NIST SP 800-82r3
    - ATT&CK for ICS T0889
# allowed-tools: Read Grep Bash
---

## When to Use

- Evidence collection after containment in an OT incident.
- Building an incident timeline across controllers, HMIs, historians, and network devices.
- Preserving evidence before systems are restored or re-imaged.
- Supporting legal, regulatory, or insurance follow-up on an OT incident.

## Prerequisites

- Containment record from the response skills. Evidence collection follows containment, not before.
- Decision authority confirmed: operations manager for anything that touches a running process, safety engineer for anything on a controller.
- Forensic share with controlled access and write-once storage if available.
- sha256sum or an equivalent hash tool.
- Chain-of-custody form per the site's legal or regulatory requirement.
- Credentials: read-only on logs and historian, engineering access only where gated.
- Authorization: operations manager approves evidence collection on live systems. The safety engineer approves any controller interaction.
- Upstream skills: `ot-incident-triage`, `ot-network-isolation-procedure`, and the containment record.

### Safety

This skill is passive by default. Collection reads live systems and exports files. Any step that changes a device is gated.

- Passive. Reads logs, captures traffic, exports data. Safe to run during normal operations.

## Workflow

> SAFETY: If at any point the action risks human safety or process integrity, halt and escalate to the operations lead before continuing.

1. Confirm the decision authority and record the chain-of-custody form number. Every artifact gets a custody entry from acquisition to storage.
2. Rank evidence sources by volatility and process risk using `references/decision-matrix.md`. Collect in that order. Network captures and logs are volatile and safe. Controller logic is volatile but touching a controller carries process risk, so it is last and gated.
3. Start a capture on the incident segment if not already running:
   `sudo tshark -i <iface> -w incident-capture.pcapng -b filesize:1048576`
   Ongoing adversary activity is the most perishable evidence.
4. Collect network device logs: firewall, switch, boundary routers. Export in native format. Hash on export.
5. Collect historian data: audit trail, tag archive extents, and the query results from `historian-tampering-detection`. Hash on export.
6. Collect HMI logs: session logs, audit trails, screen event history. Hash on export.
7. Collect host artifacts from powered systems: memory dumps where the platform supports it, then disk images of compromised hosts. Do not power off a host that a process depends on. Image live where required.
8. Collect controller evidence last and only with approval:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   Upload controller logic and configuration with the `plc-logic-integrity-check` script in capture mode. Confirm the CPU stayed in RUN (8) throughout. Do not run any forensic tool that reboots or stops a controller without explicit operations manager and safety engineer approval.
9. Hash and register every artifact:
   `sha256sum <artifact> >> evidence.sha256`
   Append each artifact to `forensic-evidence-register.md` with: artifact name, source system, acquisition time, collector, hash, custody entry.
10. Build the timeline. Correlate events across sources into `incident-timeline.md`. One row per event: UTC timestamp, source system, event, evidence reference. Use UTC everywhere. OT devices often drift; record the clock offset observed per source and note it in the timeline.
11. Verify the timeline covers the full incident window: first indicator to containment. Gaps are recorded as gaps, not filled by assumption.

## Verification

- Correct output: `forensic-evidence-register.md` lists every artifact with a verified hash and custody entry, and `incident-timeline.md` covers the full incident window with source-referenced events.
- Failure mode: an artifact hash fails on re-verification. The artifact changed after acquisition. Record the failure, preserve both versions, and investigate the custody gap. A hash mismatch is itself evidence.
- Failure mode: controller evidence was never collected because the process could not tolerate the gate. Record the source as not-covered with the reason. Do not treat the register as complete.
- OT check: every device touched during collection stayed in its pre-collection state. Controllers in RUN (8), historians serving collectors, no new alarms from the collection itself.
- OT check: clock offsets recorded per source reconcile the timeline. A timeline built on uncorrected device clocks is wrong by the drift amount and unusable for sequencing.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-2-1 | 4.3.4.5 | Incident response. Evidence collection supports the response capability. |
| IEC 62443-3-3 | SR 2.8 | Auditable events. The evidence is the audit record of the incident. |
| IEC 62443-3-3 | SR 6.1 | Audit log accessibility. Collection preserves the logs SR 6.1 requires to be accessible. |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. Hash verification is the integrity check on evidence. |
| NIST SP 800-82r3 | IR-4 | Incident Handling. Evidence collection is an IR-4 handling activity. |
| NIST SP 800-82r3 | IR-5 | Incident Monitoring. The timeline tracks the incident end to end. |
| NIST SP 800-82r3 | AU-9 | Protection of Audit Information. Hashes and controlled storage protect the evidence. |
| NIST CSF 2.0 | RS | Respond. Family level. Site assigns specific subcategories. |
| ATT&CK for ICS | T0889 | Modify Program. Controller logic evidence is the T0889 record. |
| ATT&CK for ICS | T0873 | Project File Infection. Project file artifacts are the T0873 evidence. |

