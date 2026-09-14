# Questionnaire: Remote Access Design Input

Answer per role requesting access. Answers without specifics are returned for completion.

## Role Inventory

1. Which roles need remote access? For each: organization, headcount, named individuals.
2. Which OT systems does each role need? Name zones, not individual hosts, unless access is host-specific.
3. How often does each role connect? Per week, per month, per incident.
4. From where does each role connect? Office, vendor network, home, mobile.
5. Does any role need interactive control of controllers, or only monitoring and configuration?

## Current State

6. What remote paths exist today? For each: technology, endpoint, who can use it, when last reviewed.
7. Are any current paths direct tunnels into L3 or below? List them. These are the primary redesign targets.
8. Are any accounts shared between people today? Name them.

## Authentication Capability

9. Can each vendor organization deploy MFA for their staff? Which mechanism?
10. Who provisions and revokes accounts on each side, and how fast?
11. Is SSO federation available from the requesting organization?

## Recording and Legal

12. Are there works-council, contract, or privacy constraints on session recording for any role?
13. Where must session recordings be stored geographically?
14. What is the retention requirement per contract or regulation?

## Operations Constraints

15. What is the emergency access requirement if the primary path fails during an incident?
16. Who holds break-glass authority today, and is that documented?
17. What is the maximum acceptable delay to establish an emergency session?

