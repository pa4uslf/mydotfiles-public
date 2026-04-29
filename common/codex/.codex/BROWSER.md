# Browser Automation Safety

Browser automation can cross from ordinary testing into high-trust local access.
Choose the tool and browser profile intentionally.

## Tool Classes

- Headless browser automation is best for reproducible tests.
- Real-browser automation is best for tasks that need existing login state.
- Anti-detect or profile-isolated browsers are environment layers, not generic
  test runners.

## Safety Rules

- Do not mix unrelated accounts in one persistent browser profile.
- Do not upload or sync a full local browser profile unless that is explicitly
  intended.
- Prefer domain-scoped cookie import over whole-profile copying.
- Treat tools that attach to a real Chrome session as high trust.
- Close sessions and clean temporary artifacts after testing.
