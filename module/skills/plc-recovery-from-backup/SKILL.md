---
name: plc-recovery-from-backup
description: Restore a compromised or corrupted PLC from a verified backup with a rollback plan, covering integrity verification, maintenance window confirmation, restore execution, and post-restore process verification. Use when PLC logic or configuration is untrusted.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-IRR-plc-recovery-from-backup
  author: comradezephyr
  frameworks:
    - IEC 62443-2-1
    - NIST SP 800-82r3
    - ATT&CK for ICS T0889
# allowed-tools: Read Grep Bash
---

## When to Use

- Restoring a controller after suspected or confirmed logic tampering.
- Recovering a corrupted controller after a failed update or malware event.
- Returning a controller to service after incident isolation.
- Rolling forward after a vendor firmware issue is resolved.

## Prerequisites

- Verified backup of the controller logic and configuration with `sha256sum` files.
- A second known-good backup for the rollback plan.
- Maintenance window approved by the operations manager.
- Connection type and rack/slot data per the controller inventory.
- python-snap7 or the vendor download tool for the platform.
- Credentials: engineering access on the controller.
- Authorization: operations manager approves the restore. Safety engineer confirms the process can tolerate the controller stopping.
- Upstream skills: `plc-logic-integrity-check` for the baseline hash method. This skill reuses its verification approach.

### Safety

This skill is active. Every step that touches the controller is gated in the Workflow section.

- Active. Applies restores to live controllers. Requires operations manager approval, a safety engineer review, and a maintenance window.

## Workflow

> SAFETY: If at any point the action risks human safety or process integrity, halt and escalate to the operations lead before continuing.

1. Verify backup integrity before any controller contact:
   `sha256sum -c backup.sha256`
   A failed check means the backup is untrusted. Do not restore from it. Find another recovery point.
2. Record the rollback plan. Before any change, capture the controller's current state: logic hash, CPU mode, and configuration export. The rollback plan is: restore this state if the new state fails verification. If no pre-change capture is possible because the controller is already compromised, the rollback plan is the second verified backup.
3. Confirm the target identity and state:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   `python3 -c "import snap7; c=snap7.client.Client(); c.Connect('<ip>',0,<slot>); i=c.GetCpuInfo(); print(i.ModuleTypeName, i.CpuState)"`
   Confirm the module type matches the backup's target controller. A mismatch aborts the restore.
4. Confirm the maintenance window with the operations manager. This step will interrupt process. The controller must stop to accept a restore. Confirm with operations before proceeding and record the approval time.
5. Apply the restore:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   `python3 module/skills/plc-logic-integrity-check/scripts/plc_logic_integrity.py --ip <ip> --rack 0 --slot 1 --blocks <blocks> --baseline-dir restore/ --capture`
   Then download the verified logic with the vendor tool or snap7 upload in reverse. Use the vendor download procedure for the platform. Restore execution follows the vendor's download procedure. The skill defines the gates around it.
6. Verify the logic matches the backup:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   `python3 module/skills/plc-logic-integrity-check/scripts/plc_logic_integrity.py --ip <ip> --rack 0 --slot 1 --blocks <blocks> --baseline-dir restore/ --out plc-recovery-record.md`
   Status must be MATCH for every block.
7. Return the controller to RUN and confirm the process state:
   - CPU state returns to 8 (RUN).
   - Interlocks and safety chains show healthy status.
   - Process values return to the expected operating band within the control engineer's tolerance.
8. If verification failed or the process did not return to the expected state, execute the rollback plan from step 2. Escalate to the operations manager and safety engineer.
9. Produce `plc-recovery-record.md`. Sections: backup identity and hashes, target confirmation, window approval, restore actions with timestamps, verification results, process confirmation, rollback plan and its status.

## Verification

- Containment confirmed: the restored logic hash matches the verified backup for every block, and the controller accepts only connections from the approved engineering stations.
- Process safety confirmed: CPU state is RUN (8), interlocks show healthy, process values are inside the operating band, and no new alarms fired after the restore.
- No new problems confirmed: the restore introduced no logic changes beyond the backup. The post-restore hash equals the pre-restore target hash. Any delta between the backup and the running logic after restore is a new problem.
- OT check: the controller never entered fault state during the restore. A fault during download means the platform's download procedure was violated. Halt and consult the vendor documentation.
- OT check: the safety engineer confirms interlock function before the process resumes full-rate operation. A restore that touches interlock logic requires a safety function test per the site's proof test procedure.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-2-1 | 4.3.4.5 | Incident response. Recovery is part of the response capability. |
| IEC 62443-3-3 | SR 7.2 | Resource management. Verified backups are the managed resource the restore depends on. |
| IEC 62443-3-3 | SR 7.1 | Denial of service protection. The rollback plan bounds the recovery time. |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. Hash verification is the integrity check on the restore. |
| NIST SP 800-82r3 | CP-9 | System Backup. The verified backup is the CP-9 artifact. |
| NIST SP 800-82r3 | CP-10 | System Recovery. The restore procedure is the CP-10 action. |
| NIST SP 800-82r3 | IR-4 | Incident Handling. Recovery within the response procedure. |
| NIST CSF 2.0 | RC | Recover. Family level. Site assigns specific subcategories. |
| ATT&CK for ICS | T0889 | Modify Program. The restore removes tampered logic and restores approved logic. |

