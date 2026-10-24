---
name: opc-ua-endpoint-discovery
description: Discover OPC UA servers on port 4840 and record their endpoints and security policies. Use when mapping OPC UA flows between historians, HMIs, and controllers.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-DIS-opc-ua-endpoint-discovery
  author: comradezephyr
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0888
# allowed-tools: Read Grep Bash
---

## When to Use

- Mapping OPC UA endpoints before monitoring deployment.
- Recording the security policy set (None, Basic128Rsa15, Basic256, Basic256Sha256) for the segment.
- Investigating connections rejected with BadSecurityPolicyRejected.
- Preparing an OPC UA firewall rule set.

## Prerequisites

- tshark 4.x. Verify with `tshark --version`.
- asyncua 2.x. Verify with `python -c "import asyncua; print(asyncua.__version__)"`. The bundled `scripts/opcua_endpoint_probe.py` uses it.
- SPAN port or network TAP on the segment.
- Credentials: anonymous or a read-only service account where the server enforces authentication.
- Authorization: server owner sign-off for endpoint probes.
- Upstream skills: `passive-ot-network-discovery` for the flow baseline.

### Safety

This skill is passive by default. Active steps are gated in the Workflow section.

- Passive. Captures and inspects traffic. Sends no packets. Safe to run during normal operations.

## Workflow

1. Resolve the OPC UA field names for this tshark revision:
   `tshark -G fields | grep -i opcua | grep -iE "policy|token" | head -20`
   Use the resolved names in the commands below.
2. Passive flow map:
   `tshark -r capture.pcapng -Y "opcua" -T fields -e ip.src -e ip.dst -e tcp.dstport -E separator=, | sort -u > opcua_flows.csv`
3. Record the security policies observed in OpenSecureChannel frames. Parse the resolved policy field per source address and list the distinct values. A server seen only with the policy None is a hardening finding, not a configuration fact.
4. Probe a server that never opens a SecureChannel during the window:
   > STOP: Confirm change control approval before executing this step. If approval is missing, halt and report.
   `python3 scripts/opcua_endpoint_probe.py --url opc.tcp://<ip>:4840 --out endpoints.md`
   The probe connects with the None policy, reads the endpoint list, and writes the policy, mode, and token table. Exit 3 means the server answered but returned no endpoints. Apply step 5 before recording the result.
5. Decision point: if the server answers on 4840 but returns no endpoints, the server requires a registered application URI. Rerun with `--application-uri <registered-uri>`. If it still returns nothing, record as `app-uri-gated`.
6. Write `endpoints.md`: server IP, discovered endpoint URLs, security policies, user token types, and clients observed in capture.

## Verification

- Correct output: every 4840 server has endpoints and a policy set, or an `app-uri-gated` flag. `opcua_flows.csv` lists all detected OPC UA flows.
- Failure mode: the probe exits 3 on an open 4840. The server rejects the session without a registered application URI. Rerun with `--application-uri`, then record `app-uri-gated` if it still returns nothing.
- Failure mode: the capture shows repeated BadSecurityPolicyRejected during normal operations. The client and server policy sets do not intersect.
- OT check: confirm the historian kept its OPC UA subscription running through the probe window. Post-query capture still shows periodic Publish frames from the historian client.
- OT check: confirm no server certificate changed during the window. A changed certificate indicates replacement or tampering.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 3.1 | Communication integrity. The policy set is the integrity baseline for OPC UA sessions. |
| IEC 62443-3-3 | SR 1.1 | Identification and authentication. User token types are recorded per endpoint. |
| IEC 62443-4-2 | CR 1.1 | Human user identification. The token inventory feeds the component capability statement. |
| NIST SP 800-82r3 | IA-5 | Authenticator management. The policy and token inventory supports authenticator management for servers. |
| ATT&CK for ICS | T0888 | Remote System Information Discovery. Endpoint enumeration is the same discovery an adversary runs. |
| NIST CSF 2.0 | ID | Identify. Family level. Site assigns specific subcategories. |

Row-by-row justification lives in `references/standards.md`.
