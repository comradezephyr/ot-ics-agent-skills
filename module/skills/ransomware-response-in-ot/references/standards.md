# Framework Mappings: ransomware-response-in-ot

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-2-1

### 4.3.4.5

Incident response.

Applies because the skill is the OT-specific ransomware response procedure. 4.3.4.5 requires an incident response capability for the ICS. The workflow operationalizes that capability for the ransomware case with OT safety constraints built in.

## IEC 62443-3-3

### SR 7.1

Denial of service protection.

Applies because every isolation decision balances containment against process availability. SR 7.1 requires protection against denial of network-accessible resources. An over-broad isolation is a self-inflicted denial. The rollback check in step 7 guards that.

### SR 7.2

Resource management.

Applies because step 9 protects the recovery point. SR 7.2 requires managing the capacity of resources so they are available when needed. Backups that are mounted on the network are resources the adversary can encrypt. The offline-only restore rule is the resource management control.

### SR 3.1

Communication integrity.

Applies because encrypted files, renamed archives, and corrupt project files are integrity violations. SR 3.1 requires integrity protection for communications and stored data. The ransomware indicators are the integrity failure observables.

## NIST SP 800-82r3

### IR-4

Incident Handling.

Applies because the workflow is the handling procedure. IR-4 requires that incidents be handled per defined procedures. The zone classification, isolation decisions, and coordination log are the IR-4 artifacts.

### IR-5

Incident Monitoring.

Applies because the verification section tracks incident status through process continuity checks. IR-5 requires tracking incidents and reporting status. The record and the traffic checks are the tracking evidence.

### CP-9

System Backup.

Applies because step 9 selects the recovery point under CP-9 backup discipline. CP-9 requires backup of system-level information. The offline-only rule and the hash verification are the CP-9 enforcement actions in the incident context.

### CP-10

System Recovery.

Applies because the restore path is the CP-10 action. CP-10 requires recovery capability with defined timeframes. The verified recovery point and the restore schedule are the CP-10 evidence.

## NIST CSF 2.0

### RS (Respond)

Family level. The skill is a response procedure. CSF subcategories are site specific and are not pinned by this file.

## ATT&CK for ICS

### T0880

Loss of Safety.

Applies because ransomware response actions can touch safety systems, and ransomware itself can disable safety telemetry. The OT check that watches for new bypasses and overrides during the response guards against T0880 from both directions.

### T0881

Service Stop.

Applies as a response-failure mapping. An over-broad isolation or a rushed credential reset stops OT services without stopping the adversary. The step 7 traffic check detects the self-inflicted stop.

### T0886

Remote Services.

Applies because ransomware commonly stages into OT through remote access paths. Step 6 disables L4 remote access as the containment move that closes the T0886 path.

### T0889

Modify Program.

Applies because ransomware on engineering stations can corrupt or encrypt project files. The EWS branch in the decision matrix includes a check for unauthorized program modification before the station returns to service.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

