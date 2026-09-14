# Framework Mappings: engineering-workstation-hardening-audit

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 1.1

Identification and authentication of human users.

Applies because the script enumerates local administrators and the analysis flags shared and generic accounts. SR 1.1 requires unique identification and authentication of human users. A shared local admin credential defeats accountability on the EWS.

### SR 6.2

Continuous monitoring.

Applies because the JSON output is a repeatable per-station snapshot. SR 6.2 requires the capability to monitor security-relevant events. Running the check on a schedule and diffing snapshots is the monitoring loop for EWS state.

### SR 2.8

Auditable events.

Applies because the audit records patch level, USB policy, and installed software per station with a collection date. SR 2.8 requires security-relevant events to be auditable. The snapshot is the audit record for the station at a point in time.

## ATT&CK for ICS

### T0887

Wireless Compromise.

Applies as a threat mapping. The USB removable storage check closes the path T0887 covers for media-based compromise, including wireless-adjacent transfer paths. A station with `usb_deny_all` at 0 is exposed to T0887 adjacent techniques such as T0847, Replication Through Removable Media.

### T0893

Data from Local System.

Applies as a threat mapping. Unauthorized remote access agents found in `remote_agents` are the persistence an adversary uses to collect from the EWS under T0893. The agent check is the detection surface.

## NIST SP 800-82r3

### SI-2

Flaw Remediation.

Applies because the patch check measures time since the newest installed hotfix. SI-2 requires flaws to be identified and corrected within defined timeframes. The 90 day threshold is the skill default. The site defines its own SI-2 timeframe and the check reports against it.

### CM-7

Least Functionality.

Applies because AppLocker enforcement state and remote agent inventory measure whether the station runs only approved software. CM-7 requires configuring the system to provide only essential capabilities. NotConfigured AppLocker and unlisted agents are CM-7 gaps.

## NIST CSF 2.0

### PR (Protect)

Family level. The skill protects the EWS estate by measuring hardening state. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

