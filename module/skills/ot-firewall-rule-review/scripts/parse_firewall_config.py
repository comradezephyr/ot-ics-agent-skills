#!/usr/bin/env python3
# Copyright 2026 comradezephyr
# SPDX-License-Identifier: Apache-2.0
"""Parse a firewall rule export and flag segmentation findings."""

import argparse
import csv
import ipaddress
from pathlib import Path

RULE_FIELDS = ["name", "source", "destination", "protocol", "port", "action", "justification", "change_ref", "last_hit"]
SEVERITY = {
    "any-any": "High",
    "purdue-violation": "High",
    "broad-conduit": "Medium",
    "missing-justification": "Medium",
    "stale-rule": "Low",
}


def load_rules(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if not rows:
        raise SystemExit(f"{path}: no rules parsed")
    missing = [field for field in RULE_FIELDS if field not in fieldnames]
    if missing:
        raise SystemExit(f"{path}: export is missing fields: {', '.join(missing)}")
    return [
        {field: (row.get(field) or "").strip() for field in RULE_FIELDS}
        for row in rows
    ]


def load_purdue_map(path):
    levels = {}
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            net = ipaddress.ip_network(row["network"], strict=False)
            levels[net] = row["level"].strip()
    return levels


def level_of(levels, field):
    value = field.strip()
    if value.lower() in ("any", ""):
        return None
    try:
        if "/" in value:
            addr = ipaddress.ip_network(value, strict=False)
        else:
            addr = ipaddress.ip_address(value)
    except ValueError:
        return "unknown"
    is_network = isinstance(addr, (ipaddress.IPv4Network, ipaddress.IPv6Network))
    if is_network:
        contained = {
            level for net, level in levels.items()
            if net.version == addr.version and net.subnet_of(addr)
        }
        if len(contained) == 1:
            return contained.pop()
        if len(contained) > 1:
            return "mixed"
        return "unknown"
    for net, level in levels.items():
        if addr.version == net.version and addr in net:
            return level
    return "unknown"


def check_rule(rule, levels):
    findings = []
    src = rule["source"].lower()
    dst = rule["destination"].lower()

    if src in ("any", "0.0.0.0/0", "::/0") and dst in ("any", "0.0.0.0/0", "::/0"):
        findings.append(("any-any", "source and destination unconstrained"))

    for field in ("source", "destination"):
        value = rule[field]
        if value.lower() == "any":
            findings.append(("broad-conduit", f"{field} is any"))
        elif "/" in value:
            try:
                rule_net = ipaddress.ip_network(value, strict=False)
            except ValueError:
                findings.append(("broad-conduit", f"{field} {value} is not a valid network"))
                continue
            ot_levels = {
                level for net, level in levels.items()
                if net.version == rule_net.version
                and net.overlaps(rule_net)
                and level in ("L1", "L2", "L3")
            }
            if ot_levels and rule_net.prefixlen < 24:
                findings.append(("broad-conduit", f"{field} {value} is broader than /24 inside OT"))

    if not rule["justification"]:
        findings.append(("missing-justification", "no justification recorded"))
    if not rule["change_ref"]:
        findings.append(("missing-justification", "no change reference recorded"))

    last_hit = rule["last_hit"]
    if last_hit in ("0", "", "never"):
        findings.append(("stale-rule", f"last hit counter reads {last_hit or 'empty'}"))

    src_level = level_of(levels, rule["source"])
    dst_level = level_of(levels, rule["destination"])
    crossing = {src_level, dst_level}
    if src_level and dst_level and "L4" in crossing and crossing & {"L1", "L2"} and "L3.5" not in crossing:
        findings.append(("purdue-violation", f"flow {src_level} to {dst_level} without L3.5"))

    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rules", required=True)
    ap.add_argument("--purdue-map", required=True)
    ap.add_argument("--out", default="firewall-rule-review.md")
    args = ap.parse_args()

    try:
        rules = load_rules(args.rules)
        levels = load_purdue_map(args.purdue_map)
    except OSError as exc:
        raise SystemExit(f"{exc.filename}: {exc.strerror}")

    report_rows = []
    for rule in rules:
        for ftype, detail in check_rule(rule, levels):
            report_rows.append((rule["name"], ftype, SEVERITY[ftype], detail))

    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(f"# Firewall Rule Review\n\nTotal rules reviewed: {len(rules)}\n\n")
        fh.write("| Rule | Finding | Severity | Detail |\n")
        fh.write("| --- | --- | --- | --- |\n")
        for name, ftype, sev, detail in report_rows:
            fh.write(f"| {name} | {ftype} | {sev} | {detail} |\n")
        if not report_rows:
            fh.write("| none | | | no findings |\n")
    print(f"wrote {args.out}: {len(rules)} rules, {len(report_rows)} findings")


if __name__ == "__main__":
    main()

