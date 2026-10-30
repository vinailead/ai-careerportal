# GitHub Copilot Agentic Coding Instructions

Please read and strictly adhere to the architectural invariants, grounded-truth rules, and verification commands documented in [`AGENTS.md`](../AGENTS.md).

## Key Rules Summary
- **Grounded Truth Only**: Never invent metrics, skills, or employers in `backend/cv_data.py`.
- **No Director Roles**: Enforce the regex exclusion `\b(director|vp|vice president)\b` across all job ingestion and custom tailoring endpoints (`backend/jobs_engine.py`, `backend/app.py`).
- **Locations**: Only `Chennai`, `Bengaluru`, `Hyderabad`, and unrestricted `Global Remote`.
- **Testing**: Run `pytest -v` before opening or updating any Pull Request.
