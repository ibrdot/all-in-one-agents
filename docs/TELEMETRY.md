# Telemetry

## ⏱️ 30-second TL;DR

**This project collects nothing.**

The bootstrap, hooks, and installer make **zero network calls** beyond the
`git clone` / `git pull` you run yourself. There is no analytics, no ping,
no phone-home, no error reporting.

> **Today**: the opt-out variable below is a no-op — because there is nothing
> to disable. It is reserved for forward compatibility only, in case any
> future version ever adds an opt-in diagnostic.

---

## Opt-out variable

For forward compatibility, the environment variable below is reserved:

```bash
export ALL_IN_ONE_AGENTS_DISABLE_TELEMETRY=1
```

If any future version ever adds an opt-in diagnostic, this variable disables
it completely. Today it is a no-op — because there is nothing to disable.

---

## Next

- [Installation by harness](INSTALL.md) — installer behavior (no network calls)
- [Runtime](RUNTIME.md) — when network IS used (explicit provider calls only)
- [Security policy](../SECURITY.md) — report sensitive issues privately
- [Compatibility evidence](COMPATIBILITY-EVIDENCE.md) — what is tested vs claimed
