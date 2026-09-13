# Framework Mappings: skill-name-in-kebab-case

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 1.1

Identification and authentication of human users.

Applies because step 2 records which human account performed the access. SR 1.1 requires human access to be identified and authenticated, and the step 2 log is the evidence. If the skill performs no human-authenticated action, drop this mapping.

## NIST SP 800-82r3

### AC-2

Account Management.

Applies because step 5 checks account state on the jump host. AC-2 requires that account creation, activation, and deactivation follow defined procedures, and the step 5 output verifies the enforced state. If the skill does not touch accounts, drop this mapping.

## ATT&CK for ICS

### T0843

Program Download.

Applies because step 6 evaluates a register-write pattern consistent with an unauthorized program download. T0843 describes an adversary using engineering software to modify control logic. If the skill cannot distinguish writes from expected operator activity, drop this mapping.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.
