# Framework Mappings: it-ot-convergence-risk-assessment

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a design decision in the Workflow section. Keep both files in sync.

## IEC 62443-3-2

### risk assessment

Applies to decisions 2, 4, and 7. Path decomposition, likelihood and impact rating, and pre-stated go or no-go criteria are the 62443-3-2 risk assessment applied to the convergence scope.

### zone and conduit design

Applies to decision 3. Paths are classified against the existing zone and conduit design. A path that does not fit the design is a redesign requirement.

## IEC 62443-3-3

### SR 5.1

Network segmentation.

Applies to decisions 3 and 6. The no-new-crossing decision and design-reuse mitigations keep convergence paths inside the segmentation model. SR 5.1 requires segmentation to limit the effect of an event, and a convergence path is a new event surface.

### SR 5.2

Zone boundary protection.

Applies to decision 5. DMZ termination per path enforces the boundary for enterprise-initiated data flows.

## NIST SP 800-82r3

### RA-2

Security Categorization.

Applies to decision 4. Impact is derived from the consequence-of-compromise statement of the source zone, which is the RA-2 input.

### RA-3

Risk Assessment.

Applies to decision 4. The likelihood and impact method with named justification is the RA-3 assessment.

### RA-5

Vulnerability Monitoring.

Applies to decision 5. IoT and platform vulnerability posture feeds the likelihood rating for those paths.

### CA-2

Control Assessments.

Applies to decision 7. The go or no-go criteria are the assessment criteria applied before the decision.

### SC-7

Boundary Protection.

Applies to decision 3. Path placement decisions keep the boundary intact.

## NIST CSF 2.0

### ID (Identify)

Family level. The register is an identification artifact. CSF subcategories are site specific and are not pinned by this file.

## ATT&CK for ICS

### T0884

Connection Proxy.

Applies to decision 5. SaaS monitoring platforms and data lake agents become proxy paths into OT. The per-vendor and push-only designs bound the T0884 exposure of convergence projects.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

