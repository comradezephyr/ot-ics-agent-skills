@load base/frameworks/notice

module PROFINET;

export {
    redef enum Notice::Type += {
        Dcp_Set,
        Duplicate_Name,
        Arp_Conflict,
        Cycle_Disruption,
        Rt_Gap,
    };

    ## Offsets are counted from the first byte that Zeek hands to
    ## packet_contents() for the frame. Confirm them on one captured frame
    ## from this segment before deployment. The defaults assume the frame
    ## starts at the PROFINET FrameID.
    const frame_id_offset = 0 &redef;
    const service_id_offset = 2 &redef;
    const dcp_block_offset = 12 &redef;
    const dcp_name_option = 0x02 &redef;
    const dcp_name_suboption = 0x03 &redef;

    const dcp_set = 0x04 &redef;
    const dcp_identify = 0x05 &redef;

    const dcp_frame_first = 0xFEFC &redef;
    const dcp_frame_last = 0xFEFF &redef;
    const rt_frame_first = 0x8000 &redef;
    const rt_frame_last = 0xBFFF &redef;

    ## Frames used to estimate the update interval before gaps are scored.
    const rt_warmup = 20 &redef;
    const rt_sigma = 3.0 &redef;
    const rt_gap_factor = 10.0 &redef;

    ## Station name to source MAC, learned from Identify responses.
    global known_devices: table[string] of string &default="";
}

type RtState: record {
    last: time &default=0sec;
    samples: count &default=0;
    sum: double &default=0.0;
    sumsq: double &default=0.0;
};

global rt_state: table[string] of RtState &default=RtState();

function report(note: Notice::Type, msg: string)
    {
    NOTICE([$note=note, $msg=msg]);
    }

function byte_at(data: string, offset: count): count
    {
    # Zeek string indexing starts at 1.
    if ( offset + 1 > |data| )
        return 0;
    return bytestring_to_count(data[offset + 1]);
    }

function word_at(data: string, offset: count): count
    {
    return byte_at(data, offset) * 256 + byte_at(data, offset + 1);
    }

function dcp_name(data: string): string
    {
    local offset = dcp_block_offset;
    while ( offset + 4 <= |data| )
        {
        local option = byte_at(data, offset);
        local suboption = byte_at(data, offset + 1);
        local block_len = word_at(data, offset + 2);
        if ( block_len == 0 )
            {
            # Padding block, two bytes of header only.
            offset += 2;
            next;
            }
        if ( offset + 4 + block_len > |data| )
            return "";
        if ( option == dcp_name_option && suboption == dcp_name_suboption )
            {
            local name = "";
            local i: count = 1;
            while ( i <= block_len )
                {
                name = name + data[offset + 4 + i];
                i += 1;
                }
            return name;
            }
        # Blocks are padded to an even length.
        offset += 4 + block_len + (block_len % 2);
        }
    return "";
    }

function check_rt(mac: string, now: time)
    {
    local state = rt_state[mac];
    if ( state$last == 0sec )
        {
        state$last = now;
        rt_state[mac] = state;
        return;
        }

    local delta = interval_to_double(now - state$last);
    state$last = now;
    if ( state$samples < rt_warmup )
        {
        state$samples += 1;
        state$sum += delta;
        state$sumsq += delta * delta;
        rt_state[mac] = state;
        return;
        }

    local samples = count_to_double(state$samples);
    local mean = state$sum / samples;
    local variance = state$sumsq / samples - mean * mean;
    local sd = variance > 0.0 ? sqrt(variance) : 0.0;
    local threshold = mean + rt_sigma * sd;

    if ( delta > threshold )
        report(Cycle_Disruption,
              fmt("update interval %.6f s exceeds %.6f s for %s", delta, threshold, mac));
    if ( delta > rt_gap_factor * threshold )
        report(Rt_Gap, fmt("%.6f s with no frame from %s", delta, mac));

    state$samples += 1;
    state$sum += delta;
    state$sumsq += delta * delta;
    rt_state[mac] = state;
    }

event bad_arp(SPA: addr, SHA: string, TPA: addr, THA: string, explanation: string)
    {
    report(Arp_Conflict, fmt("%s answered by %s: %s", SPA, SHA, explanation));
    }

event packet_contents(c: connection, contents: string)
    {
    if ( |contents| < 4 )
        return;

    local fid = word_at(contents, frame_id_offset);
    local mac = c$orig_l2_addr;

    if ( fid >= dcp_frame_first && fid <= dcp_frame_last )
        {
        local service = byte_at(contents, service_id_offset);
        if ( service == dcp_set )
            report(Dcp_Set, fmt("DCP SET from %s, confirm the commissioning window", mac));
        if ( service == dcp_identify )
            {
            local name = dcp_name(contents);
            if ( name == "" )
                return;
            if ( name in known_devices && known_devices[name] != mac )
                report(Duplicate_Name,
                      fmt("station name %s claimed by %s and %s", name, known_devices[name], mac));
            else
                known_devices[name] = mac;
            }
        return;
        }

    if ( fid >= rt_frame_first && fid <= rt_frame_last )
        check_rt(mac, network_time());
    }
