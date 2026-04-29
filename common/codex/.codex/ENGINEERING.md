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

## Documentation

- Update docs when commands, config, public behavior, or workflow entry points
  change.
- Do not duplicate long guidance across many files; keep a clear source of
  truth and link to it.
