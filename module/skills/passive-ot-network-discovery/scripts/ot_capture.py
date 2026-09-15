#!/usr/bin/env python3
# Copyright 2026 comradezephyr
# SPDX-License-Identifier: Apache-2.0
"""Passively capture OT discovery traffic from a SPAN or TAP to a pcapng file."""

import argparse
import signal

from scapy.all import PcapWriter, sniff

FILTER = (
    "tcp port 502 or tcp port 20000 or tcp port 4840 or tcp port 44818 or "
    "tcp port 102 or udp port 2222 or udp port 20000 or udp port 4840 or "
    "udp port 44818 or ether proto 0x8892"
)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-i", "--iface", required=True)
    ap.add_argument("-o", "--out", default="capture.pcapng")
    ap.add_argument("-d", "--duration", type=int, default=3600)
    ap.add_argument("--append", action="store_true", help="append to existing capture file instead of overwriting")
    args = ap.parse_args()

    writer = PcapWriter(args.out, append=args.append, sync=False)

    def stop(_sig, _frame):
        writer.close()
        raise SystemExit(0)

    signal.signal(signal.SIGINT, stop)

    def on_packet(pkt):
        writer.write(pkt)

    sniff(iface=args.iface, filter=FILTER, prn=on_packet, store=False, timeout=args.duration)
    writer.close()


if __name__ == "__main__":
    main()
