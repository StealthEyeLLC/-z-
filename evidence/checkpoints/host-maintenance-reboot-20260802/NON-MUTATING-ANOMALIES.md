# Non-mutating preflight anomalies

1. An unsupported stream-read operation name was attempted once; it performed no mutation. The supported file/stream read path then succeeded.
2. A probe shell defaulted to `/bin/sh` and rejected `pipefail` before executing any probe or creating state.
3. A temporary C probe compilation was rejected by `-Werror=misleading-indentation`; the cleanup trap removed the temporary directory before any primitive ran.
4. A corrected primitive run passed all kernel and host primitives through seccomp, then stopped because the client-only `ProxyUseFdpass` option was checked with `sshd`. Cleanup ran. The option was then checked correctly with `ssh -G`, and independent TAP, loop, transient-unit, and temporary-directory residue counts were all zero.

None of these events changed repository content, packages, boot policy, retained services, networking, implementation roots, guest artifacts, or product state.
