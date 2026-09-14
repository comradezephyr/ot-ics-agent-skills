# DMZ Architecture: <site or system>

Design status: <draft | reviewed | approved>
Design owner: <name>

## 1. Boundary Flow Inventory

| Flow | Direction | Source | Destination | Protocol | Business Function | Placement Decision |

## 2. Service Matrix

| Service | Zone | IT Side Access | OT Side Access | Mechanism | Trade-off | Anchor |

## 3. Data Diode and Firewall Decisions

Per flow: diode or firewall, the criteria applied, and the cost trade-off accepted.

## 4. Historian Replication Design

Push mechanism, DMZ copy topology, consumer access, freshness bound.

## 5. Jump Host Design

Reference to the remote access design, HA model, session recording.

## 6. Patch Staging Design

Staging server, hash verification, pull mechanism into OT, channel isolation from vendor updates.

## 7. Vendor Access Termination

Tunnel termination points and the per-vendor table.

## 8. Identity Design

OT-side authentication services, one-way replication, domain independence statement.

## 9. DMZ Operations

Patching cadence, monitoring, backup, and the DMZ owner.

## 10. Prohibited Patterns

DMZ-to-L1/L2 session initiation, enterprise domain dependence, unpatched DMZ services, hidden second paths around diodes.

## 11. Review Record

Reviewer names, dates, accepted trade-offs.

