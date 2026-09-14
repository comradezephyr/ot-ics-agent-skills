# Firewall Rule Review Questionnaire

Answer per firewall. Record the evidence document for every answer. An answer without evidence is a finding.

## Export and Coverage

1. Is every firewall on the OT boundary included in the review? List any excluded unit and why.
2. Does the rule export contain all required fields: name, source, destination, protocol, port, action, justification, change reference, last hit counter?
3. If the platform cannot export last hit counters, state the platform and firmware.

## Rule Hygiene

4. Who approves new conduit rules? What record exists per approval?
5. When was the last full rule set review before this one?
6. Are there rules named temp, test, or vendor? Temporary rules past their expiry are findings.

## Change Management

7. Does every rule carry a change reference? Which system issues the references?
8. Is there a rule with no matching change record from the last audit?

## Network Placement

9. Which subnets terminate on this firewall, and at which Purdue levels?
10. Do any conduits cross L3.5 directly to L1 or L2?
11. Are management interfaces of the firewall itself reachable from L4?

## Monitoring

12. Are rule hit counters enabled platform-wide?
13. Are denied packets logged, and where do the logs go?
14. Who reviews firewall logs, and how often?

