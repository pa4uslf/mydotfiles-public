# Engineering Workflow

## Default Loop

1. Inspect the real files and commands.
2. Identify the smallest coherent change.
3. Edit only the necessary files.
4. Run targeted verification.
5. Report what changed, what was verified, and what remains risky.

## Debugging

- Do root-cause analysis before applying fixes.
- Preserve the failing evidence until the fix is verified.
- Prefer one hypothesis and one verification step at a time.

## Implementation

- Keep behavior changes explicit.
- Avoid broad refactors unless they are required for the task.
- Add tests when the change affects public behavior, shared contracts, or
  regression-prone logic.

## Verification Levels

- L0: Use a short self-check; state the real evidence, scope, and anything not
  verified.
- L1: Run the targeted test, lint, type check, or smoke check that matches the
  changed area.
- L2: Run the project-level `verify` entry point or the closest complete
  validation command.
- L3: Run `verify` plus findings-first review; add security scans or human
  review for auth, data, migration, release, payment, secrets, or external-input
  paths.

If a project has no unified validation entry point, say so explicitly. Do not
describe unverified work as verified. Mature projects should expose
`scripts/verify.*`, `npm run verify`, or an equivalent command and call it from
CI or release gates according to risk.

## Testing Entry Points

Do not duplicate a separate long `TEST.md` by default. Route testing work to the
existing source of truth:

- Before implementation: use the TDD workflow.
- After implementation when coverage is missing: add the smallest test layer
  that closes the real evidence gap.
- During iteration: run a scoped quality gate.
- Before delivery: run the full verification gate.
- During review: check whether the verification evidence covers the changed
  behavior.
- For security, auth, payments, data, secrets, external input, or release paths:
  follow the security policy.

Project-specific test commands belong in that project's README, package scripts,
`scripts/verify.*`, CI config, or short AGENTS entry.

## Documentation

- Update docs when commands, config, public behavior, or workflow entry points
  change.
- Do not duplicate long guidance across many files; keep a clear source of
  truth and link to it.
