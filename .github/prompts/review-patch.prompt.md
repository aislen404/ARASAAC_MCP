# GitHub Copilot Review Prompt Template

Review the patch for:

1. OpenSpec compliance.
2. License compliance.
3. Privacy/no PII.
4. Human review gate.
5. Pictogram IDs real and not generated.
6. Accessibility impact.
7. Security risk.
8. Test coverage.
9. Documentation update.

Return:

```text
status: pass | warn | fail
blocking_issues:
non_blocking_issues:
recommended_fixes:
missing_tests:
```
