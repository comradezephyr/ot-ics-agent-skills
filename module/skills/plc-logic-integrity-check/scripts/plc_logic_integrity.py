#!/usr/bin/env python3
# Copyright 2026 comradezephyr
# SPDX-License-Identifier: Apache-2.0
"""Compare uploaded S7 blocks against a stored baseline."""

import argparse
import hashlib
import re
import sys
from pathlib import Path

import snap7

NAME_RE = re.compile(r"^(SDB|SFB|SFC|DB|FC|FB|OB)(\d+)$")


def parse_block(name):
    m = NAME_RE.match(name)
    if not m:
        sys.exit(f"invalid block name: {name}")
    return int(m.group(2))


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ip", required=True)
    ap.add_argument("--rack", type=int, default=0)
    ap.add_argument("--slot", type=int, default=1)
    ap.add_argument("--connection-type", type=int, default=1)
    ap.add_argument("--baseline-dir", required=True)
    ap.add_argument("--blocks", nargs="+", required=True)
    ap.add_argument("--capture", action="store_true", help="write baseline instead of comparing")
    ap.add_argument("--out", default="logic-integrity-report.md")
    args = ap.parse_args()

    client = snap7.client.Client()
    client.set_connection_type(args.connection_type)
    try:
        client.connect(args.ip, args.rack, args.slot)
    except Exception as exc:
        sys.exit(f"connection to {args.ip} failed: {exc}")

    rows = []
    baseline = Path(args.baseline_dir)
    baseline.mkdir(parents=True, exist_ok=True)

    for name in args.blocks:
        block_num = parse_block(name)
        try:
            blob = client.upload(block_num)
        except Exception as exc:
            rows.append((name, 0, "", "ERROR", str(exc)))
            continue
        digest = sha256(blob)
        bin_path = baseline / f"{name}.bin"
        hash_path = baseline / f"{name}.sha256"
        if args.capture:
            bin_path.write_bytes(blob)
            hash_path.write_text(digest + "\n")
            rows.append((name, len(blob), digest, "BASELINE", ""))
            continue
        if not hash_path.exists():
            rows.append((name, len(blob), digest, "NEW", ""))
            continue
        expected = hash_path.read_text().strip()
        status = "MATCH" if digest == expected else "MISMATCH"
        rows.append((name, len(blob), digest, status, ""))

    client.disconnect()

    if args.capture:
        print(f"wrote baseline for {len(rows)} blocks to {baseline}")
        return

    overall = "PASS" if all(r[3] == "MATCH" for r in rows) else "FAIL"
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(f"# Logic Integrity Report: {args.ip}\n\n")
        fh.write("| Block | Size | SHA-256 | Status | Detail |\n")
        fh.write("| --- | --- | --- | --- | --- |\n")
        for name, size, digest, status, detail in rows:
            fh.write(f"| {name} | {size} | {digest} | {status} | {detail} |\n")
        fh.write(f"\nOverall: {overall}\n")
    print(f"wrote {args.out}: {overall}")


if __name__ == "__main__":
    main()
