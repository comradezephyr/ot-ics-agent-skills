# Backup and Recovery Plan: <site or system>

Design status: <draft | reviewed | approved>
Plan owner: <name>

## 1. Asset Class Table

| Class | Examples | RTO | RPO | Backup Mechanism | Frequency | Offline Copy | Air-Gap Mechanism | Restore Test Interval | Owner | Trade-off |

## 2. RTO and RPO Basis

Per class: the process tolerance stated by operations that justifies the targets.

## 3. Storage Architecture

Backup network or media rotation design, retention, and custody procedure.

## 4. Air-Gap Enforcement

The architectural mechanism, not the policy statement.

## 5. Restore Test Schedule

Per class: interval, bench or spare system, owner, and where results are recorded.

## 6. Integrity Design

Hash procedure at creation and verification at test.

## 7. Safety System Backups

The SIS backup discipline and its owner.

## 8. Prohibited Patterns

Production-network-mounted backup targets, untested backups, logic backups without project files, policy-only air gaps.

## 9. Review Record

Reviewer names, dates, accepted trade-offs.

