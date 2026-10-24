---
name: supply-chain-compromise-response-ot
description: Respond to a compromised vendor-supplied OT component such as PLC firmware, an HMI application, or a historian plugin, covering footprint identification, affected-site isolation, vendor coordination, and post-fix integrity verification. Use when a vendor component is confirmed or suspected compromised.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-IRR-supply-chain-compromise-response-ot
  author: comradezephyr
  frameworks:
    - IEC 62443-2-1
    - NIST SP 800-82r3
    - ATT&CK for ICS T0873
# allowed-tools: Read Grep Bash
---

## When to Use

- A vendor advisory or ICS-CERT alert names a component deployed on site.
- A compromised vendor component is confirmed at another site with shared supply.
- Firmware, project files, or a plugin from a vendor behaves outside specification.
- A vendor account or update channel is confirmed compromised.

## Prerequisites

- Asset inventory with vendor, model, firmware version, and site for every OT component.
- Update channel documentation: where vendor updates come from and how they are staged.
- Vendor emergency contact and the site escalation path.
- Integrity baselines: firmware hashes and project file hashes per component.
- Firewall access for isolating affected deployments.
- Credentials: read-only inventory and firewall admin for isolation.
- Authorization: operations manager approves per-site isolation. The safety engineer reviews any affected safety component.
- Upstream skills: `passive-ot-network-discovery` for the component footprint.

### Safety

This skill is active. Isolation changes live systems and is gated in the Workflow section.

- Active. Applies firewall changes to live deployments. Requires operations manager approval per site.

## Workflow

> SAFETY: If at any point the action risks human safety or process integrity, halt and escalate to the operations lead before continuing.

1. Confirm the decision authority. The operations manager owns each site decision. The safety engineer reviews any component with a safety function. Record both.
2. Identify the compromised component and its version. Record vendor, product, version, and the compromise indicator source: vendor advisory, ICS-CERT, or observed behavior.
3. Map the deployment footprint from the asset inventory. One row per site and component instance: site, host, version, process served, safety function yes or no.
4. Verify which sites actually run the affected version. A version check on each instance:
   `python3 -c "import snap7; c=snap7.client.Client(); c.Connect('<ip>',0,<slot>); print(c.GetCpuInfo().ModuleTypeName, c.GetCpuInfo().Version)"`
   Adjust for platform. Record actual version per instance. Inventory data is often stale.
5. Classify instances: running the affected version, running a patched version, or not affected. Only the first class is in scope for isolation.
6. Isolate affected deployments:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   Deny update-channel and vendor-access paths to the affected instances. Isolate at the network layer. Do not power off or halt a running process to contain a supply-chain risk unless the safety engineer requires it.
7. Disable the compromised update channel. Deny the staging server or update source so the component cannot fetch further payloads. Record the rule.
8. Coordinate with the vendor. Requirements for the coordination record:
   - The advisory or indicator in writing.
   - A request for a fixed version and its verification method.
   - A statement that the site will verify any fix independently before applying it.
   Do not apply a vendor patch on the vendor's word alone. A compromised update channel can deliver a second-stage payload as a fix.
9. Verify integrity after the vendor fix:
   - Hash the fixed firmware or project file against the vendor's published hash from a channel that is not the compromised one.
   - Apply the fix in a maintenance window using the `plc-recovery-from-backup` gates.
   - Re-run the integrity check against the pre-incident baseline for unaffected blocks.
10. Produce `supply-chain-response-record.md`. Sections: component identification, footprint by site, isolation rules with timestamps, update channel status, vendor coordination log, fix verification results.

## Verification

- Containment confirmed: no affected instance can reach the compromised update channel or vendor access path, deny counters increment, and unaffected sites retained their update capability.
- Process safety confirmed: all classified instances continued running their processes during isolation, no interlock trips occurred, and safety-function instances were reviewed by the safety engineer.
- No new problems confirmed: the vendor fix hash matches the published hash from an uncompromised channel, the post-fix integrity check matches the baseline for unaffected blocks, and no instance regressed during the fix.
- OT check: the version check in step 4 ran read-only against every instance and no instance entered fault state. A version probe must not change controller state.
- OT check: the fixed component passed its process-level verification. A firmware fix that changes cycle time or IO behavior is a new problem even when the hash verifies.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-2-1 | 4.3.4.5 | Incident response. The coordinated multi-site response is an incident handling action. |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. Firmware and project file hashes are the integrity checks. |
| IEC 62443-3-3 | SR 7.2 | Resource management. Verified fix artifacts are managed resources before deployment. |
| IEC 62443-3-3 | SR 7.6 | Network and service availability. Isolation preserves process availability while cutting the update path. |
| NIST SP 800-82r3 | IR-4 | Incident Handling. The workflow is the handling procedure for supply-chain compromise. |
| NIST SP 800-82r3 | SA-8 | Security Engineering Practices. Vendor fix verification applies SA-8 review discipline to the acquired product. |
| NIST CSF 2.0 | GV | Govern. Family level. Vendor coordination and update governance are GV decisions. |
| ATT&CK for ICS | T0873 | Project File Infection. Compromised project files and firmware are the delivery vehicle. |
| ATT&CK for ICS | T0889 | Modify Program. A compromised component can modify controller programs after deployment. |
| ATT&CK for ICS | T0862 | Supply Chain Compromise. The compromise itself enters through the vendor supply path. |


Row-by-row justification lives in `references/standards.md`.
