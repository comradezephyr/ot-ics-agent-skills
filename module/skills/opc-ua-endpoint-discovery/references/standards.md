# Framework Mappings: opc-ua-endpoint-discovery

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 3.1

Communication integrity.

Applies because steps 2 and 3 record which security policies are actually used on the wire. SR 3.1 requires integrity protection for communications. A server that runs policy None fails the integrity requirement. The observed policy per endpoint is the evidence.

### SR 1.1

Identification and authentication.

Applies because step 6 records the user token types each endpoint accepts. SR 1.1 requires that human access be identified and authenticated. The token inventory is the input for the endpoint hardening decision.

## IEC 62443-4-2

### CR 1.1

Human user identification.

Component level analogue of SR 1.1. The token type list per endpoint is the component capability statement input. A server that accepts only anonymous tokens cannot satisfy CR 1.1. The skill records that fact.

## NIST SP 800-82r3

### IA-5

Authenticator management.

Applies because the policy and token inventory is the input for managing server authenticators. IA-5 requires that authenticators be managed through their lifecycle. The skill does not manage authenticators. It records the state an administrator must act on.

## ATT&CK for ICS

### T0888

Remote System Information Discovery.

Applies as adversarial-model telemetry. Enumerating OPC UA endpoints is what an adversary performs under T0888 before selecting a target. The skill runs the same query for inventory. The endpoint list is the defensive baseline. The mapping is traceability, not permission to perform the technique.

## NIST CSF 2.0

### ID (Identify)

Family level. The skill output is an endpoint, policy, and token inventory. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.
