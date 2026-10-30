# Security & Responsible Use Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## GitHub Terms of Service & Acceptable Use Compliance

This repository is designed in strict compliance with the [GitHub Acceptable Use Policies](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies) and [GitHub Terms of Service](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service):

1. **Zero Secret / Credential Storage**: API keys, tokens, and `.env` files are excluded via `.gitignore` and must never be committed.
2. **User-Initiated & Polite Discovery**: Live job discovery is strictly user-initiated, rate-limited, and read-only, with full support for user-pasted Job Descriptions (`POST /api/jobs/custom-tailor`).
3. **Personal Data Protection**: Generated binary resume files (`output_cvs/`) and local application tracking state (`backend/application_tracker.json`) are git-ignored by default.

## Reporting a Vulnerability

If you discover a security issue or unintended PII exposure, please open a private security advisory on GitHub or contact the maintainer directly.
