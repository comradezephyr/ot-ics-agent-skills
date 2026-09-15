---
name: ot-remote-access-audit
description: Audit VPN configurations, jump hosts, and remote access paths into OT, including vendor tunnels, modems, MFA coverage, and session logging. Use when reviewing remote paths before an account hygiene pass.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-ASM-ot-remote-access-audit
  author: comradezephyr
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0886
# allowed-tools: Read Grep Bash
---

## When to Use

- Reviewing remote paths before an account hygiene pass.
- Responding to a vendor remote session incident.
- Validating that every remote path enforces MFA.
- Change review for a new VPN headend or jump host.

## Prerequisites

- VPN headend config exports, CA and AAA logs, jump host session logs.
- Authorized vendor account and contact list.
- Site modem and cellular router inventory.
- Credentials: read-only to the VPN and jump host configs, or an evidence pack from the platform owner.
- Authorization: IT and OT owner sign-off. Config inspection is passive. A live path test is gated.
- Upstream skills: none.

### Safety

This skill is passive by default. Active steps are gated in the Workflow section.

- Passive. Config and log review. Sends no packets. Safe to run during normal operations.

## Workflow

1. Load the config exports and logs.
2. Enumerate every remote path into OT: site-to-site VPN, remote-access VPN, vendor tunnel, modem, cellular router.
3. For each path record: endpoints, protocol, owner, MFA status, session logging status, session duration limit.
4. Decision point: a path with no MFA is a High finding. Move it to the top of the findings list.
5. Check session logging. Jump host and VPN sessions must produce audit records readable for 90 days. Missing logs are findings.
6. Check the authorized user list against the accounts. An account that connects but appears in no authorization record is a finding.
7. Optional live verification of one jump host path, only when the site authorizes it:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   `ssh -o StrictHostKeyChecking=accept-new <jump-host>` and confirm: MFA challenge appears, session banner shows, session closes on timeout.
8. Produce `remote-access-findings.md`. One row per path: endpoints, MFA, logging, session limit, authorized status, severity.

## Verification

- Correct output: one row per remote path, MFA coverage recorded for every path, session logs reviewed for 90 day retention.
- Failure mode: session log retention is under 90 days. The logging pipeline is broken. Investigate before the next review.
- Failure mode: an account in the VPN logs appears in no authorization record. Account review gap.
- OT check: no unmanaged modem or cellular router appears in the inventory.
- OT check: jump host sessions to L1 or L2 show a gateway hop, and no direct jump from the internet-facing VPN segment to L1.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 1.1 | Identification and authentication of human users. MFA checks in steps 4 and 7. |
| IEC 62443-3-3 | SR 6.2 | Continuous monitoring. Session log review in step 5. |
| ATT&CK for ICS | T0886 | Remote Services. Every remote path is an entry point for T0886. |
| ATT&CK for ICS | T0884 | Connection Proxy. Vendor tunnels and jump hosts are proxy points. |
| NIST SP 800-82r3 | AC-2 | Account Management. The authorized user cross-check in step 6. |
| NIST CSF 2.0 | PR | Protect. Family level. Site assigns specific subcategories. |
