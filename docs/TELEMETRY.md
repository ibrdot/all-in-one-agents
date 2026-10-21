# Telemetry

**This project collects nothing.**

The bootstrap, hooks, and installer make **zero network calls** beyond the
`git clone` / `git pull` you run yourself. There is no analytics, no ping,
no phone-home, no error reporting.

## Opt-out variable

For forward compatibility, the environment variable below is reserved:

```bash
export ALL_IN_ONE_AGENTS_DISABLE_TELEMETRY=1
```

If any future version ever adds an opt-in diagnostic, this variable disables
it completely. Today it is a no-op — because there is nothing to disable.
