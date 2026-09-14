# Conduit Register: <site or system>

Design status: <draft | reviewed | approved>
Design owner: <name>

## 1. Conduit Register

| Conduit | Source Zone | Destination Zone | Protocol | Direction | Source Pairs | Destination Pairs | Session Limit | Encryption | Inspection | Trade-off | Anchor |

## 2. Direction and Initiation Rules

Which zone originates sessions, reply-only flows, and named exceptions with owners.

## 3. Encryption and Inspection Decisions

Per conduit: why encryption or inspection was chosen, and what was traded away.

## 4. Session Limit Basis

Upset-condition capture reference per limit.

## 5. Default Deny Statement

The register is the allow list. Flows not listed are denied. Change process reference for new flows.

## 6. Prohibited Patterns

any/any pairs, whole-zone destinations, unlimited sessions, TLS on protocols that cannot carry it.

## 7. Review Record

Reviewer names, dates, accepted trade-offs.

