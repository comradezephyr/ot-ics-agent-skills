# Framework Mappings: profinet-anomaly-detection

This file expands the mapping table in `SKILL.md`. Every row in that table must be traceable to a step in the Workflow section. Keep both files in sync.

## IEC 62443-3-3

### SR 6.2

Continuous monitoring.

Applies because the Zeek policy is the deployed monitoring capability for the PROFINET segment at Layer 2. SR 6.2 requires the capability to monitor security-relevant events. The policy covers DCP changes, identity conflicts, ARP behavior, and RT timing.

### SR 3.1

Communication integrity.

Applies because DCP SET commands and duplicate device names are integrity attacks on device identity. SR 3.1 requires integrity protection for communications. A rename or reassignment breaks the trusted device identity that the integrity property depends on.

### SR 7.6

Network and service availability.

Applies because cycle disruption and RT gap detection guard IO update availability. SR 7.6 requires protection against denial of service. A device that stops receiving RT frames is effectively denied.

## ATT&CK for ICS

### T0848

Rogue Master.

Applies because a duplicate device name or a second device claiming the same identity is the rogue condition. T0848 covers an adversary impersonating a legitimate station. On PROFINET the identity is the DCP device name bound to a MAC.

### T0881

Service Stop.

Applies because DCP SET commands can rename or reassign a device so that it stops exchanging RT frames with its controller. That is a service stop executed at Layer 2 without any IP-visible event.

## NIST SP 800-82r3

### SI-4

System Monitoring.

Applies because the deployed policy is the SI-4 sensor for the Layer 2 segment. SI-4 requires monitoring to detect unauthorized activity. Most IT sensors do not see this layer, which makes this policy the only monitoring control for DCP and RT behavior.

## NIST CSF 2.0

### DE (Detect)

Family level. The skill is a detection capability. CSF subcategories are site specific and are not pinned by this file.

## Update Rules

- Change `SKILL.md` and this file in the same change.
- Use real control and technique IDs. Do not invent IDs.
- If a mapping cannot be verified from skill output, remove it.

