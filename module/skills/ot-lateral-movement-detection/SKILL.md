---
name: ot-lateral-movement-detection
description: Detect lateral movement between Purdue levels including RDP and SMB crossings, non-adjacent level flows, vendor tunnel reuse, and jump host sessions to unapproved targets. Use when monitoring the OT boundary for adversary staging.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-MON-ot-lateral-movement-detection
  author: comradezephyr
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0886
# allowed-tools: Read Grep Bash
---

## When to Use

- Monitoring the OT boundary for level-crossing traffic outside approved conduits.
- Hunting for RDP, SMB, or SSH sessions that cross Purdue levels.
- Investigating a vendor tunnel used outside its approved window.
- Post-incident sweep for adversary staging between zones.

## Prerequisites

- Suricata 7.x on the boundary span. Zeek 5.x on the same span.
- `purdue-map.csv` from `ot-firewall-rule-review` or site documentation. One row per subnet: network, level.
- Approved conduit list: which flows cross which levels, with windows for vendor access.
- Python 3.10 or newer for the triage script.
- Credentials: none for analysis. IDS reload rights for deployment.
- Authorization: boundary owner sign-off for rule deployment. Live test traffic is gated.
- Upstream skills: `passive-ot-network-discovery` for the flow baseline.

### Safety

This skill is passive by default. Active steps are gated in the Workflow section.

- Passive. Authors rules and analyzes captures and IDS logs. Safe to run during normal operations.

## Workflow

1. Load `purdue-map.csv` and classify the boundary sensors. Every rule below keys on the `$L1_NETS`, `$L2_NETS`, `$L3_NETS`, `$L35_NETS`, `$L4_NETS` variables.
2. Author the ruleset from `references/detection-rules.md`. The rules cover RDP, SMB, SSH, and WinRM crossings by adjacency class.
3. Validate offline: `suricata -T -c /etc/suricata/suricata.yaml` and `zeek -C -r baseline.pcapng site/lateral-movement.zeek`, with the optional policy from `references/detection-rules.md` saved under `site/`.
4. Deploy the ruleset to the boundary sensors:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   Copy the rules to each sensor and reload with `suricatasc -c reload-rules`.
5. Prove the rules fire using offline replay only. Build a test capture on a bench segment with one RDP session crossing L3 to L2 and one SMB session crossing L3 to L1:
   `suricata -r lateral-test.pcapng -c /etc/suricata/suricata.yaml -l test-output/`
6. Generate live crossing traffic only if replay cannot exercise a rule:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   One approved RDP session from the L3 jump host to a test target in L2, inside the maintenance window.
7. Run the triage script on production telemetry:
   `python3 scripts/lateral_movement_triage.py --eve /var/log/suricata/eve.json --zeek conn.log --purdue-map purdue-map.csv --out lateral-movement-triage.md`
   The script classifies each flow as adjacent or non-adjacent. Non-adjacent crossings are findings regardless of alert status.
8. Correlate with vendor access windows. A tunnel session outside its approved window is a finding even when the flow itself is on the conduit list.
9. Tune against the 72 hour baseline. Adjacent crossings that are approved conduits must not alert. Non-adjacent crossings always alert.

## Verification

- Correct output: `lateral-movement-triage.md` has one row per crossing with source, destination, levels, protocol, adjacency class, and window status. Non-adjacent crossings are listed as findings.
- Failure mode: every flow classifies as non-adjacent. `purdue-map.csv` is missing subnets or has wrong levels. Fix the map before reporting.
- Failure mode: no alerts on the replay test. The sensor span does not carry the boundary VLANs. Verify the span covers the L3.5 choke points.
- OT check: zero non-adjacent crossings over a 72 hour baseline. A steady non-adjacent flow means the map or the conduit list is wrong, not that the rule is broken.
- OT check: confirm the jump host reached only its approved targets during the baseline. A jump session to a non-approved target is a finding even when adjacent.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 5.1 | Network segmentation. Non-adjacent level crossings are segmentation violations observed at runtime. |
| IEC 62443-3-3 | SR 5.2 | Zone boundary protection. The rules monitor the boundary the SR 5.2 requirement defines. |
| IEC 62443-3-3 | SR 6.2 | Continuous monitoring. The ruleset is the boundary monitoring capability. |
| ATT&CK for ICS | T0886 | Remote Services. RDP, SSH, and SMB crossings are the T0886 staging path. |
| ATT&CK for ICS | T0884 | Connection Proxy. Vendor tunnels and jump hosts are the proxy points. |
| ATT&CK for ICS | T0888 | Remote System Information Discovery. Crossing traffic often precedes discovery scanning. |
| NIST SP 800-82r3 | SC-7 | Boundary Protection. The crossing monitor verifies SC-7 enforcement at runtime. |
| NIST CSF 2.0 | DE | Detect. Family level. Site assigns specific subcategories. |


Row-by-row justification lives in `references/standards.md`.
