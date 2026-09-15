#!/usr/bin/env python3
# Copyright 2026 comradezephyr
# SPDX-License-Identifier: Apache-2.0
"""Classify observed flows as adjacent or non-adjacent Purdue level crossings."""

import argparse
import csv
import ipaddress
import json
from collections import defaultdict

ADJACENT = {
    ("L0", "L1"), ("L1", "L2"), ("L2", "L3"),
    ("L3", "L3.5"), ("L3.5", "L4"), ("L3", "L4"),
}
MANAGEMENT_PORTS = {"3389": "rdp", "445": "smb", "22": "ssh", "5985": "winrm", "5986": "winrm"}


def load_purdue_map(path):
    levels = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            levels.append((ipaddress.ip_network(row["network"], strict=False), row["level"].strip()))
    return levels


def level_of(levels, addr_text):
    try:
        addr = ipaddress.ip_address(addr_text)
    except ValueError:
        return None
    for net, level in levels:
        if addr in net:
            return level
    return "unknown"


def adjacency(a, b):
    if a is None or b is None or a == b:
        return "unknown"
    pair = (a, b)
    rev = (b, a)
    if pair in ADJACENT or rev in ADJACENT:
        return "adjacent"
    return "non-adjacent"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--eve")
    ap.add_argument("--zeek")
    ap.add_argument("--purdue-map", required=True)
    ap.add_argument("--out", default="lateral-movement-triage.md")
    args = ap.parse_args()

    levels = load_purdue_map(args.purdue_map)
    crossings = defaultdict(lambda: {"count": 0, "first": None, "last": None, "protocol": ""})

    def record(src, dst, port, protocol, ts):
        src_level = level_of(levels, src)
        dst_level = level_of(levels, dst)
        key = (src, dst, src_level, dst_level, protocol)
        row = crossings[key]
        row["count"] += 1
        row["protocol"] = protocol
        row["first"] = ts if row["first"] is None or ts < row["first"] else row["first"]
        row["last"] = ts if row["last"] is None or ts > row["last"] else row["last"]

    if args.eve:
        with open(args.eve, encoding="utf-8") as fh:
            for line in fh:
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get("event_type") != "flow":
                    continue
                port = str(event.get("dest_port", ""))
                if port not in MANAGEMENT_PORTS:
                    continue
                record(event["src_ip"], event["dest_ip"], port,
                       MANAGEMENT_PORTS[port], event.get("timestamp", ""))

    if args.zeek:
        with open(args.zeek, encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("#"):
                    continue
                cols = line.split("\t")
                if len(cols) < 10:
                    continue
                port = cols[5]
                if port not in MANAGEMENT_PORTS:
                    continue
                record(cols[2], cols[4], port, MANAGEMENT_PORTS[port], cols[0])

    rows = []
    for (src, dst, src_level, dst_level, protocol), data in crossings.items():
        rows.append((src, dst, src_level, dst_level, protocol,
                     adjacency(src_level, dst_level),
                     data["first"], data["last"], data["count"]))
    rows.sort(key=lambda r: (r[5] != "non-adjacent", r[6] or ""))

    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write("# Lateral Movement Triage\n\n")
        fh.write("| Source | Destination | Src Level | Dst Level | Protocol | Adjacency | First | Last | Count |\n")
        fh.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
        for src, dst, sl, dl, proto, adj, first, last, count in rows:
            fh.write(f"| {src} | {dst} | {sl} | {dl} | {proto} | {adj} | {first} | {last} | {count} |\n")
        if not rows:
            fh.write("| none | | | | | | | | 0 |\n")
    non_adjacent = sum(1 for r in rows if r[5] == "non-adjacent")
    print(f"wrote {args.out}: {len(rows)} crossings, {non_adjacent} non-adjacent")


if __name__ == "__main__":
    main()

