# Questionnaire: Vendor Risk Assessment

One response set per vendor. Every score in the register traces to an answer or an artifact named here.

## Identity and Footprint

1. Vendor legal entity, ownership, and country of origin.
2. Products and services in use, per site, with version or service tier.
3. Which zones does the vendor's product or service touch? Name zones.
4. Which delivery model: on-premise product, hosted service, managed service, integration labor?

## Security Program

5. Does the vendor publish a secure development lifecycle description, for example against IEC 62443-4-1?
6. Does the vendor operate a PSIRT or a documented vulnerability disclosure process? Record the URL.
7. Which third-party audits or certifications exist, with scope and date (ISO 27001, SOC 2, IEC 62443-4-1 certificate)?
8. Who is the vendor security contact, and is there a named escalation path?

## Incident History

9. List advisories naming the vendor's product in the last 36 months, with advisory IDs.
10. What is the median days from disclosure to patch across those advisories?
11. How many critical advisories remain unpatched after 12 months?
12. Has the vendor disclosed an incident affecting customer environments? When and what scope?
13. What is the disclosure posture: proactive, reactive on discovery, or no advisories filed?

## Patch and Support Cadence

14. Stated patch cadence per product, and whether updates are signed.
15. Can updates be verified by published hash before installation?
16. Stated EOL policy, last EOL announcement, and years the product line has been supported.
17. Are firmware and software updates delivered over a channel the site can stage and verify?

## Component Transparency

18. Does the vendor provide an SBOM? In which format (SPDX, CycloneDX, other)?
19. Does the SBOM include transitive dependencies?
20. Is the SBOM regenerated at each release, and delivered on request or by default?
21. Does the vendor disclose third-party component origins and jurisdictions?

## Remote Access Model

22. What access does the vendor require: none, outbound-only data push, scheduled interactive, or standing interactive?
23. Does the vendor's access terminate in the DMZ today, or directly in OT?
24. Does the vendor accept per-session grants with MFA, or require standing accounts?
25. Does the vendor use shared accounts or per-engineer credentials?
26. Does the vendor accept session recording? Any contractual objection?

## Contract and Commercial

27. Which required clauses are present, with clause numbers: breach notification timeline, right to audit, patch support window, EOL notice, vulnerability disclosure obligation, SBOM delivery, subcontractor flow-down, escrow?
28. For missing clauses, what compensating controls can hold until renewal?
29. For vendors with no contract (open source, free tools), who owns supply continuity?
30. What is the replacement cost if the vendor is avoided: integration effort, licensing, downtime?
