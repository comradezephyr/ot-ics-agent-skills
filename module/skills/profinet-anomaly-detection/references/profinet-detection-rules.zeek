@load base/frameworks/notice
@load base/protocols/conn

module PROFINET;

export {
    redef enum Notice::Type += {
        Dcp_Set,
        Duplicate_Name,
        Arp_Conflict,
        Cycle_Disruption,
        Rt_Gap,
    };

    global known_devices: table[string] of addr &default=0.0.0.0;
    global last_rt: table[string] of double &default=0.0;
    global rt_mean: table[string] of double;
    global rt_std: table[string] of double;
    global arp_table: table[addr] of set[string];
}

function write_anomaly(note: string, src: addr, detail: string)
    {
    NOTICE([$note=note, $src=src, $msg=detail]);
    }

event arp_request(kind: count, src: addr, dst: addr, sha: string, spa: addr, tha: string, tpa: addr)
    {
    if ( spa !in arp_table )
        arp_table[spa] = set();
    add arp_table[spa][sha];
    if ( |arp_table[spa]| > 1 )
        write_anomaly(Arp_Conflict, src,
                      fmt("%s answered by %d hardware addresses", spa, |arp_table[spa]|));
    }

## DCP and RT frames ride Ethertype 0x8892. Zeek packet contents for that
## ethertype land here on most builds. Confirm field offsets against a
## captured frame before production use.
event packet_contents(c: connection, contents: string)
    {
    if ( |contents| < 10 )
        return;
    local svc = contents[9];
    local src = c$id$orig_h;

    if ( svc == 0x04 )
        write_anomaly(Dcp_Set, src, "DCP SET observed, verify commissioning window");

    if ( svc == 0x05 )
        {
        local name = find_dcp_name(contents);
        if ( name == "" )
            return;
        if ( name in known_devices && known_devices[name] != src )
            write_anomaly(Duplicate_Name, src,
                          fmt("device name %s also claimed by %s", name, known_devices[name]));
        else
            known_devices[name] = src;
        }
    }

function find_dcp_name(data: string): string
    {
    local off = strstr_offset(data, "\x02\x03");
    if ( off < 0 || |data| < off + 4 )
        return "";
    local len = byte_to_count(data[off + 3]);
    if ( len == 0 || len > 240 )
        return "";
    return substr(data, off + 4, off + 3 + len);
    }

function check_rt_gap(pair: string, now: double)
    {
    if ( pair !in rt_mean )
        return;
    local last = last_rt[pair];
    if ( last == 0.0 )
        {
        last_rt[pair] = now;
        return;
        }
    local delta = now - last;
    last_rt[pair] = now;
    if ( delta > rt_mean[pair] + 3.0 * rt_std[pair] )
        write_anomaly(Cycle_Disruption, as_addr(pair),
                      fmt("delta %.6f exceeds 3 sigma", delta));
    if ( delta > 10.0 * (rt_mean[pair] + 3.0 * rt_std[pair]) )
        write_anomaly(Rt_Gap, as_addr(pair), "missing RT frames");
    }

