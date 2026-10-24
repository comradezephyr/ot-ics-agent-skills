#!/usr/bin/env python3
# Copyright 2026 comradezephyr
# SPDX-License-Identifier: Apache-2.0
"""Read the endpoint list from an OPC UA server and print a Markdown table.

Exit codes: 0 endpoints found, 3 server answered but returned no endpoints,
1 connection or protocol failure.
"""

import argparse
import asyncio
import sys

from asyncua import Client

DEFAULT_APPLICATION_URI = "urn:ot-ics-agent-skills:endpoint-probe"


def normalize(url):
    if "://" in url:
        return url
    return f"opc.tcp://{url}"


async def read_endpoints(url, timeout, application_uri):
    client = Client(url=url, timeout=timeout)
    client.application_uri = application_uri
    return await client.connect_and_get_server_endpoints()


def policy_name(uri):
    if not uri:
        return "none"
    return uri.rsplit("#", 1)[-1].rsplit("/", 1)[-1]


def token_names(endpoint):
    names = set()
    for token in endpoint.UserIdentityTokens or []:
        name = getattr(token.TokenType, "name", None) or str(token.TokenType)
        names.add(name)
    return ",".join(sorted(names)) if names else "none"


def format_table(endpoints):
    lines = [
        "| Endpoint | Security policy | Security mode | User tokens |",
        "| --- | --- | --- | --- |",
    ]
    for endpoint in endpoints:
        mode = getattr(endpoint.SecurityMode, "name", None) or str(endpoint.SecurityMode)
        mode = mode.replace("None_", "None")
        lines.append(
            f"| {endpoint.EndpointUrl} | {policy_name(endpoint.SecurityPolicyUri)} "
            f"| {mode} | {token_names(endpoint)} |"
        )
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--url", required=True, help="opc.tcp URL or host:port")
    ap.add_argument("--timeout", type=float, default=5.0)
    ap.add_argument("--application-uri", default=DEFAULT_APPLICATION_URI)
    ap.add_argument("--out", default="-", help="output file, - for stdout")
    args = ap.parse_args()

    url = normalize(args.url)
    try:
        endpoints = asyncio.run(read_endpoints(url, args.timeout, args.application_uri))
    except Exception as exc:
        sys.exit(f"{url}: endpoint read failed: {exc}")

    if not endpoints:
        print(f"{url}: server answered but returned no endpoints", file=sys.stderr)
        return 3

    table = format_table(endpoints)
    if args.out == "-":
        sys.stdout.write(table)
    else:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(f"# OPC UA endpoints: {url}\n\n")
            fh.write(table)
        print(f"wrote {args.out}: {len(endpoints)} endpoints", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
