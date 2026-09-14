# Lateral Movement Detection Rules

Rule discipline: management protocols run on standard ports over IP, so port-based rules are valid here. Anchor flows with the direction and state keywords before matching. Site variables `$L1_NETS`, `$L2_NETS`, `$L3_NETS`, `$L35_NETS`, `$L4_NETS` are defined in `suricata.yaml`.

## Suricata rules

RDP crossing L3 to L2 or deeper. Approved jump traffic originates from the jump host variable `$JUMP_HOSTS`; everything else alerts.

```
alert tcp !$JUMP_HOSTS any -> $L2_NETS 3389 (msg:"ICS rdp into L2 from non-jump source"; flow:to_server,established; sid:1000301; rev:1;)
alert tcp $L3_NETS any -> $L1_NETS 3389 (msg:"ICS rdp into L1 from L3"; flow:to_server,established; sid:1000302; rev:1;)
```

SMB crossing levels. SMB has no legitimate path from L3 to L1 or L2 on a segmented OT network.

```
alert tcp $L3_NETS any -> $L1_NETS 445 (msg:"ICS smb from L3 to L1"; flow:to_server,established; sid:1000311; rev:1;)
alert tcp $L3_NETS any -> $L2_NETS 445 (msg:"ICS smb from L3 to L2"; flow:to_server,established; sid:1000312; rev:1;)
alert tcp $L4_NETS any -> $L1_NETS 445 (msg:"ICS smb from L4 to L1"; flow:to_server,established; sid:1000313; rev:1;)
```

SSH sessions between non-adjacent levels.

```
alert tcp $L35_NETS any -> $L1_NETS 22 (msg:"ICS ssh from DMZ to L1 bypassing L3"; flow:to_server,established; sid:1000321; rev:1;)
alert tcp $L4_NETS any -> $L1_NETS 22 (msg:"ICS ssh from L4 to L1"; flow:to_server,established; sid:1000322; rev:1;)
```

WinRM from L4 into OT.

```
alert tcp $L4_NETS any -> $L1_NETS 5985 (msg:"ICS winrm from L4 to L1"; flow:to_server,established; sid:1000331; rev:1;)
alert tcp $L4_NETS any -> $L2_NETS 5985 (msg:"ICS winrm from L4 to L2"; flow:to_server,established; sid:1000332; rev:1;)
```

Vendor tunnel reuse. Alert on any session from the vendor tunnel subnet outside the approved window using the hour and weekday keywords. Adjust to the site window.

```
alert tcp $VENDOR_TUNNEL any -> $OT_NETS any (msg:"ICS vendor tunnel outside approved window"; flow:to_server,established; hour:0,1,2,3,4,5,6,19,20,21,22,23; weekday:saturday,sunday; sid:1000341; rev:1;)
```

## Zeek analysis

Level classification and adjacency from `conn.log`. The triage script consumes Zeek output and `purdue-map.csv` directly, so a full Zeek policy is optional. For a Zeek-native alert path:

```zeek
@load base/protocols/conn

event conn_established(c: connection)
    {
    local src = c$id$orig_h;
    local dst = c$id$resp_h;
    local svc = c$id$resp_p;
    if ( svc == 3389/tcp && Site::is_local_addr(dst) && !Site::is_local_addr(src) )
        NOTICE([$note=Netflow::Crossing, $src=src, $dst=dst,
                $msg=fmt("rdp crossing from %s to %s", src, dst)]);
    }
```

The Suricata ruleset is the primary sensor. The Zeek path provides a cross-check where Suricata is not deployed.

## Test evidence

Bench capture with one RDP session L3 to L2 and one SMB session L3 to L1. Replay with `suricata -r lateral-test.pcapng -c /etc/suricata/suricata.yaml -l test-output/`. Confirm sids 1000301 and 1000311 each fire once. Record the test date per sid.

