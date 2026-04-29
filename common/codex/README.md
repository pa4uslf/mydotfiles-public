# Public Codex Workflow

This directory is a sanitized public subset of a private local Codex setup.

It is intended to show the workflow structure, review gates, prompt routing, and
safe configuration patterns without exposing local trust boundaries, browser
login state, private project paths, or machine-specific automation.

## Included

- Public-safe `AGENTS.md` top-level operating rules.
- `ENGINEERING.md`, `SECURITY.md`, `BROWSER.md`, and `SKILLS.md` workflow docs.
- `config.example.toml` as a template, not a live config.
- Public-safe automation, contract-first, harness, and security review docs.
- Lightweight agent role configs under `.codex/agents/`.
- Reusable prompt files under `.codex/prompts/`.
- Helper scripts that do not encode private paths or credentials.

## Excluded

- Live `config.toml`.
- MCP wrapper scripts with local install paths.
- Trusted project path tables.
- Real browser adapter state, profile/cookie sync details, and account-specific
  workflow rules.
- Personal strategy docs and machine-specific routing documents.
- Memory policy, founder coaching, and marketing routing are intentionally not
  exported by default.

## Install Sketch

```bash
mkdir -p ~/.codex
cp common/codex/.codex/config.example.toml ~/.codex/config.toml
```

Review the config before using it. The example intentionally omits local model
proxies, trusted project paths, and machine-specific MCP commands.
