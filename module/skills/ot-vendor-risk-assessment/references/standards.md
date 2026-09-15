# Framework Mappings: ot-vendor-risk-assessment

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a workflow step. Keep both files in sync.

## IEC 62443-2-4

### service provider requirements

Applies to decisions 2, 7, and 8. 62443-2-4 carries requirements for service providers delivering integration and maintenance into an ICS. The assessment consumes them from the buyer side: the vendor's security program, remote access model, and contractual obligations are the requirements this register checks. A vendor that provides integration labor into a zone is in scope for 62443-2-4 regardless of whether the vendor claims certification.

## NIST SP 800-161

### supply chain risk management

Family level. Applies to decisions 2, 8, and 10. 800-161 defines supply chain risk management as a program activity spanning tiered supplier visibility, contractual instruments, and continuous monitoring. The dimension set and weights are the site's tailoring of that program to OT vendors. This file does not pin a specific 800-161 control ID because the publication organizes its content by practice area rather than by the 800-53 numbering used elsewhere in this pack.

Note for program owners: where the site maps 800-161 to 800-53 controls internally, the natural landing points are SA-9 and SA-12, which are mapped separately below. Confirm the site's mapping before citing 800-161 IDs in external reports.

## NIST SP 800-82r3

### SA-9

External Information System Services.

Applies to decisions 4, 7, 8, and 9. SA-9 requires that external service providers be assessed for the controls they operate on the site's behalf, that the site retain the ability to audit, and that providers meet defined security requirements. The contract clause mapping in step 8 is the SA-9 instrument. The remote access scoring in step 7 is the SA-9 assessment of the provider's operational access.

### SA-12

Supply Chain Protection.

Applies to decisions 5 and 6. SA-12 covers supply chain protection across acquisition, including component transparency and vulnerability handling. SBOM availability and observed patch cadence are the two SA-12 measures this assessment can verify from outside the vendor.

### RA-3

Risk Assessment.

Applies to decision 3. Likelihood derives from the vendor's advisory posture. Impact derives from the zones the product touches. The two together produce the composite. A vendor with a poor advisory record whose product sits only in a reporting zone is a different risk from the same vendor at L1.

## ATT&CK for ICS

### T0862

Supply Chain Compromise.

Applies to the whole workflow as the threat being reduced. T0862 covers an adversary compromising a product or service before it reaches the site. The assessment reduces that risk by measuring disclosure behavior, update verifiability, and component transparency.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.
- Where a publication uses practice areas rather than control IDs, cite the publication and the practice area, and say so explicitly.
