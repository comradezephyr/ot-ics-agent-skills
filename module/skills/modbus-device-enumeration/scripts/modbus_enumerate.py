#!/usr/bin/env python3
"""Enumerate Modbus register windows for a unit and write a CSV."""

import argparse
import csv
import sys

from pymodbus.client.sync import ModbusTcpClient

MAX_COUNT = 125
WINDOWS = [(0, 9999), (10000, 19999), (30000, 39999)]


def read_range(client, reader, start, end):
    rows = []
    for address in range(start, end + 1, MAX_COUNT):
        count = min(MAX_COUNT, end - address + 1)
        result = reader(client, address, count)
        if result.isError():
            code = getattr(result, "exception_code", None)
            label = f"error 0x{code:02x}" if code is not None else "error"
            rows.append((address, "", label, str(result)))
            continue
        for offset, value in enumerate(result.registers):
            rows.append((address + offset, value, "", ""))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host", required=True)
    ap.add_argument("--port", type=int, default=502)
    ap.add_argument("--unit", type=int, default=1)
    ap.add_argument("--out", default="registers.csv")
    args = ap.parse_args()

    unit = args.unit
    readers = {
        0x03: lambda c, a, n: c.read_holding_registers(address=a, count=n, device_id=unit),
        0x04: lambda c, a, n: c.read_input_registers(address=a, count=n, device_id=unit),
    }

    client = ModbusTcpClient(args.host, port=args.port, timeout=5)
    if not client.connect():
        sys.exit(f"failed to connect to {args.host}:{args.port}")
    try:
        with open(args.out, "w", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(["host", "unit", "function", "address", "value", "error", "detail"])
            for start, end in WINDOWS:
                for code, reader in readers.items():
                    for address, value, error, detail in read_range(client, reader, start, end):
                        writer.writerow([args.host, args.unit, f"0x{code:02x}", address, value, error, detail])
    finally:
        client.close()


if __name__ == "__main__":
    main()
