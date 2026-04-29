# Security Workflow

## Baseline Checks

Run secrets scanning before publishing:

```bash
gitleaks detect --source . --redact
detect-secrets scan --all-files
```

For dependency scanning, choose tools by ecosystem:

- Node: `npm audit`, `pnpm audit`, or `yarn audit`
- Python: `pip-audit`
- Rust: `cargo audit`
- Mixed repositories and containers: `grype`, `trivy`, and `osv-scanner`

## Local Database Maintenance

- `grype`: update with `grype db update`.
- `trivy`: update with `trivy image --download-db-only`; Java projects may also
  need `--download-java-db-only`.
- `osv-scanner`: offline mode needs `--download-offline-databases`.
- `cargo-audit`: keeps a local RustSec advisory DB unless `--no-fetch` is used.

## Review Focus

- Secrets and credentials in current files and Git history.
- Auth, authorization, and public data exposure.
- CI/CD tokens, release permissions, and branch protections.
- Command execution, path traversal, and shell quoting.
- Browser automation, local profile access, and cookie handling.
