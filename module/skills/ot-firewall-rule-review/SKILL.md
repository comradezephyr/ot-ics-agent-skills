---
name: ot-firewall-rule-review
description: Review industrial firewall rule exports for any-any rules, overly broad conduits, missing justification, stale rules, and Purdue boundary violations. Use when auditing rule sets on Tofino, Hirschmann, Cisco IE, Fortinet, or Palo Alto in OT mode.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-ASM-ot-firewall-rule-review
  author: comradezephyr
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0886
# allowed-tools: Read Grep Bash
---

## When to Use

- Periodic review of firewall rule sets protecting OT zones.
- Before or after a segmentation redesign.
- Investigating traffic observed in a Purdue level it should not reach.
- Change review for a new conduit request.

## Prerequisites

- Rule export from each firewall. The `references/questionnaire.md` file defines the required export fields.
- Network to Purdue level mapping for the site. One row per subnet: network, Purdue level.
- Firewall platform docs for export format: Tofino, Hirschmann EAGLE, Cisco IOS/ASA, FortiGate, Palo Alto.
- Credentials: read-only firewall admin or an operator-provided export.
- Authorization: firewall owner sign-off. Config review is passive.
- Upstream skills: `passive-ot-network-discovery` for observed flow baselines.

### Safety

This skill is passive by default. Active steps are gated in the Workflow section.

- Passive. Parses exported rule files. Sends no packets. Safe to run during normal operations.

## Workflow

1. Collect rule exports from every firewall on the OT boundary. Required fields per rule: name, source, destination, protocol, port, action, justification, change reference, last hit counter.
2. Map each site subnet to its Purdue level. Store as `purdue-map.csv` with columns: network, level.
3. Parse and flag:
   `python3 scripts/parse_firewall_config.py --rules <rules.csv> --purdue-map purdue-map.csv --out firewall-rule-review.md`
   The parser flags:
   - any-any rules. Source and destination both unconstrained.
   - overly broad conduits. Source or destination prefix shorter than /24 inside OT, or source set to any.
   - missing justification or missing change reference.
   - stale rules. Last hit counter at zero, or no hit record for 180 days.
   - Purdue violations. Any flow from L1 directly to L4, or from L4 directly to L1 or L2 without an L3.5 hop.
4. Cross-check flagged rules against observed flows from `passive-ot-network-discovery`. A flagged rule with recent observed traffic is a live exposure. A flagged rule with no traffic confirms it is unused.
5. Decision point: an any-any rule on an OT boundary firewall is a High finding regardless of observed traffic. A Purdue violation is High when it crosses from L4 to L1 or L2.
6. Produce `firewall-rule-review.md`. One row per finding: firewall, rule name, finding type, severity, evidence, recommended replacement rule.

## Verification

- Correct output: every rule in the export appears in the parse run, findings carry rule names and evidence, and `firewall-rule-review.md` states the total rule count reviewed.
- Failure mode: the parser reports zero rules parsed. The export format does not match the required fields. Fix the export before trusting a clean result.
- Failure mode: every rule is flagged stale. The last hit counters were reset or never enabled on the platform. Confirm counter availability per firewall model before reporting.
- OT check: confirm no rule allows inbound sessions to L1 from any network outside the OT zones. Modbus and DNP3 endpoints at L1 accept connections. They should not receive them from L4.
- OT check: confirm historian and replication conduits at L3.5 are pinned to explicit hosts. A conduit rule to a whole L3 subnet is a finding.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 5.1 | Network segmentation. Rule findings are segmentation gaps. |
| IEC 62443-3-3 | SR 5.2 | Zone boundary protection. Purdue violation checks enforce the boundary. |
| IEC 62443-4-2 | CR 5.2 | Zone boundary protection at the component level for embedded firewalls. |
| ATT&CK for ICS | T0886 | Remote Services. Permissive rules are the path T0886 uses. |
| NIST SP 800-82r3 | SC-7 | Boundary protection. The rule set is the boundary control under review. |
| NIST CSF 2.0 | PR | Protect. Family level. Site assigns specific subcategories. |

