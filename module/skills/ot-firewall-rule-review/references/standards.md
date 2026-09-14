# Framework Mappings: ot-firewall-rule-review

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 5.1

Network segmentation.

Applies because every finding type maps to a segmentation defect. An any-any rule means no effective segmentation between the connected zones. An overly broad conduit means zones exist on paper but not in enforcement. The review measures the rule set against the zone model.

### SR 5.2

Zone boundary protection.

Applies because step 3 checks every rule for Purdue level crossing. SR 5.2 requires denial of unauthorized communication across zone boundaries. A rule permitting L4 to L1 without an L3.5 hop is a direct SR 5.2 failure.

## IEC 62443-4-2

### CR 5.2

Zone boundary protection at the component level.

Applies because the review scope includes embedded firewalls on industrial devices, such as switch and firewall appliances deployed inside zones. CR 5.2 carries the SR 5.2 requirement to the component. Export limits on embedded platforms are recorded in the questionnaire rather than treated as absence of the control.

## ATT&CK for ICS

### T0886

Remote Services.

Applies as a threat mapping. Permissive rules on management protocols are the network path T0886 requires. The Purdue violation and breadth checks reduce the rule surface T0886 relies on. The mapping is traceability. The skill does not simulate T0886.

## NIST SP 800-82r3

### SC-7

Boundary protection.

Applies because the rule set is the SC-7 control implementation on the OT boundary. SC-7 requires managed interface connections, deny by default, and documented exceptions. Missing justification, any-any rules, and stale rules are SC-7 documentation and enforcement gaps.

## NIST CSF 2.0

### PR (Protect)

Family level. The skill protects zone boundaries by measuring rule set state. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

