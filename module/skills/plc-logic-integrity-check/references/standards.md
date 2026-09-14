# Framework Mappings: plc-logic-integrity-check

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 3.1

Communication integrity.

Applies because steps 4 and 5 compare the uploaded program against the stored hash. SR 3.1 requires integrity protection for communications. For PLC logic the integrity object is the program itself. The hash match is the evidence. A MISMATCH outside a change record means the integrity property no longer holds.

### SR 2.8

Auditable events.

Applies because step 8 records baseline hashes, CPU state, block digests, and the change record reference. SR 2.8 requires that events relevant to security be auditable. The report is the audit artifact. Without the baseline hash files from step 3, there is no audit trail, which is why step 1 verifies them first.

## ATT&CK for ICS

### T0889

Modify Program.

Applies as a detection mapping. Step 4 compares the running program to the baseline. A MISMATCH outside a change record is the observed state that T0889 leaves behind. The mapping is traceability. It does not imply the change was adversarial.

### T0843

Program Download.

Applies as a detection mapping. Step 6 cross-checks the hash result with vendor compare tools. T0843 describes an adversary using engineering software to modify control logic. The compare detects the after state of a download even when the download was not observed on the wire.

## NIST SP 800-82r3

### SI-7

Software, firmware, and information integrity.

Applies because the skill performs the SI-7 control action: detecting unauthorized changes to software. SI-7 requires that integrity of software be checked periodically. The block hash comparison is the check. If the site cannot supply a known-good baseline, this skill cannot operate, and that gap is itself a finding.

## NIST CSF 2.0

### PR (Protect)

Family level. The skill protects the integrity of control logic. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.
