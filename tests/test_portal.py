"""
Pytest verification suite for:
  1. Grounded-Truth CV Ledger & Zero-Gap Chronology
  2. Strict Exclusion of Director / VP Roles & Location Allowlist
  3. 5-Factor Deterministic ATS Match Scoring
  4. 1:1 2-Page PDF & Google Docs (.docx) Document Rendering
  5. FastAPI REST Endpoints & Custom JD Tailoring
"""

import os
import re
import pymupdf
import docx
from fastapi.testclient import TestClient

from backend.app import app
from backend.cv_data import MASTER_VARIATIONS, get_master_cv, tailor_cv_for_job
from backend.cv_renderer import render_cv_pdf, render_cv_docx
from backend.jobs_engine import get_all_enriched_jobs

client = TestClient(app)


def test_grounded_truth_and_zero_gap_chronology():
    """Verifies Independent AI Product Development is inside PROFESSIONAL WORK EXPERIENCE and facts are preserved."""
    for vid in MASTER_VARIATIONS:
        cv = get_master_cv(vid)
        assert cv["header"]["name"] == "Vinoth Nataraj"
        assert cv["experience"][0]["company"] == "Independent AI Product Development"
        assert cv["experience"][0]["dates"] == "Jan 2026- Present"
        assert cv["experience"][1]["company"] == "VERIZON | Chennai"
        assert cv["experience"][2]["company"] == "CCLYTICX SERVICES PVT LTD | Chennai"
        verizon_blob = " ".join(cv["experience"][1]["bullets"])
        assert "$54.8M" in verizon_blob
        assert "2.8M" in verizon_blob
        assert "100+" in verizon_blob
        assert "$400M" in verizon_blob


def test_curated_jobs_no_director_and_valid_locations():
    """Verifies zero Director/VP roles exist and only allowed locations & tracks are present."""
    jobs = get_all_enriched_jobs()
    assert len(jobs) >= 25
    allowed_locs = {"Chennai", "Bengaluru", "Hyderabad", "Global Remote"}
    allowed_tracks = {"AI Strategy", "AI Builder", "Analytics", "Gen AI Leader", "Agentic AI"}

    for job in jobs:
        assert not re.search(r"\b(director|vp|vice president)\b", job["title"], re.I), (
            f"Forbidden title found: {job['title']}"
        )
        assert job["location_bucket"] in allowed_locs
        assert job["track"] in allowed_tracks
        assert 75 <= job["match_score"] <= 99
        assert job["url"].startswith("https://")


def test_pdf_and_docx_rendering_two_pages(tmp_path):
    """Verifies rendered PDF is exactly 2 pages with clickable links and DOCX renders cleanly."""
    cv = get_master_cv("ai_strategy")
    pdf_file = str(tmp_path / "test_cv.pdf")
    docx_file = str(tmp_path / "test_cv.docx")

    render_cv_pdf(cv, pdf_file)
    render_cv_docx(cv, docx_file)

    assert os.path.exists(pdf_file)
    assert os.path.exists(docx_file)

    pdf_doc = pymupdf.open(pdf_file)
    assert len(pdf_doc) == 2, "Rendered PDF must match the exact 2-page layout"
    page1_text = pdf_doc[0].get_text()
    page2_text = pdf_doc[1].get_text()
    assert "Vinoth Nataraj" in page1_text
    assert "PROFESSIONAL WORK EXPERIENCE" in page1_text
    assert "Independent AI Product Development" in page1_text
    assert "VERIZON | Chennai" in page1_text
    assert "CCLYTICX SERVICES PVT LTD | Chennai" in page2_text
    assert "EDUCATION" in page2_text
    assert len(pdf_doc[0].get_links()) >= 3

    word_doc = docx.Document(docx_file)
    full_docx_text = "\n".join(p.text for p in word_doc.paragraphs)
    assert "Vinoth Nataraj" in full_docx_text
    assert "Independent AI Product Development" in full_docx_text
    assert "The University of Sheffield, United Kingdom" in full_docx_text


def test_api_endpoints_and_custom_jd_tailor():
    """Verifies FastAPI endpoints and ensures custom-tailor rejects Director titles and accepts valid JDs."""
    r_health = client.get("/api/health")
    assert r_health.status_code == 200
    assert r_health.json()["director_roles_excluded"] is True

    # Director role must be rejected with 400
    r_bad = client.post(
        "/api/jobs/custom-tailor",
        json={
            "title": "Director of AI Strategy",
            "company": "Example Corp",
            "location_bucket": "Chennai",
            "track": "AI Strategy",
            "description": "Leading AI Strategy.",
        },
    )
    assert r_bad.status_code == 400

    # Senior Manager role must succeed and produce tailored CV
    r_good = client.post(
        "/api/jobs/custom-tailor",
        json={
            "title": "Senior Manager – Agentic AI & CX Transformation",
            "company": "Global FinTech Hub",
            "location_bucket": "Chennai",
            "track": "Agentic AI",
            "url": "https://www.linkedin.com/jobs",
            "description": "Build LangGraph multi-agent workflows, Gemini RAG pipelines, and reduce cost-to-serve across credit portfolios.",
        },
    )
    assert r_good.status_code == 200
    new_job = r_good.json()["job"]
    assert new_job["match_score"] >= 85
    assert "LangGraph" in new_job["jd_keywords"]
