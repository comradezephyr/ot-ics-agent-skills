# Framework Mappings: ot-asset-ownership-governance

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a workflow step. Keep both files in sync.

## IEC 62443-2-1

### 4.3.2.2

Roles and responsibilities.

Applies to decisions 1, 4, and 6. The ownership matrix, lifecycle sign-off, and dispute resolution are the 4.3.2.2 implementation. 62443-2-1 requires that security responsibilities be assigned, documented, and understood.

## NIST SP 800-82r3

### CM-8

System Component Inventory.

Applies to decisions 1 and 5. The ownership matrix covers the inventory. CM-8 requires an inventory of system components, and ownership is the accountability layer on top of it. Unowned assets are CM-8 gaps before they are security risks.

### PM-1

Information Security Program Plan.

Applies to decision 7. The governance document is the program artifact. PM-1 requires a formal security program plan, and asset ownership is part of that plan.

### CM-3

Configuration Change Control.

Applies to decision 2. The approval alignment between this matrix and the change workflow keeps one authority per class for both governance and execution.

### CA-7

Continuous Monitoring.

Applies to decision 3. The quarterly access review is the CA-7 monitoring activity for access state per asset class.

## NIST CSF 2.0

### GV.RR

Roles, Responsibilities, and Authorities.

Applies to the whole workflow. The ownership matrix is the GV.RR artifact. It names who owns what, who approves what, and who resolves disputes.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control identifiers. Do not invent PM identifiers beyond the real family.
- If a mapping cannot be verified from skill output, remove it.
