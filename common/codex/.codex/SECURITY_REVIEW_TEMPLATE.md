# Security Review Template

Purpose: turn the security workflow into an executable review record.

Use for release reviews, repository security scans, high-risk code changes,
CI/CD checks, supply-chain checks, and skill/plugin repository reviews.

## 1. Scope

- Review date: `YYYY-MM-DD`
- Target: `repo / branch / commit / release tag`
- Review type: `code / pre-release / supply-chain / CI-CD / secrets / compliance gap`
- Included paths and systems:
- Explicitly out of scope:

## 2. Verdict

- Release decision: `pass / conditional pass / block`
- Overall risk: `Critical / High / Medium / Low`
- Blocking issues: `yes / no`
- Summary:

## 3. Capabilities Used

- Skills / sub-agents:
- Policy references:
- CLI tools:
- Checks not run:
- Reason not run:
- Substitute checks:

## 4. Scan Summary

### Static Analysis

- `semgrep`:
- `semgrep p/secrets`:
- `semgrep p/owasp-top-ten`:

### Dependency / Package Vulnerabilities

- `osv-scanner`:
  - Command / scope:
  - Version:
  - Recursive / offline / call analysis:
  - Result summary:
- `npm audit / pnpm audit / yarn audit`:
- `pip-audit`:
- `cargo audit`:
- `grype`:
- `trivy fs`:

### Secrets And History

- `gitleaks`:
- `detect-secrets`:
- Git history secrets check:
- Manual hardcoded secret search:

## 5. Manual Review

- Authentication and authorization:
- Permission boundaries:
- Input validation:
- SQL / NoSQL / command injection:
- SSRF:
- File upload / path traversal:
- Logs / error leakage:
- Rate limiting / abuse resistance:
- Response headers / TLS / CORS:
- Default configuration:

## 6. CI/CD / Supply Chain / Release Path

- Workflows, release scripts, bots, or installers:
- `pull_request_target` / `workflow_run` usage:
- Actions pinned to immutable SHA:
- Mutable downloads inside actions:
- Minimal workflow permissions:
- Environment-scoped secrets:
- OIDC / trusted publishing:
- Long-lived registry tokens or PATs:
- Release cache and cache poisoning risk:
- Protected branches / tags / releases:
- Bot or GitHub App permissions:
- Webhook authentication and input validation:

## 7. Dynamic Verification

- Browser / E2E / mobile automation:
- Environment:
- Allowed flows:
- Rejected flows:
- Remaining risk:

## 8. Findings

### Critical

- Location:
- Risk:
- Fix:

### High

- Location:
- Risk:
- Fix:

### Medium

- Location:
- Risk:
- Fix:

### Low

- Location:
- Risk:
- Fix:

## 9. Compliance Gaps

- Access control:
- Monitoring and alerting:
- Change management:

## 10. Recheck And Release Conditions

- Required fixes:
- Deferrable items:
- Recheck method:
- Owner:
- Planned recheck date: `YYYY-MM-DD`
