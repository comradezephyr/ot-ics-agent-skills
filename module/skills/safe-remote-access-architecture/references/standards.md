# Framework Mappings: safe-remote-access-architecture

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a design decision in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 1.1

Identification and authentication of human users.

Applies to decisions 3 and 4. MFA on every path and per-human accounts are the SR 1.1 design actions. The shared-account prohibition is what makes authentication attributable. A design that retains shared vendor accounts does not satisfy SR 1.1 regardless of MFA, because authentication no longer proves which human acted.

### SR 1.2

Software process and device identification.

Applies to decision 8. Source-pinned tunnels identify the remote device, not just the user. A tunnel that accepts connections from any source address does not satisfy SR 1.2 at the network layer.

### SR 2.8

Auditable events.

Applies to decisions 5 and 10. Session recording and SIEM forwarding are the SR 2.8 design actions. The prohibition of unrecorded paths is the enforcement. A design with a path that bypasses recording has an SR 2.8 gap by construction.

### SR 5.1

Network segmentation.

Applies to decision 2. DMZ termination means no remote session has direct network reach into L1 through L3. SR 5.1 requires segmentation to limit the effect of an event. The remote path is the most exposed path and therefore terminates at the outermost zone.

### SR 5.2

Zone boundary protection.

Applies to decisions 7 and 8. Brokering and per-vendor tunnels enforce the L3.5 boundary for remote sessions. SR 5.2 requires denial of unauthorized communication across zone boundaries.

## NIST SP 800-82r3

### AC-17

Remote Access.

Applies to decisions 2, 6, 7, and 8. Termination in the DMZ, expiring grants, brokering, and per-vendor tunnels are the AC-17 control implementations. AC-17 requires authorization and encryption for remote access. The 8 hour grant bound is the site's AC-17 enforcement decision.

### IA-2

Identification and Authentication, organizational users.

Applies to decision 3. MFA with a phishing-resistant or TOTP factor is the IA-2 design. SMS exclusion is the IA-2 hardening decision against SIM swap.

### AU-12

Audit Record Generation.

Applies to decision 5. Recording at the jump host generates the audit record set for remote sessions.

### AU-6

Audit Record Review.

Applies to decision 10. SIEM forwarding with retention makes the generated records reviewable.

## ATT&CK for ICS

### T0886

Remote Services.

Applies as the threat being designed against. Remote access is the T0886 path into OT. Every decision above removes a T0886 precondition: direct reachability, standing credentials, unauthenticated sessions, and unattributed accounts.

### T0884

Connection Proxy.

Applies to decision 8. Vendor portals are proxy points whose compromise spreads to every connected vendor. Dedicated per-vendor tunnels bound the T0884 blast radius to one vendor relationship.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

