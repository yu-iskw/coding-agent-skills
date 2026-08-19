# Recipe: Pull request risk and review

## Flow

`change-risk-assessment` → `test-gap-analysis` → `security-review` when trust boundaries or sensitive capabilities changed → `pull-request-review` → `release-readiness` when the PR is a release candidate

## Gates

1. Classify blast radius before deciding review depth.
2. Use test-gap analysis to target missing validation around the actual changed behavior.
3. Invoke security review only when the change affects authentication, authorization, secrets, untrusted input, command/process execution, network boundaries, dependencies, or similarly sensitive surfaces.
4. Keep the final PR review independent from the implementation rationale.
5. If the change ships directly, include rollback, migration, packaging, and documentation readiness in the final decision.
