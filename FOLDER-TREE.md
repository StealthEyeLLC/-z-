# Repository Folder Tree

```text
.
├── README.md
├── AGENTS.md
├── CONTRIBUTING.md
├── FOLDER-TREE.md
├── UPLOAD-TO-GITHUB.md
├── llms.txt
├── .github/
│   ├── copilot-instructions.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/
│       ├── architecture-change.md
│       └── implementation-defect.md
├── docs/
│   ├── INDEX.md
│   ├── MANIFEST.md
│   ├── INVARIANTS.md
│   ├── ANTI-INVARIANTS.md
│   ├── SACRIFICES.md
│   ├── SCOPE.md
│   ├── ARCHITECTURE.md
│   ├── VARIANTS.md
│   ├── SECURITY.md
│   ├── DECISIONS.md
│   ├── BUILD.md
│   ├── CERTIFICATION.md
│   ├── CHANGE-CONTROL.md
│   ├── reference/
│   │   ├── GLOSSARY.md
│   │   ├── COMPATIBILITY.md
│   │   ├── DEPENDENCIES.md
│   │   ├── IMPLEMENTATION-HOST.md
│   │   └── SEARCH-INDEX.md
│   └── research/
│       ├── INDEX.md
│       ├── SSH-RESEARCH-AND-ARCHITECTURE.md
│       ├── FINAL-DELTA-RESEARCH-2026-07-31.md
│       ├── OPERATIONAL-COMPLETENESS-STRATEGY-2026-07-31.md
│       ├── SOURCES.md
│       └── CHANGES-FROM-ORIGINAL.md
├── assets/
│   ├── README.md
│   ├── dependencies.lock.json
│   └── phase-0a-materialization.json
├── evidence/
│   ├── README.md
│   └── phase-0a/
│       ├── CERTIFICATION.json
│       └── RESULT.md
├── scripts/
│   ├── README.md
│   └── verify-phase-0a.py
├── src/README.md
└── tests/README.md
```

The structure deliberately keeps governing documents shallow and searchable. Research and reference material are separated so they cannot be mistaken for higher-precedence law.

<!-- phase-0b-checkpoint -->
## Phase 0B additions

- `assets/phase-0b-semantics.json` — certified semantic contract and candidate tuple.
- `scripts/build-phase-0b-guest.sh` — deterministic identity-free proof image builder.
- `scripts/build-phase-0b-client-root.sh` and `scripts/build-phase-0b-clients.py` — isolated client closure builders.
- `scripts/run-phase-0b.py` — private proof runner.
- `scripts/verify-phase-0b.py` — read-only committed-record and optional raw-evidence verifier.
- `tools/phase-0b/` — descriptor handoff, strict host lookup, serial reconnect, VMM API, and proof target.
- `evidence/phase-0b/` — certification record and result.
