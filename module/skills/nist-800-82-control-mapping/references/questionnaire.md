# Questionnaire: NIST SP 800-82 Rev. 3 Control Mapping

For each family record rating (Implemented, Partial, Absent), evidence pointer, and family lead. Answers without an evidence pointer are scored Partial at best.

## AC Access Control

- Q1. Where is the OT account list maintained and who approves new accounts?
- Q2. How often are OT accounts reviewed for orphaned or shared entries?
- Q3. Is a privilege separation enforced for engineering and operator accounts?

## AU Audit and Accountability

- Q1. Which OT systems log login, logout, and configuration events?
- Q2. What is the log retention period and who reviews the logs?

## CA Assessment, Authorization, and Monitoring

- Q1. Who authorizes changes to the OT network and on what evidence?
- Q2. Which monitoring feeds exist for OT and who triages them?

## CM Configuration Management

- Q1. Where is the EWS and PLC baseline configuration stored?
- Q2. How are configuration changes approved and recorded?

## CP Contingency Planning

- Q1. Where is the OT continuity plan? When was it last exercised?
- Q2. What is the last verified restore of PLC logic and historian data?

## IA Identification and Authentication

- Q1. How do users authenticate to OT systems? Where is MFA enforced?
- Q2. Are there shared credentials across EWS or HMIs?

## IR Incident Response

- Q1. Where is the OT incident response plan and who owns it?
- Q2. When was the last tabletop or live exercise?

## MA Maintenance

- Q1. How is vendor maintenance access approved and logged?
- Q2. Are maintenance laptops controlled before connection?

## MP Media Protection

- Q1. What is the USB and removable media policy for OT?
- Q2. Who inventories media that enters the OT network?

## PE Physical and Environmental Protection

- Q1. Which controls protect the control room and cabinet space?
- Q2. Who has physical access to PLC racks?

## PL Planning

- Q1. Where is the OT security architecture document?
- Q2. When was it last updated?

## PS Personnel Security

- Q1. What security training do OT operators and engineers receive?
- Q2. How often is the training refreshed?

## RA Risk Assessment

- Q1. When was the last OT risk assessment performed?
- Q2. What was its scope and who approved it?

## SA System and Services Acquisition

- Q1. Are OT procurement requirements defined (segmentation, patched versions)?
- Q2. Who approves OT vendor selection?

## SC System and Communications Protection

- Q1. Where do the OT firewalls and DMZ sit in the architecture?
- Q2. Which paths are encrypted and with what ciphers?

## SI System and Information Integrity

- Q1. What malware protection and whitelisting runs on EWS?
- Q2. Where is the PLC logic baseline and how is it verified?

Write one row per family into `control-coverage-matrix.md` with rating, evidence, lead, and open items.
