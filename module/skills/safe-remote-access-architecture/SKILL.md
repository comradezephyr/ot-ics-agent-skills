---
name: safe-remote-access-architecture
description: Design remote access for vendors and engineers into OT with mandatory MFA, session recording, time-limited grants, jump host brokering, and a two-person break-glass procedure. Use when designing or redesigning how external parties reach OT systems.
version: 0.1.0
license: Apache-2.0
metadata:
  skill_id: otics-ARC-safe-remote-access-architecture
  author: your-github-username
  frameworks:
    - IEC 62443-3-3
    - NIST SP 800-82r3
    - ATT&CK for ICS T0886
# allowed-tools: Read Grep Bash
---

## When to Use

- Designing remote access for a new vendor, integrator, or remote operations center.
- Redesigning remote access after an audit finding or an incident.
- Replacing direct vendor tunnels or always-on accounts.
- Adding a new remote access path to an existing OT network.

## Prerequisites

- Zone and conduit design from `ot-network-segmentation-design` or the current zone map.
- List of remote access roles: vendor engineers, control engineers, integrators, remote operations staff.
- Access frequency and origin per role: how often, from which networks, to which systems.
- DMZ capacity plan from `dmz-architecture-for-ot` if the DMZ exists.
- SIEM or log platform capacity for session recording storage.
- Credentials: none. This skill produces documents.
- Authorization: security manager and operations manager review the completed design.
- Upstream skills: `ot-network-segmentation-design` for the zone map. `dmz-architecture-for-ot` for the termination point.

### Safety

This skill is passive. It produces design documents only.

## Workflow

1. Complete `references/questionnaire.md` with the access requester and the zone owners. Every access path in the final design must trace to a questionnaire answer.
2. Termination point decision. Requirement: no remote session reaches L1, L2, or L3 directly. Anchor: IEC 62443-3-3 SR 5.1. Decision: all remote sessions terminate on jump hosts in the L3.5 DMZ and are brokered from there. Trade-off accepted: an extra hop adds latency to every session and makes the DMZ a chokepoint. The chokepoint is the intent.
3. Authentication decision. Requirement: every human session authenticates with MFA. Anchor: IEC 62443-3-3 SR 1.1, NIST SP 800-82r3 IA-2. Decision: TOTP or hardware token MFA on every path. SMS is excluded because of SIM swap risk. Vendor organizations that cannot deploy MFA get hardware tokens issued by the site. Trade-off accepted: token logistics for vendors and a longer connection procedure. No MFA means no access, including during incidents except through break-glass.
4. Identity decision. Requirement: every session maps to one named human. Anchor: SR 1.1. Decision: per-vendor individual accounts. Shared vendor accounts and vendor-run credential brokers are prohibited. Trade-off accepted: account administration overhead scales with vendor headcount. The alternative is unattributable sessions, which fails SR 2.8 and every forensics workflow.
5. Session recording decision. Requirement: all vendor and remote engineer sessions are recorded. Anchor: SR 2.8, AU-12 in NIST terms. Decision: full session recording at the jump host, keystroke and screen for interactive sessions. Trade-off accepted: recording storage cost and a works-council or privacy review in some jurisdictions. If recording is legally blocked for a role, network-level command logging is the fallback and the design must say so explicitly per role.
6. Time-limited access decision. Requirement: access grants expire. Anchor: AC-17. Decision: grants carry a maximum duration of 8 hours and a maximum window, for example a maintenance visit. Accounts are disabled between grants. No standing vendor access. Trade-off accepted: re-approval overhead per visit versus the risk of standing credentials. A vendor that needs standing access for monitoring gets a data-push design through the DMZ instead, not interactive access.
7. Jump host design. Requirement: protocol brokering with no network reachability from remote users to OT hosts. Anchor: SR 5.2. Decision: users reach the jump host over the tunnel; the jump host originates the connection into OT; direct RDP, SSH, or web access from remote to OT is denied at the boundary. Trade-off accepted: jump host availability becomes critical. Run two jump hosts behind a load balancer, and treat jump host failure as an availability incident with an operations-approved workaround.
8. Vendor tunnel decision. Requirement: one tunnel per vendor, source-pinned. Anchor: SR 5.2. Decision: dedicated site-to-site tunnels with fixed source addresses per vendor. No shared vendor portals. Trade-off accepted: N tunnels to operate versus one shared portal whose compromise exposes every vendor at once.
9. Break-glass decision. Requirement: emergency access exists without MFA but cannot be used silently. Anchor: SR 7.1 context, IR-4. Decision: one break-glass account per jump host pair, credential sealed in two parts held by two people, use triggers an automatic alert to operations and security, and every use requires a post-use review. Trade-off accepted: slower emergency response, roughly 15 minutes to convene two credential holders, versus a standing bypass.
10. Logging decision. Requirement: all session events land in the SIEM. Anchor: SR 2.8, AU-6. Decision: jump host session logs, tunnel up-down events, and authentication events forward to the SIEM with 90 day minimum retention. Trade-off accepted: ingest cost.
11. Assemble `remote-access-design.md` from `references/design-template.md`. Every design section (1 through 11) must state its framework anchor and accepted trade-off. Section 12 is administrative metadata and does not require a trade-off. A design section with no trade-off named is a section where the trade-off was not examined.

## Verification

- Correct output: every role from the questionnaire appears in `remote-access-design.md` with all twelve sections filled, each design section naming its framework anchor and its accepted trade-off.
- Gap pattern: a design with MFA but no break-glass procedure is incomplete. The first incident that disables MFA reachability will be resolved by whoever is physically onsite, which is uncontrolled access.
- Gap pattern: a design that lets any vendor tunnel reach L1 directly is wrong regardless of MFA, session recording, or grant limits. The termination decision in step 2 is violated even when every other section is perfect.
- Gap pattern: a design with unlimited session duration has no AC-17 enforcement. MFA authenticates the session start, not the session length.
- Gap pattern: a design whose sections name no trade-off was not designed. It was transcribed from a checklist.
- OT check: the prohibited-patterns section names direct tunnels into L1 and shared vendor accounts explicitly. Those two patterns are the most common audit findings in remote access design.
- OT check: the design states how operators reach the HMI if the jump hosts are both down. Remote access failure must not become a process visibility failure.

## Framework Mappings

| Framework | Control or Technique ID | Relevance |
| --- | --- | --- |
| IEC 62443-3-3 | SR 1.1 | Identification and authentication of human users. MFA and per-human accounts. |
| IEC 62443-3-3 | SR 1.2 | Software process and device identification. Source-pinned tunnels. |
| IEC 62443-3-3 | SR 2.8 | Auditable events. Session recording and SIEM forwarding. |
| IEC 62443-3-3 | SR 5.1 | Network segmentation. DMZ termination, no direct remote reach into OT. |
| IEC 62443-3-3 | SR 5.2 | Zone boundary protection. Jump host brokering and per-vendor tunnels. |
| NIST SP 800-82r3 | AC-17 | Remote Access. Termination point, grant lifecycle, brokering, tunnels. |
| NIST SP 800-82r3 | IA-2 | Identification and Authentication. MFA with SMS excluded. |
| NIST SP 800-82r3 | AU-12 | Audit Record Generation. Session recording at the jump host. |
| NIST SP 800-82r3 | AU-6 | Audit Record Review. SIEM forwarding with retention. |
| ATT&CK for ICS | T0886 | Remote Services. The threat the design removes preconditions for. |
| ATT&CK for ICS | T0884 | Connection Proxy. Per-vendor tunnels bound the shared portal blast radius. |

