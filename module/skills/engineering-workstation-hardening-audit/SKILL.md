---
name: engineering-workstation-hardening-audit
description: Audit OT engineering workstations (EWS) for hardening gaps covering patch level, USB policy, application whitelisting, antivirus exclusions, shared credentials, and engineering software versions. Use when assessing the EWS estate.
version: 0.1.0
license: Apache-2.0
metadata:
  author: your-github-username
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0887
# allowed-tools: Read Grep Bash
---

## When to Use

- Periodic hardening review of the EWS estate.
- Investigating EWS compromise indicators, such as unexpected engineering software installs.
- Before connecting a new EWS to the OT network.
- After a vendor engineer worked on a station.

## Prerequisites

- Local Administrator or WinRM remote access to each EWS.
- PowerShell 5.1 or newer on the targets.
- The site EWS inventory with hostnames and owners.
- Engineering software list: TIA Portal, Studio 5000, RSLogix, Wonderware, iFIX, others per site.
- Credentials: local admin on each station, or a delegated account with remote audit rights.
- Authorization: EWS owner sign-off. Remote collection is active and gated.
- Upstream skills: `passive-ot-network-discovery` to locate the stations.

### Safety

This skill is active. Collection touches live workstations and is gated in the Workflow section.

- Active. Reads live OS state over WinRM. No configuration changes. Requires change control approval.

## Workflow

1. Verify reachability without touching the target:
   `Test-NetConnection <ews-host> -Port 5985`
   A failed WinRM test means the station must be audited locally at the console.
2. Collect locally on the station:
   `powershell -ExecutionPolicy Bypass -File ews_harden_check.ps1 -Out ews-audit-<host>.json`
3. Or collect remotely from the audit host:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   `powershell -Command "Invoke-Command -ComputerName <ews-host> -FilePath ews_harden_check.ps1 -ArgumentList '-Out','ews-audit-<host>.json'"`
4. Analyze the JSON output:
   - Patch level: `hotfix_count` and the newest `InstalledOn`. Over 90 days behind is a finding.
   - USB policy: `usb_deny_all` must be 1. 0 is a finding.
   - AppLocker: `applocker_enforced` must be Enforced or Audit. NotConfigured is a finding.
   - Defender exclusions: `av_exclusion_paths` and `av_exclusion_processes`. Any exclusion covering an engineering software directory is a finding.
   - Shared credentials: `local_admins` with more than one entry needs a named owner review. Generic accounts such as `admin` are a finding.
   - Remote agents: `remote_agents` lists remote access tools. Anything outside the approved list is a finding.
   - Engineering software: cross-reference `installed_software` against the site CVE list. Known vulnerable versions are findings.
5. Decision point: if `remote_agents` contains an unauthorized remote access tool, treat the station as candidate compromised and escalate to incident response. Do not limit the finding to hardening.
6. Produce `ews-hardening-findings.md`. One row per station per check: host, check, observed, expected, severity.

## Verification

- Correct output: a JSON file per station with all seven check sections populated, and `ews-hardening-findings.md` with one row per station per check.
- Failure mode: `Invoke-Command` returns access denied. The audit account lacks remote rights. Fall back to local collection at the console.
- Failure mode: `applocker_enforced` reads NotConfigured on every station. The baseline never shipped. Report as an estate-wide gap, not per-station.
- OT check: confirm no EWS has a routable path from L4. `Get-NetRoute` output in the JSON must show no default gateway toward the enterprise network.
- OT check: confirm engineering software versions match the change record. An install date with no change record is a finding.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 1.1 | Identification and authentication. Shared and generic local admin accounts fail this. |
| IEC 62443-3-3 | SR 6.2 | Continuous monitoring. The audit output feeds the EWS monitoring baseline. |
| IEC 62443-3-3 | SR 2.8 | Auditable events. Patch, USB, and software state are recorded per station. |
| ATT&CK for ICS | T0887 | Wireless Compromise. USB policy gaps are the removable media path into the EWS. |
| ATT&CK for ICS | T0893 | Data from Local System. Unauthorized remote agents enable this technique. |
| NIST SP 800-82r3 | SI-2 | Flaw Remediation. The patch level check is the SI-2 verification action. |
| NIST SP 800-82r3 | CM-7 | Least Functionality. AppLocker and remote agent checks enforce least functionality. |
| NIST CSF 2.0 | PR | Protect. Family level. Site assigns specific subcategories. |

