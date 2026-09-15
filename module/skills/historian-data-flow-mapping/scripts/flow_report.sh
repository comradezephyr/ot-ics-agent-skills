#!/usr/bin/env sh
# Copyright 2026 comradezephyr
# SPDX-License-Identifier: Apache-2.0
set -eu

CAP=${1:?usage: flow_report.sh capture.pcapng}

tshark -r "$CAP" -T fields -e ip.src -e ip.dst -e tcp.dstport -e udp.dstport -E separator=, |
awk -F, '
{
  port = $3
  proto = "tcp"
  if (port == "" || port == "0") {
    port = $4
    proto = "udp"
    if (port == "" || port == "0") { port = "0" }
  }
  key = proto "/" port
  flows[$1 "," $2 "," key]++
}
END {
  for (k in flows) print flows[k], k
}' |
sort -rn > flows.txt

echo "wrote flows.txt" >&2
