# Exact-text edit plan

The plan is a JSON array. Paths are relative to `--root`; duplicate paths are rejected.
Use a real `hashlib.sha256(path.read_bytes()).hexdigest()` value for `sha256`.

```json
[
  {
    "path": "src/config.py",
    "sha256": "<64-character SHA-256 of the original bytes>",
    "old": "TIMEOUT = 10",
    "new": "TIMEOUT = 30",
    "count": 1
  }
]
```

`count` is a positive exact integer. Empty search strings, no-op edits, absolute
paths, parent traversal, symlinks, NUL bytes and invalid UTF-8 are rejected.
UTF-8 bytes and CRLF line endings are preserved unless the replacement changes them.
All entries are checked before writes begin. Preview is the default. Apply replaces
files atomically one at a time, not as an atomic batch. The tool rechecks content
before each write, but cannot guarantee safety against hostile concurrent writers.
Stop other writers and use a dedicated worktree. Recover a partial batch by inspecting
`git diff` and constructing a new plan; never blindly replay a stale plan.
