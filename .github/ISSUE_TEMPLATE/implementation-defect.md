---
name: Implementation defect
title: "defect: "
about: Report behavior that violates documented Z semantics
---

## Current status and authorized phase

Confirm that `docs/STATUS.md` was reviewed. State the exact implementation or certification phase in which the defect was observed.

## Observed behavior

## Expected behavior

Link the governing document and section.

## Exact environment

Record these identities separately when applicable:

1. implementation-host tuple;
2. candidate or certified release tuple;
3. source commit and tree;
4. kernel, Cloud Hypervisor, firmware, guest, and SSH profile identities;
5. machine identity and lifecycle state.

Do not substitute the implementation-host tuple for a product release tuple.

## Reproduction

Provide exact commands and preconditions without including secrets.

## Evidence

Include logs, exit status, process identity, relevant file digests, positive and negative observations, and cleanup state. Remove secrets.

## Claim and blast-radius boundary

State which capability is disproven, which adjacent claims remain valid, and whether the issue indicates implementation-host tuple drift.

## Data safety

State whether machine disks or metadata may be at risk. Do not destroy ambiguous durable state to simplify reproduction.
