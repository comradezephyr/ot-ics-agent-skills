# OT/ICS Agent Skills

## What This Is

A skill pack for OT/ICS security practitioners who run AI agents. It packages assessment, monitoring, and incident response workflows as structured runbooks for an agent to execute. The reader is expected to know the OT protocol stack, including Modbus and DNP3, and the Purdue reference model. This file is the module-level context an agent reads after the pack is installed. It is a technical reference, not a pitch.

## How to Use These Skills

Each skill in `module/skills/` is a directory containing a runbook. Every runbook follows the same structure.

- When to Use. The conditions that justify invoking this skill. Read this first. If the task does not match, pick a different skill.
- Prerequisites. Tools, credentials, network access, and upstream skills required before the workflow starts.
- Workflow. Numbered steps the agent executes in order.
- Verification. Checks that confirm each step produced a correct result.
- Framework Mappings. The framework sections this skill touches.

The agent reads the runbook before starting and executes the workflow in order. If prerequisites are unmet, it stops and reports. If verification fails, it reports what did not pass instead of continuing. Skills reference each other by directory name, so install the whole `module/` tree, not individual skills.

## Framework Mappings

Runbooks map their steps and artifacts to these frameworks.

- IEC 62443. Zone and conduit model, security levels SL1 through SL4, and the component assurance model. Skills cite the specific part, for example 62443-3-3 or 62443-4-1, where relevant.
- NIST SP 800-82 Rev. 3. ICS-specific guidance and baseline controls.
- MITRE ATT&CK for ICS. Techniques used to classify observed or suspected adversary behavior.
- Purdue Model. Reference levels L0 through L4/L5. Used to place assets, traffic, and findings within the control hierarchy.
- NIST CSF 2.0. Govern, Identify, Protect, Detect, Respond, and Recover functions for control and reporting alignment.

Mappings are traceability aids. They mark which framework section a step satisfies or which technique an indicator matches. They are not compliance declarations.

## Skill Index

Every entry is a directory under `module/skills/`. A skill tagged (planned) has not been written yet.

### Discovery and Inventory

- `passive-ot-network-discovery` (planned): passive protocol analysis to inventory OT assets without active scanning
- `modbus-device-enumeration` (planned): enumerate Modbus TCP/RTU devices, function codes, register maps
- `profinet-device-inventory` (planned): discover and fingerprint PROFINET devices via DCP
- `ethernet-ip-device-discovery` (planned): enumerate EtherNet/IP (CIP) devices and object models
- `opc-ua-endpoint-discovery` (planned): discover OPC UA servers and security policies
- `dnp3-outstation-inventory` (planned): enumerate DNP3 outstations and capabilities
- `historian-data-flow-mapping` (planned): map flows between PLCs, HMIs, historians

### Assessment and Audit

- `iec-62443-gap-assessment` (planned): assess against IEC 62443-3-3 system security requirements
- `purdue-model-zone-conduit-audit` (planned): audit zones and conduits against Purdue architecture
- `nist-800-82-control-mapping` (planned): map existing controls to NIST SP 800-82 Rev. 3
- `plc-logic-integrity-check` (planned): compare running PLC logic to known-good baseline
- `ot-remote-access-audit` (planned): audit VPN, jump host, and remote paths into OT
- `engineering-workstation-hardening-audit` (planned): assess EWS hardening gaps
- `ot-firewall-rule-review` (planned): review industrial firewall rules for permissive conduits

### Monitoring and Detection

- `modbus-anomaly-detection` (planned): detect anomalous Modbus function codes, register access, timing
- `dnp3-anomaly-detection` (planned): detect DNP3 anomalies including spoofed responses
- `profinet-anomaly-detection` (planned): detect PROFINET device spoofing and cycle disruption
- `stuxnet-style-attack-detection` (planned): detect PLC logic tampering, sensor spoofing, EWS compromise
- `historian-tampering-detection` (planned): detect unauthorized modifications to historian data
- `ot-lateral-movement-detection` (planned): detect lateral movement between Purdue levels
- `safety-instrumented-system-anomaly-detection` (planned): monitor SIS for anomalous trips and bypasses

### Incident Response

- `ot-incident-triage` (planned): triage with safety-first decision gates
- `plc-recovery-from-backup` (planned): restore PLC from verified backup with rollback plan
- `scada-hmi-incident-containment` (planned): contain compromised HMI without process disruption
- `ot-network-isolation-procedure` (planned): isolate compromised segment with minimal process impact
- `ransomware-response-in-ot` (planned): respond without shutting down production
- `supply-chain-compromise-response-ot` (planned): respond to compromised vendor-supplied component
- `post-incident-ot-forensics` (planned): preserve forensic evidence from OT devices

### Architecture and Design

- `ot-network-segmentation-design` (planned): design segmentation using Purdue and IEC 62443 zones
- `conduit-security-design` (planned): design secure conduits between OT zones
- `dmz-architecture-for-ot` (planned): design a DMZ between IT and OT networks
- `safe-remote-access-architecture` (planned): design safe remote access for vendors and engineers
- `ot-backup-and-recovery-design` (planned): design backup and recovery for PLCs, HMIs, historians
- `ot-change-management-workflow` (planned): design change management that maintains controls
- `it-ot-convergence-risk-assessment` (planned): assess risks from IT/OT convergence

### Compliance and Governance

- `nerc-cip-compliance-check` (planned): assess NERC CIP compliance
- `iec-62443-certification-readiness` (planned): prepare for IEC 62443 certification
- `ot-security-program-maturity-assessment` (planned): assess maturity against C2M2
- `ot-vendor-risk-assessment` (planned): assess security risk of OT vendors and suppliers
- `ot-incident-response-plan-review` (planned): review and improve an OT IR plan
- `ot-security-awareness-training-plan` (planned): design training for OT operators and engineers
- `ot-asset-ownership-governance` (planned): establish governance for OT asset ownership
