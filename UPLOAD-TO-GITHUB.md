# Complete the -Z- Documentation Upload

Target repository: `StealthEyeLLC/-z-`  
Target branch: `main`

## Remaining manual files

Upload these six files from the initialization package to the exact repository paths shown:

1. `docs/INVARIANTS.md`
2. `docs/ANTI-INVARIANTS.md`
3. `docs/ARCHITECTURE.md`
4. `docs/VARIANTS.md`
5. `docs/CERTIFICATION.md`
6. `docs/research/SSH-RESEARCH-AND-ARCHITECTURE.md`

Preserve the paths exactly. Do not add an enclosing package directory as an extra repository level.

The uploaded source files may still contain the former project identity. After all six paths exist remotely, perform one controlled identity-normalization pass and regenerate `SHA256SUMS.txt`.

## Verification after upload and normalization

1. Confirm every link in `docs/INDEX.md` resolves.
2. Confirm all six paths above exist on `main`.
3. Search for `StealthEyeLLC/zssh` and the former product token `zssh`; both results must be empty.
4. Search for `StealthEyeLLC/-z-`, `-Z-`, `ProxyUseFdpass`, `AF_VSOCK`, `Network None`, and `zero Z processes`; the expected discovery and governing documents should appear.
5. Confirm `evidence/README.md` says no implementation evidence exists yet.
6. Verify every entry in `SHA256SUMS.txt` against the final repository content.

GitHub code-search indexing may not be immediate after upload. Root indexes and explicit links remain authoritative during indexing delay.
