# Sparse Copy Test

Status: **PASS**

- Filesystem: `ext4`
- `cp --reflink=always`: rejected with exit status `1`
- Selected fallback: `cp --reflink=never --sparse=always with .partial then atomic rename`
- Synthetic logical size: `1073741824` bytes
- Source allocated bytes: `268439552`
- Destination allocated bytes: `268435456`
- Content SHA-256: `8109d7e9a9e384d2e23aacb0d502246821dc095229bcf20cf7eb46f577646b12`
- Logical size, content, and exposed hole extents: equal
- Final owner/mode: `root:root` / `0600`
- Interrupted-copy exit status: `137`
- Final name absent after interruption: yes
- Owned partial cleaned: yes
- Unowned cleanup refused: yes
- Unrelated sentinel preserved: yes
- Successful retry: yes
- Guest disk used: no

All synthetic artifacts were removed after evidence capture.
