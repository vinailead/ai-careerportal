# Contributing Guidelines

Thank you for contributing to the **AI Career Search, Match & ATS CV Tailoring Portal**!

## Development Workflow

1. Fork and clone the repository.
2. Create a Python 3.10+ virtual environment and install dependencies:
   ```bash
   uv venv .venv
   uv pip install -r requirements.txt
   ```
3. Review [`AGENTS.md`](./AGENTS.md) before modifying CV tailoring, job scoring, or document rendering logic.
4. Run the test suite and ensure 100% pass rate:
   ```bash
   ./.venv/bin/pytest -v
   ```
5. Open a Pull Request completing the checklist in `.github/PULL_REQUEST_TEMPLATE.md`.
