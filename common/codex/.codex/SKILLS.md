# Codex Skills

## Management Model

- Keep repo-managed skills in version control.
- Keep runtime-installed or third-party experimental skills outside the public
  dotfiles export unless they have been reviewed.
- Disable duplicate or noisy skills by config rather than deleting the source
  when reversible rollback matters.

## Intake Checklist

1. Read the skill's `SKILL.md`.
2. Check scripts for shell execution, network calls, browser/profile access, and
   credential handling.
3. Decide whether it belongs in a public repo, a private repo, or local runtime
   only.
4. Add only the minimal routing docs needed for future use.
