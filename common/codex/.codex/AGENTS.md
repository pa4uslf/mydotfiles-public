# AGENTS - Public Codex Instructions

## Operating Principles

- Read the repository before making non-trivial changes.
- Prefer existing project conventions over new abstractions.
- Keep edits scoped to the requested behavior.
- When using external libraries or APIs, verify current official documentation.
- For security-sensitive changes, define trust boundaries, default states, and
  rollback paths before editing.
- Use explicit dates for relative-time records such as "today", "yesterday",
  "this week", or "recent".

## Git Safety

- Check `git status --short --branch` before editing and before committing.
- Do not revert unrelated user changes.
- Stage and commit serially; do not run `git add`, `git commit`, and `git push`
  in parallel.
- Before publishing, run secrets scanning on both current files and Git history.

## Source Of Truth

- Prefer editing managed source files over generated home-directory copies.
- Treat live config files as examples unless the repository explicitly says they
  are source-of-truth.
- Keep long-lived workflow rules in versioned documentation, not in ephemeral
  chat memory.

## Verification

- Match verification depth to risk.
- For public releases, run at least:

```bash
gitleaks detect --source . --redact
detect-secrets scan --all-files
```
