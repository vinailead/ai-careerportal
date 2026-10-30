# Agentic Coding Instructions (`AGENTS.md`)

This repository follows **GitHub Agentic Coding** standards so autonomous coding agents (GitHub Copilot Coding Agent, Google Antigravity, Claude Code) can safely navigate, extend, and verify this project.

## 1. Core Domain Invariants (MUST NEVER BE VIOLATED)

1. **100% Grounded-Truth CV Tailoring (`backend/cv_data.py`)**:
   - Never fabricate employers, titles, dates, degrees, certifications, or quantitative metrics.
   - All tailored CVs must strictly preserve the verified metrics from the reference CV (`13+ years`, `3.5 Yrs in Telecom`, `10 Yrs in Financial Services (CaaS)`, `$54.8M` cost-to-serve savings, `2.8M` annual call deflections, `100+` Agentic AI use cases projecting `$400M` ROI, pod of `10 Senior Consultants`, `70%` delivery reduction from `15 days to 5 days`, `$5B +` consumer credit portfolio, `15+ KPIs`, `40%` marketing ROI visibility gain).
2. **Zero-Employment-Gap ATS Structure**:
   - `Independent AI Product Development (Jan 2026- Present)` MUST be placed inside `PROFESSIONAL WORK EXPERIENCE` as the top chronological entry (above `VERIZON | Chennai` and `CCLYTICX SERVICES PVT LTD | Chennai`) so enterprise ATS parsers credit continuous employment.
3. **Strict Seniority & Location Filtering (`backend/jobs_engine.py`, `backend/app.py`)**:
   - **Exclude Director & VP Roles**: Any role with `Director`, `VP`, or `Vice President` in the title must be rejected by both discovery and custom JD tailoring.
   - **Location Allowlist**: Only roles in **Chennai**, **Bengaluru / Bangalore**, **Hyderabad**, or **Global Remote (Worldwide / India-eligible)** are permitted. Exclude geo-restricted remote roles outside India (e.g., "Remote - US Only").
4. **1:1 Visual & Typography Fidelity (`backend/cv_renderer.py`)**:
   - Every generated PDF (`render_cv_pdf`) and Google Doc `.docx` (`render_cv_docx`) must maintain the exact 2-page layout, `Calibri` / `Calibri-Bold` typography, centered contact header with clickable links, full-width `0.71pt` horizontal section dividers, and right-aligned role/education dates.

## 2. Browser Support & Frontend Policy (`frontend/index.html`)

- **Design System**: Google Material Design 3 (M3) split-pane layout.
- **Browser Support**: Allow Baseline Newly Available features (`<dialog closedby="any">`, `overscroll-behavior: contain`, CSS Container Queries `container-type: inline-size`), provided lightweight custom fallback code (`<= 20 lines`, zero external JS dependencies) is included for `<dialog closedby>`.
- **Semantic Markup**:
  - Job cards must use `<article class="job-card">` with `container-type: inline-size`.
  - Modals must use native `<dialog>` opened with `.showModal()` without redundant `role="dialog"` or `aria-modal`.

## 3. Development & Verification Commands

```bash
# 1. Create virtual environment & install dependencies
uv venv .venv
uv pip install -r requirements.txt

# 2. Run automated test suite (MUST pass before any commit/PR)
./.venv/bin/pytest -v

# 3. Start the portal server locally
./.venv/bin/uvicorn backend.app:app --host 127.0.0.1 --port 8765
```
