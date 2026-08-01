---
name: Architecture change
title: "architecture: "
about: Propose a change to Z's governing architecture
---

## Current rule

Quote or link the exact governing text and state its precedence.

## Current operational status

Confirm that `docs/STATUS.md` was reviewed. State the current authorized build phase and whether the proposal depends on, changes, or invalidates the locked implementation-host tuple.

## Proposed rule

State the exact replacement.

## User-visible value

What capability or correctness property does this add?

## Native primitive analysis

Why cannot Linux, OpenSSH, systemd, Cloud Hypervisor, or another existing standard provide it directly?

## Added authority and complexity

List processes, privileges, durable state, protocols, dependencies, trust boundaries, host assumptions, and maintenance obligations.

## Deletion pressure

What existing complexity becomes unnecessary?

## Failure, recovery, and certification

Describe failure behavior, recovery, positive tests, negative tests, cleanup, and required evidence.

## Implementation-host and compatibility impact

State whether the proposal changes the implementation-host tuple, release tuple, kernel requirements, CPU exposure, VMM configuration, firmware, guest distribution, or SSH profile. A tuple change requires a separate evidence-backed transition; it cannot be hidden inside an architecture edit.

## Claim boundary

State what the proposal would and would not prove. Host readiness must not be represented as Z product or release certification.

## Affected documents

List every governing, status, reference, search, manifest, workflow, and evidence file that must change.

## Owner approval

Required before implementation changes architectural law.
