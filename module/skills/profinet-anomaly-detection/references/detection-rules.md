# PROFINET Detection Rules

Zeek policy. PROFINET DCP and RT are Layer 2, Ethertype 0x8892. No IP stack is involved for RT traffic. The policy monitors DCP service frames, device name announcements, ARP behavior, and RT frame timing. Field names vary across Zeek and tshark versions. Confirm the available fields at deployment time with `tshark -G fields | grep pn_dcp` and adjust the extractors.

## Zeek policy: profinet-detection-rules.zeek

```zeek
@load base/frameworks/notice

export {
    redef enum Log::ID += { PROFINET_ANOMALY };
    redef enum Notice::Type += {
        PROFINET::Dcp_Set,
        PROFINET::Duplicate_Name,
        PROFINET::Arp_Conflict,
        PROFINET::Cycle_Disruption,
        PROFINET::Rt_Gap,
    };

    global known_devices: table[string] of addr &default=0.0.0.0;
    global last_rt: table[string] of double &default=0.0;
    global rt_deltas: table[string] of vector of double &default=vector();
}

event zeek_init()
    {
    Log::create_stream(PROFINET_ANOMALY, [$columns=string_array_to_set(["ts","note","src","detail"])]);
    }

function write_anomaly(note: string, src: addr, detail: string)
    {
    Log::write(PROFINET_ANOMALY, fmt("%s %s %s %s", network_time(), note, src, detail));
    }

## DCP frames arrive on Ethertype 0x8892 with a DCP service ID field.
## Zeek 5.x exposes PROFINET via the protocol analyzer; the packet layer
## below works on any build because it reads raw Ethernet payloads.
event new_connection(c: connection)
    {
    if ( c$id$resp_p != 0x8892/udp )
        return;
    }

event packet_contents(c: connection, contents: string)
    {
    ## DCP SET service id is 0x04 in the DCP service id field.
    if ( |contents| < 10 )
        return;
    local svc = contents[9];
    local src = c$id$orig_h;

    if ( svc == 0x04 )
        write_anomaly("dcp_set", src, "DCP SET observed, verify commissioning window");

    if ( svc == 0x05 )
        {
        local name = find_dcp_name(contents);
        if ( name == "" )
            return;
        if ( name in known_devices && known_devices[name] != src )
            {
            write_anomaly("duplicate_name", src,
                          fmt("device name %s also claimed by %s", name, known_devices[name]));
            NOTICE([$note=PROFINET::Duplicate_Name, $src=src,
                    $msg=fmt("duplicate device name %s", name)]);
            }
        else
            known_devices[name] = src;
        }
    }

function find_dcp_name(data: string): string
    {
    ## DCP Identify response carries the device name in an option 02, suboption 03 block.
    local opt_block = strstr(data, "\x02\x03");
    if ( |opt_block| < 4 )
        return "";
    local len = byte_to_count(opt_block[3]);
    if ( len == 0 || len > 240 )
        return "";
    return substr(opt_block, 4, 3 + len);
    }
```

ARP conflict detection. An IP that answers ARP with two different MACs is spoofing a controller or IO device. Run as a separate policy loaded in the same node.

```zeek
@load base/protocols/conn

global arp_table: table[addr] of set[string];

event arp_request(kind: count, src: addr, dst: addr, sha: string, spa: addr, tha: string, tpa: addr)
    {
    if ( spa !in arp_table )
        arp_table[spa] = set();
    add arp_table[spa][sha];
    if ( |arp_table[spa]| > 1 )
        NOTICE([$note=PROFINET::Arp_Conflict, $src=src,
                $msg=fmt("%s answered by %d hardware addresses", spa, |arp_table[spa]|)]);
    }
```

RT cycle monitoring. Feed `rt-frames.txt` deltas from the workflow into the threshold check, or run the table update inline from a custom packet event keyed on the RT frame type. The policy alerts when a pair's inter-arrival delta exceeds 3 standard deviations of the baseline or when no RT frame arrives within 10 cycle periods.

```zeek
function check_rt_gap(pair: string, now: double, mean: double, std: double)
    {
    local last = last_rt[pair];
    if ( last == 0.0 )
        {
        last_rt[pair] = now;
        return;
        }
    local delta = now - last;
    last_rt[pair] = now;
    rt_deltas[pair][|rt_deltas[pair]|] = delta;
    if ( delta > mean + 3.0 * std )
        {
        write_anomaly("cycle_disruption", as_addr(pair), fmt("delta %.6f exceeds 3 sigma", delta));
        NOTICE([$note=PROFINET::Cycle_Disruption, $msg=fmt("%s cycle delta %.6f", pair, delta)]);
        }
    if ( delta > 10.0 * (mean + 3.0 * std) )
        NOTICE([$note=PROFINET::Rt_Gap, $msg=fmt("%s missing RT frames", pair)]);
    }
```

The `as_addr` helper and the baseline loader are deployment-specific. Keep the baseline mean and standard deviation per pair in a TSV loaded at `zeek_init`, one row per controller-device pair.

## Test evidence

Build `pn-anomaly-test.pcapng` on a bench segment: one DCP SET NAME frame, two devices announcing the same name, an ARP pair with conflicting MACs, and an RT stream with a planted gap. Replay and confirm each anomaly class appears in `profinet-anomaly.log`. Record the test date with the policy version.

