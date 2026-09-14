# Modbus Detection Rules

Rule discipline for this file: the `modbus:` keyword resolves protocol fields correctly and is preferred over raw content matches. Never use `depth:1` content matches on port 502 unless the first byte of the wire format has been confirmed on this deployment. Every rule below uses the native keyword. Site variables `$PLC_SERVERS`, `$HMI_SERVERS`, and `$UNIT_WHITELIST` are defined in `suricata.yaml`.

## Suricata rules

Write function codes from non-whitelisted sources. Codes: 0x05 write single coil, 0x06 write single register, 0x0F write multiple coils, 0x10 write multiple registers.

```
alert tcp !$HMI_SERVERS any -> $PLC_SERVERS 502 (msg:"ICS modbus write single register from non-HMI source"; flow:to_server,established; modbus: function 0x06; sid:1000101; rev:1;)
alert tcp !$HMI_SERVERS any -> $PLC_SERVERS 502 (msg:"ICS modbus write single coil from non-HMI source"; flow:to_server,established; modbus: function 0x05; sid:1000102; rev:1;)
alert tcp !$HMI_SERVERS any -> $PLC_SERVERS 502 (msg:"ICS modbus write multiple registers from non-HMI source"; flow:to_server,established; modbus: function 0x10; sid:1000103; rev:1;)
alert tcp !$HMI_SERVERS any -> $PLC_SERVERS 502 (msg:"ICS modbus write multiple coils from non-HMI source"; flow:to_server,established; modbus: function 0x0F; sid:1000104; rev:1;)
```

Writes to non-whitelisted unit IDs. The unit whitelist blocks an adversary that has already reached the segment from addressing arbitrary slaves.

```
alert tcp any any -> $PLC_SERVERS 502 (msg:"ICS modbus write to non-whitelisted unit"; flow:to_server,established; modbus: function 0x06; modbus: unit !0x01; sid:1000111; rev:1;)
```

If the installed Suricata build does not support stacked `modbus:` keywords, split the rule per unit or use a raw content match anchored after the MBAP header. The MBAP header is 7 bytes and the unit ID is byte 6, so `content:"|01|"; offset:6; depth:1;` matches unit 0x01.

Rapid register writes. Three writes to the same PLC inside 10 seconds indicate script-driven modification, not operator activity.

```
alert tcp !$HMI_SERVERS any -> $PLC_SERVERS 502 (msg:"ICS modbus rapid register writes"; flow:to_server,established; modbus: function 0x06; detection_filter:track by_src, count 3, seconds 10; sid:1000121; rev:1;)
```

Register scanning. READ function codes 0x01 through 0x04 hitting many units from one source.

```
alert tcp any any -> $PLC_SERVERS 502 (msg:"ICS modbus register scan"; flow:to_server,established; modbus: function 0x03; detection_filter:track by_src, count 20, seconds 60; sid:1000131; rev:1;)
```

Out-of-hours writes. The `hour` and `weekday` keywords are Suricata-native. Adjust the window to the site shift schedule.

```
alert tcp any any -> $PLC_SERVERS 502 (msg:"ICS modbus write outside shift hours"; flow:to_server,established; modbus: function 0x10; hour:20,21,22,23,0,1,2,3,4,5; weekday:saturday,sunday; sid:1000141; rev:1;)
```

## Zeek policy

New master-slave pairs and unit ID spoofing. Zeek's modbus analyzer provides `ModbusHeaders` with `function_code` and `unit_id`. The script below alerts on pairs not present in the baseline file `site/modbus-baseline.tsv` (columns: src, dst, unit).

```zeek
@load base/protocols/modbus

export {
    redef enum Log::ID += { MODBUS_ANOMALY };
    global baseline: set[string];
}

event zeek_init()
    {
    Input::add_table([$source="site/modbus-baseline.tsv", $table=baseline,
                      $idx=IdxPair, $val=ValNone, $want_record=F]);
    }

type IdxPair: record {
    src: string;
    dst: string;
    unit: string;
};

event modbus_message(c: connection, headers: ModbusHeaders, is_orig: bool)
    {
    if ( is_orig )
        return;
    local key = fmt("%s,%s,%d", c$id$orig_h, c$id$resp_h, headers$unit_id);
    if ( key !in baseline )
        Log::write(MODBUS_ANOMALY, [$ts=network_time(), $src=c$id$orig_h,
                   $dst=c$id$resp_h, $unit=headers$unit_id,
                   $fc=headers$function_code, $note="unseen master-slave-unit pair"]);
    }
```

Rapid write counting in Zeek, complementary to the Suricata detection filter:

```zeek
global write_counts: table[addr] of count &default=0;

event modbus_message(c: connection, headers: ModbusHeaders, is_orig: bool)
    {
    if ( !is_orig )
        return;
    if ( headers$function_code in {5, 6, 15, 16} )
        {
        write_counts[c$id$orig_h] += 1;
        if ( write_counts[c$id$orig_h] > 50 )
            NOTICE([$note=Modbus::Write_Storm, $src=c$id$orig_h,
                    $msg=fmt("over 50 modbus writes from %s", c$id$orig_h)]);
        }
    }
```

## Test evidence

Each rule ships with a replay test. Capture a scripted write sequence with tshark, then replay:

`suricata -r modbus-test.pcapng -c /etc/suricata/suricata.yaml -l test-output/`

Expected: one `alert` entry per rule in `test-output/eve.json` with the matching `signature_id`. Record the test date per sid in the triage runbook.

