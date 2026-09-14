#!/usr/bin/env python3
"""Triage Suricata eve.json alerts for Modbus rules into a grouped runbook."""

import argparse
import json
from collections import defaultdict


def load_alerts(path):
    alerts = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("event_type") == "alert":
                alerts.append(event)
    return alerts


def key_of(alert):
    src = alert["src_ip"]
    dst = alert["dest_ip"]
    unit = "n/a"
    fc = "n/a"
    if alert.get("modbus"):
        unit = alert["modbus"].get("unit_id", "n/a")
        fc = alert["modbus"].get("function", "n/a")
    return (alert["alert"]["signature_id"], alert["alert"]["signature"], src, dst, str(unit), str(fc))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("eve")
    ap.add_argument("--out", default="modbus-triage.md")
    args = ap.parse_args()

    groups = defaultdict(list)
    for alert in load_alerts(args.eve):
        groups[key_of(alert)].append(alert)

    rows = []
    for key, hits in sorted(groups.items()):
        stamps = sorted(h["timestamp"] for h in hits)
        rows.append((*key, stamps[0], stamps[-1], len(hits)))
    rows.sort(key=lambda r: (-r[-1], r[0]))

    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write("# Modbus Alert Triage\n\n")
        fh.write("| SID | Signature | Source | Destination | Unit | Function | First | Last | Count |\n")
        fh.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
        for sid, sig, src, dst, unit, fc, first, last, count in rows:
            fh.write(f"| {sid} | {sig} | {src} | {dst} | {unit} | {fc} | {first} | {last} | {count} |\n")
        if not rows:
            fh.write("| none | | | | | | | | 0 |\n")
    print(f"wrote {args.out}: {len(rows)} alert groups, {sum(r[-1] for r in rows)} alerts")


if __name__ == "__main__":
    main()

