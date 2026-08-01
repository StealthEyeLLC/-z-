# Phase 0A negative tests

Status: **PASSED**

Executed: 35; passed: 35; failed: 0.

1. **PASS** — wrong Debian InRelease digest rejected
2. **PASS** — invalid Debian signature rejected
3. **PASS** — unexpected signer fingerprint rejected
4. **PASS** — wrong package-index digest rejected
5. **PASS** — package from live mirror rejected
6. **PASS** — package correct name wrong version rejected
7. **PASS** — package correct version wrong digest rejected
8. **PASS** — closure missing package rejected
9. **PASS** — closure extra package rejected
10. **PASS** — closure version mismatch rejected
11. **PASS** — wrong Rust channel-manifest digest rejected
12. **PASS** — wrong Rust component digest rejected
13. **PASS** — ambient host Rust is not accepted as isolated toolchain
14. **PASS** — third-party crate or Cargo registry presence rejected
15. **PASS** — wrong Cloud Hypervisor size rejected
16. **PASS** — wrong Cloud Hypervisor digest rejected
17. **PASS** — wrong Cloud Hypervisor version rejected
18. **PASS** — wrong firmware size rejected
19. **PASS** — wrong firmware digest rejected
20. **PASS** — final asset symlink rejected
21. **PASS** — wrong asset owner rejected
22. **PASS** — wrong asset mode rejected
23. **PASS** — root with ambiguous ownership rejected
24. **PASS** — root escaping through symlink rejected
25. **PASS** — insufficient capacity rejected before mutation
26. **PASS** — reflink failure selects sparse-copy fallback
27. **PASS** — interrupted sparse copy never creates final-name artifact
28. **PASS** — cleanup refuses an unowned path
29. **PASS** — cleanup preserves an unrelated sentinel file
30. **PASS** — remote branch divergence blocks publication
31. **PASS** — non-fast-forward push refused
32. **PASS** — changed implementation-host tuple blocks mission
33. **PASS** — changed kernel or boot policy blocks mission
34. **PASS** — dirty starting worktree blocks mutation
35. **PASS** — changed dependency identity is not silently written into existing tuple

All mutation-oriented cases used disposable copies, simulations, or disposable Git repositories. No authoritative artifact, boot state, or real remote branch was changed.
