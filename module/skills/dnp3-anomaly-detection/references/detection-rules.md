# DNP3 Detection Rules

Rule discipline for this file: the `dnp3:` keyword resolves protocol fields and is preferred over raw content matches. DNP3 runs over TCP 20000 with its own data link layer. Never use `depth:1` content matches on port 20000. Site variables `$DNP3_MASTERS` and `$DNP3_OUTSTATIONS` are defined in `suricata.yaml`.

## Suricata rules

Function codes appearing as commands from non-master sources. Codes: 2 WRITE, 3 SELECT, 4 OPERATE, 5 DIRECT_OPERATE, 13 COLD_RESTART.

```
alert tcp !$DNP3_MASTERS any -> $DNP3_OUTSTATIONS 20000 (msg:"ICS dnp3 direct operate from non-master"; flow:to_server,established; dnp3_func:129; sid:1000201; rev:1;)
alert tcp !$DNP3_MASTERS any -> $DNP3_OUTSTATIONS 20000 (msg:"ICS dnp3 cold restart from non-master"; flow:to_server,established; dnp3_func:13; sid:1000202; rev:1;)
alert tcp any any -> $DNP3_OUTSTATIONS 20000 (msg:"ICS dnp3 direct operate without select-operate"; flow:to_server,established; dnp3_func:5; sid:1000203; rev:1;)
```

If the installed build names the keyword differently, check the available fields with `suricata --list-keywords | grep dnp3` and use the raw content match anchored on the DNP3 data-link start byte 0x0564 in place of the keyword.

Time sync manipulation. DNP3 time and date writes land on object group 2 variation 1 for class data or object group 50 for time. A WRITE against group 50 from a non-master is a time sync attack.

```
alert tcp !$DNP3_MASTERS any -> $DNP3_OUTSTATIONS 20000 (msg:"ICS dnp3 time sync write from non-master"; flow:to_server,established; content:"|05 64|"; content:"|c4|"; distance:8; within:4; sid:1000211; rev:1;)
```

File transfer function codes. Codes 14 through 18 cover file operations. Legitimate SCADA masters rarely use them.

```
alert tcp any any -> $DNP3_OUTSTATIONS 20000 (msg:"ICS dnp3 file transfer function code"; flow:to_server,established; dnp3_func:14; sid:1000221; rev:1;)
```

Auth bypass attempts. DNP3 SA objects (group 120) carry authentication. Object requests on group 120 with unusual function codes indicate authentication probing.

```
alert tcp any any -> $DNP3_OUTSTATIONS 20000 (msg:"ICS dnp3 auth object probing"; flow:to_server,established; content:"|05 64|"; content:"|78|"; distance:10; within:6; sid:1000231; rev:1;)
```

## Zeek policy

Zeek's DNP3 analyzer exposes `dnp3_header_block`, which carries the link addresses, and `dnp3_application_response_header`, which carries the function code. Save the script as `site/dnp3-anomaly.zeek`. The master opens the connection, so responses always arrive with `is_orig` false.

Outstation impersonation. One outstation link address answered from two different IPs is a rogue master or an impersonated outstation. Unsolicited responses are function code 0x82; outstation behaviour outside the polling schedule is worth an analyst look.

```zeek
@load base/protocols/dnp3
@load base/frameworks/notice

module DNP3Watch;

export {
    redef enum Notice::Type += {
        Address_Sharing,
        Unsolicited_Outside_Polling,
    };

    ## Outstation link address to the source IPs that have answered for it.
    global outstation_ips: table[count] of set[addr];
}

event dnp3_header_block(c: connection, is_orig: bool, len: count, ctrl: count,
                        dest_addr: count, src_addr: count)
    {
    if ( is_orig )
        return;

    local ip = c$id$resp_h;
    if ( src_addr !in outstation_ips )
        outstation_ips[src_addr] = set();
    add outstation_ips[src_addr][ip];

    if ( |outstation_ips[src_addr]| > 1 )
        NOTICE([$note=Address_Sharing, $src=c$id$orig_h, $dst=ip,
                $msg=fmt("outstation link address %d answered by %s and another IP",
                         src_addr, ip)]);
    }

event dnp3_application_response_header(c: connection, is_orig: bool,
                                       application: count, fc: count, iin: count)
    {
    if ( is_orig || fc != 0x82 )
        return;

    NOTICE([$note=Unsolicited_Outside_Polling, $src=c$id$resp_h, $dst=c$id$orig_h,
            $msg="unsolicited response from outstation, verify the polling schedule"]);
    }
```

## Test evidence

Build the replay capture on a bench segment with scapy DNP3 frames. Never generate DIRECT_OPERATE, COLD_RESTART, or file transfer traffic against a live outstation. Replay with `suricata -r dnp3-test.pcapng -c /etc/suricata/suricata.yaml -l test-output/` and confirm one alert per sid in `test-output/eve.json`.

