# Framework Mappings: supply-chain-compromise-response-ot

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-2-1

### 4.3.4.5

Incident response.

Applies because a supply-chain compromise is an incident and the multi-site coordination is a handling action. 4.3.4.5 requires an incident response capability. The footprint verification and per-site isolation decisions are that capability applied across sites.

## IEC 62443-3-3

### SR 3.1

Communication integrity.

Applies because steps 2 and 9 verify the integrity of vendor-supplied artifacts. SR 3.1 requires integrity protection for communications. Firmware, project files, and updates are data in transit from the vendor. The hash verification is the integrity check.

### SR 7.2

Resource management.

Applies because the verified fix artifact is a managed resource. SR 7.2 requires managing resources so protection mechanisms function when needed. The uncompromised-channel hash check is the resource verification step.

### SR 7.6

Network and service availability.

Applies because isolation cuts the update path, not the process path. SR 7.6 requires protection of network and service availability. The process continues running while the component is contained.

## NIST SP 800-82r3

### IR-4

Incident Handling.

Applies because the workflow is the handling procedure. IR-4 requires defined handling procedures. The footprint verification, isolation, coordination, and verification steps are the procedure.

### SA-8

Security Engineering Practices.

Applies because the vendor fix is reviewed with engineering discipline before deployment. SA-8 requires that security engineering practices be applied to acquired systems. Independent verification of the fix is that practice applied during incident recovery.

## NIST CSF 2.0

### GV (Govern)

Family level. Vendor coordination, update channel policy, and per-site isolation authority are governance decisions. CSF subcategories are site specific and are not pinned by this file.

## ATT&CK for ICS

### T0862

Supply Chain Compromise.

Applies because the compromise itself enters through the vendor supply path. T0862 covers an adversary compromising a product before delivery. The update channel disable in step 7 and the independent fix verification are the response to this technique.

### T0873

Project File Infection.

Applies because compromised project files are a common delivery form for vendor component compromise. The hash baselines for project files are the detection and verification artifacts.

### T0889

Modify Program.

Applies because a compromised component can modify controller programs after deployment. The post-fix integrity check against the pre-incident baseline detects any residual T0889 state.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

