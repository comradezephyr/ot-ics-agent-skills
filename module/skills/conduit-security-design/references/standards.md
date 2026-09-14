# Framework Mappings: conduit-security-design

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a design decision in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 5.2

Zone boundary protection.

Applies to decisions 2, 3, and 7. Direction control, pair pinning, and the default deny are the SR 5.2 design actions. A conduit register that defines the allow list makes the boundary enforceable and auditable.

### SR 3.1

Communication integrity.

Applies to decision 5. Native TLS and signing where the protocol supports them are the SR 3.1 design. For protocols that cannot carry integrity protection, the zone design bounds the exposure and the boundary adds filtering. The decision documents which layer carries integrity per conduit.

### SR 3.3

Security functionality verification.

Applies to decision 6. Inspection is placed only where the platform dissects the protocol correctly. A broken inspection proxy would fail SR 3.3 verification when tested.

### SR 7.1

Resilience against denial of service.

Applies to decision 4. Session limits sized from upset-condition captures are the SR 7.1 design per conduit.

## NIST SP 800-82r3

### SC-7

Boundary Protection.

Applies to decisions 3 and 7. The register is the SC-7 allow list implementation for zone boundaries.

### SC-10

Network Disconnect.

Applies to decisions 2 and 4. Direction control and session limits disconnect abandoned or malicious sessions.

### SC-8

Transmission Confidentiality and Integrity.

Applies to decision 5. Encryption where the protocol supports it is the SC-8 action. The register records where SC-8 is met natively and where it is not.

### AC-4

Information Flow Enforcement.

Applies to decisions 2 and 3. Flow direction and explicit pairs are the AC-4 enforcement design.

## NIST CSF 2.0

### PR (Protect)

Family level. The register is a protection design. CSF subcategories are site specific and are not pinned by this file.

## ATT&CK for ICS

### T0855

Unauthorized Command Message.

Applies to decision 6. Function-code filtering at the boundary blocks unauthorized commands crossing zones. Write codes from non-authorized sources are the T0855 observable this design stops.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

