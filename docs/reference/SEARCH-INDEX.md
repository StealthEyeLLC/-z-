# -Z- Search Index

Status: **Discovery aid; not normative authority**

## Project aliases

`-Z-`, `Z`, `z`, `StealthEyeLLC/-z-`, SSH-native computer, sovereign Linux computer, lifecycle-aware SSH, SSH over vsock, AF_VSOCK SSH.

## Question-to-document map

| Search question or phrase | Read first |
|---|---|
| What is Z? | `README.md`, `docs/SCOPE.md` |
| What can never be changed casually? | `docs/INVARIANTS.md`, `docs/ANTI-INVARIANTS.md` |
| Why SSH? | `docs/ARCHITECTURE.md`, `docs/research/SSH-RESEARCH-AND-ARCHITECTURE.md` |
| How does SSH reach a machine without an IP? | `docs/ARCHITECTURE.md`, search `AF_VSOCK`, `vsock mux` |
| Why does Z exit after connection? | Search `ProxyUseFdpass`, `descriptor handoff`, `fd passing` |
| How are IDEs supported? | `docs/VARIANTS.md`, search `compatibility profile`, `stdio relay` |
| How is exact argv preserved? | `docs/INVARIANTS.md`, `docs/ARCHITECTURE.md`, search `exact execution` |
| What does Network None mean? | `docs/DECISIONS.md`, `docs/VARIANTS.md`, search `no virtual NIC` |
| How are host keys and identity handled? | `docs/SECURITY.md`, `docs/DECISIONS.md`, search `prebound`, `host key` |
| How are credentials injected? | `docs/ARCHITECTURE.md`, search `SMBIOS`, `system credentials` |
| What is prohibited? | `docs/ANTI-INVARIANTS.md` |
| What limitations are accepted? | `docs/SACRIFICES.md` |
| What should be built first? | `docs/BUILD.md` |
| What proves a release? | `docs/CERTIFICATION.md`, `evidence/README.md` |
| How do I amend architecture? | `docs/CHANGE-CONTROL.md` |
| Is this implemented? | `docs/MANIFEST.md`, `evidence/README.md` |

## High-value keywords

`OpenSSH`, `ProxyCommand`, `ProxyUseFdpass`, `HostKeyAlias`, `KnownHostsCommand`, `AF_VSOCK`, `vsock-mux`, `sshd -i`, `systemd socket activation`, `SMBIOS Type 11`, `ImportCredential`, `exact argv`, `SFTP`, `capability portal`, `Network None`, `passt`, `virtiofsd`, `Cloud Hypervisor`, `Landlock`, `seccomp`, `raw disk`, `reflink`, `cold snapshot`, `fork identity`, `unknown outcome`, `zero processes at rest`.

## Indexing rule

When adding a new architectural term, capability, or variant, update this file and `docs/MANIFEST.md` in the same change.
