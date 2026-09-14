# SIS Detection Rules

Rule discipline: SIS engineering protocols are proprietary over TCP. Do not raw-match deep inside proprietary payloads. Anchor on the TCP layer and the known ports, then flag by source set and connection direction. Port numbers in this file are the commonly observed engineering ports: TriStation 5001, HIMA 1233, Yokogawa ProSafe and Safety Manager vary by deployment, DeltaV SIS rides DeltaV transport. Confirm per controller in the inventory and correct the rules before deployment.

## Suricata rules

Engineering connections from non-approved stations. Any SIS engineering session from outside `$SIS_ENG_HOSTS` is a finding.

```
alert tcp !$SIS_ENG_HOSTS any -> $SIS_SERVERS 5001 (msg:"ICS triconex engineering access from non-approved host"; flow:to_server,established; sid:1000401; rev:1;)
alert tcp !$SIS_ENG_HOSTS any -> $SIS_SERVERS 1233 (msg:"ICS hima engineering access from non-approved host"; flow:to_server,established; sid:1000402; rev:1;)
```

SIS to BPCS writes. The SIS consumes process data. Session initiation from a SIS controller toward BPCS servers on process write ports is architecturally wrong.

```
alert tcp $SIS_SERVERS any -> $BPCS_SERVERS 502 (msg:"ICS sis initiating modbus write to bpcs"; flow:to_server,established; sid:1000411; rev:1;)
```

Repeated connection attempts to a SIS from any source. Enumeration or attack staging on a safety controller is High regardless of success.

```
alert tcp any any -> $SIS_SERVERS any (msg:"ICS sis connection scan"; flow:to_server; detection_filter:track by_src, count 10, seconds 60; sid:1000421; rev:1;)
```

Bypass and override are detected in the SIS audit trail, not on the wire, on most platforms. The network rule set catches the access that enables them.

## Audit trail review

Per platform, the review targets:

- Triconex: TriStation event log. Bypass events, SOE (sequence of events) records, and program download events.
- HIMA: audit log with user attribution per change.
- Yokogawa ProSafe: event journal with bypass and override records.
- Honeywell Safety Manager: event log with MOC references.
- Emerson DeltaV SIS: DeltaV event journal filtered to the SIS node.

Record per entry: timestamp, user or station, action, permit or MOC reference. An action with no reference is a finding.

## Sensor disagreement check

Compare SIS and BPCS readings for the same process point in the historian. The check runs per tagged point pair:

1. Pull both series from the historian for the review window.
2. Compute the absolute difference per scan cycle.
3. Difference within sensor tolerance is normal. Sustained difference beyond tolerance is a finding.
4. A SIS reading frozen at a constant while the BPCS reading is dynamic is a High finding. Frozen safety telemetry precedes undetected trip failure.

## Test evidence

Bench replay only. Build `sis-test.pcapng` with one engineering connection from a non-approved host to port 5001, and one connection attempt burst. Replay with `suricata -r sis-test.pcapng -c /etc/suricata/suricata.yaml -l test-output/` and confirm sids 1000401 and 1000421 fire. Never replay bypass, override, or setpoint commands toward a live SIS controller.

