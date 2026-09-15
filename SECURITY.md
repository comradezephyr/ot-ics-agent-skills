# Security Policy

## Reporting a Vulnerability

If you find a security issue in any skill in this pack, open a private security advisory on GitHub. Do not open a public issue for security vulnerabilities.

## Reporting Misuse

If you believe a skill in this pack is being used in a way that violates the Apache License 2.0, in particular the NOTICE preservation requirement in Section 4(d), contact the maintainer directly. Include the repository URL and the specific skill IDs from the metadata block that appear in the alleged copy.

## Scope

These skills are designed for authorized security assessment of OT/ICS environments. They are not intended for unauthorized use.

Passive skills (network discovery, log review) are safe to run during normal operations.

Active skills (scanning, config changes, isolation) require change control approval and a tested rollback plan. See the Safety section in README.md.

## Supported Versions

The current release is tagged v0.1.0. Only the latest tagged release is supported.

## Attribution

This project is licensed under Apache License 2.0. Redistribution requires preservation of the LICENSE and NOTICE files.
