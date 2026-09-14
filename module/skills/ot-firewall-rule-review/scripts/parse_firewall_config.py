#!/usr/bin/env python3
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
        rows = list(csv.DictReader(fh))
    if not rows:
        raise SystemExit(f"{path}: no rules parsed")
    missing = RULE_FIELDS[0] not in rows[0]
    if missing:
        raise SystemExit(f"{path}: export must contain fields: {', '.join(RULE_FIELDS)}")
    return rows


def load_purdue_map(path):
    levels = {}
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            net = ipaddress.ip_network(row["network"], strict=False)
            levels[net] = row["level"].strip()
    return levels


def level_of(levels, field):
    if field.strip().lower() in ("any", ""):
        return None
    addr = ipaddress.ip_network(field, strict=False) if "/" in field else ipaddress.ip_address(field)
    for net, level in levels.items():
        if addr.version == net.version and (addr in net if isinstance(addr, ipaddress.IPv4Address) else addr.subnet_of(net)):
            return level
    return "unknown"


def check_rule(rule, levels):
    findings = []
    src = rule["source"].strip().lower()
    dst = rule["destination"].strip().lower()

    if src in ("any", "0.0.0.0/0") and dst in ("any", "0.0.0.0/0"):
        findings.append(("any-any", "source and destination unconstrained"))

    for field in ("source", "destination"):
        value = rule[field].strip()
        if value.lower() == "any":
            findings.append(("broad-conduit", f"{field} is any"))
        elif "/" in value:
            prefix = ipaddress.ip_network(value, strict=False).prefixlen
            if prefix < 24 and level_of(levels, value) in ("L1", "L2", "L3"):
                findings.append(("broad-conduit", f"{field} {value} is broader than /24 inside OT"))

    if not rule["justification"].strip():
        findings.append(("missing-justification", "no justification recorded"))
    if not rule["change_ref"].strip():
        findings.append(("missing-justification", "no change reference recorded"))

    last_hit = rule["last_hit"].strip()
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

    rules = load_rules(args.rules)
    levels = load_purdue_map(args.purdue_map)

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

