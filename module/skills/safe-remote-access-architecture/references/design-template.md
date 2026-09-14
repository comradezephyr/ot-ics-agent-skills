# Remote Access Design: <site or system>

Design status: <draft | reviewed | approved>
Decision authority: <operations manager for access policy>
Design owner: <name>

## 1. Roles and Access Needs

| Role | Organization | Systems Reached | Frequency | Origin Networks |
| --- | --- | --- | --- | --- |

## 2. Termination Architecture

Where sessions terminate, the broker path, and why. Anchor: IEC 62443-3-3 SR 5.1. Trade-off: <named>.

## 3. Authentication Design

MFA mechanism per role. Vendor token handling. Anchor: SR 1.1, AC-17, IA-2. Trade-off: <named>.

## 4. Identity Model

Per-human accounts, provisioning and deprovisioning owner, review cadence. Anchor: SR 1.1. Trade-off: <named>.

## 5. Session Recording

What is recorded, where stored, retention, legal constraints per role. Anchor: SR 2.8, AU-12. Trade-off: <named>.

## 6. Grant Lifecycle

Grant duration, approval workflow, expiry, disabled-between-grants rule. Anchor: AC-17. Trade-off: <named>.

## 7. Jump Host Design

Brokering model, no direct-to-OT rule, HA design. Anchor: SR 5.2. Trade-off: <named>.

## 8. Vendor Tunnels

Per-vendor source pinning, tunnel inventory table. Anchor: SR 5.2. Trade-off: <named>.

| Vendor | Tunnel | Source Addresses | Destination Zone | Grant Window |

## 9. Break-Glass Procedure

Sealed credential custody, alerting on use, post-use review. Anchor: IR-4. Trade-off: <named>.

## 10. Logging and Monitoring

SIEM forwarding, retention, alert rules. Anchor: SR 2.8, AU-6. Trade-off: <named>.

## 11. Prohibited Patterns

Explicit list of designs this architecture forbids, for auditing against drift.

## 12. Review Record

Reviewer names, dates, and the trade-offs they accepted.

