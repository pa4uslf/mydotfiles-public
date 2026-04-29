# RTK - Rust Token Killer (Codex CLI)

**Usage**: Token-optimized CLI proxy for shell commands.

## Rule

Always prefix shell commands with `rtk`.

Examples:

```bash
rtk git status
rtk cargo test
rtk npm run build
rtk pytest -q
```

## Meta Commands

```bash
rtk gain            # Token savings analytics
rtk gain --history  # Recent command savings history
rtk proxy <cmd>     # Run raw command without filtering
```

## Verification

```bash
rtk --version
rtk gain
which rtk
```

## Notes

- In sandboxed Codex tool runs, `rtk gain` may fail to open its SQLite history database. If that happens, run it in a normal terminal or an unsandboxed shell.
- When filtered output seems incomplete, fall back to `rtk proxy <cmd>` or the raw command.
