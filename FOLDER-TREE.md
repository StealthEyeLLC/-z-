# Repository Folder Tree

```text
.
├── .gitattributes
├── README.md
├── AGENTS.md
├── CONTRIBUTING.md
├── FOLDER-TREE.md
├── INDEX.md
├── PACKAGE-VERIFICATION.md
├── SHA256SUMS.txt
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
│   ├── STATUS.md
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
│   └── dependencies.lock.json
├── evidence/
│   ├── README.md
│   └── checkpoints/
│       └── host-kernel-transition-20260801/
│           ├── CLEANUP.txt
│           ├── ENVIRONMENT.md
│           ├── HOST-TUPLE.json
│           ├── MMU-FIX.diff
│           ├── PACKAGE-SHA256SUMS.txt
│           ├── RESULT.md
│           ├── RUNTIME-PROOF.txt
│           ├── SHA256SUMS.txt
│           ├── SOURCE-SHA256SUMS.txt
│           └── TESTS.md
├── scripts/
│   └── README.md
├── src/
│   └── README.md
└── tests/
    └── README.md
```

The structure keeps governing law shallow and searchable, separates operational status from normative architecture, and stores host-transition evidence under an immutable checkpoint directory. Product source, build scripts, and product tests have not started.
