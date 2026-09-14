# Remote Access Audit Questionnaire

Answer per remote path. A path is one VPN tunnel, jump host pair, modem, or cellular router. Record the evidence document for every answer. An answer without evidence is a finding.

## Path Inventory

1. List every remote path into OT. For each: endpoints, protocol, platform owner.
2. Which paths are vendor operated? Name the vendor and the contact for each.
3. Which modems and cellular routers exist on site? Which are in the asset inventory?

## Authentication

4. Does every path enforce MFA? Name the MFA platform per path.
5. Are vendor accounts shared between vendor staff? Shared accounts are a finding.
6. Where are VPN accounts stored? Local, AAA, or directory.
7. When was the last account review on each path?

## Session Controls

8. Do all sessions route through a jump host? Which paths allow direct-to-OT sessions?
9. Is session recording in place? Which tool, and where do recordings land?
10. What is the session duration limit per path? Idle timeout?
11. Is there an authorized user list per path? Who maintains it?

## Logging and Monitoring

12. Which logs do the VPN headends emit, and to where?
13. Is log retention at least 90 days? Verify the actual retention, not the policy.
14. Who reviews remote session logs, and how often?

## Network Placement

15. Do any remote paths terminate inside L3 or lower without an L3.5 DMZ hop?
16. Do vendor tunnels reach L1 directly?
17. Are remote paths firewalled to explicit source addresses, or open to any?

