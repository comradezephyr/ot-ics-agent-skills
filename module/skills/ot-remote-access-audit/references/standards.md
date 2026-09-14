# Framework Mappings: ot-remote-access-audit

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 1.1

Identification and authentication of human users.

Applies because steps 3 and 4 record MFA status per path and step 7 optionally verifies the MFA challenge live. SR 1.1 requires human user identification and authentication on all access paths. Remote paths are the most exposed access paths. A path without MFA fails SR 1.1 at SL2 and above.

### SR 6.2

Continuous monitoring.

Applies because step 5 verifies session logging and 90 day retention. SR 6.2 requires that the capability to monitor security-relevant events be maintained. Session logs are the monitoring evidence for remote access. Retention under 90 days is a partial implementation.

## ATT&CK for ICS

### T0886

Remote Services.

Applies as a threat mapping. Every path in the inventory is an entry point an adversary uses under T0886. The audit reduces the number of unmanaged paths. The mapping is traceability. The skill does not simulate T0886.

### T0884

Connection Proxy.

Applies as a threat mapping. Step 7 verifies that jump host sessions show a gateway hop. A direct jump from an internet-facing segment to L1 means the jump host is not acting as a proxy boundary, which is the condition T0884 exploits for staging.

## NIST SP 800-82r3

### AC-2

Account Management.

Applies because step 6 cross-checks connecting accounts against authorization records. AC-2 requires account types, eligibility, and authorization to be managed and reviewed. An account with no authorization record is an AC-2 gap.

## NIST CSF 2.0

### PR (Protect)

Family level. The skill protects the OT boundary by closing unmanaged access paths. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

