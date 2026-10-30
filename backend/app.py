"""
FastAPI Backend for Vinoth Nataraj's AI Career Search, Match & CV Tailoring Portal.
Serves:
  - GET  /api/health : Health check & version status
  - GET  /api/jobs : Curated & verified jobs across Chennai, Bengaluru, Hyderabad, and Global Remote
  - GET  /api/jobs/live-search : Polite, rate-limited real-time job discovery (excludes Director roles)
  - POST /api/jobs/custom-tailor : Instant ATS scoring & 1:1 CV tailoring for any pasted Job Description
  - GET  /api/master-variations : All 6 Master CV Variations
  - GET  /api/cv/job/{job_id}/{fmt} : Exact-format PDF or Google Doc (.docx) for a specific job
  - GET  /api/cv/master/{variation_id}/{fmt} : Master variation PDF or Google Doc (.docx)
  - POST /api/tracker : Persistent application status & notes tracker
"""

import json
import os
import re
import time
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.cv_data import MASTER_VARIATIONS, get_master_cv, tailor_cv_for_job
from backend.cv_renderer import render_cv_pdf, render_cv_docx
from backend.jobs_engine import (
    get_all_enriched_jobs,
    discover_live_jobs,
    score_job_against_profile,
    VINOTH_SKILLS_TAXONOMY,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "frontend")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_cvs")
DOWNLOADS_CV_DIR = os.environ.get(
    "TAILORED_CVS_DIR",
    "/Users/vinoth/Downloads/Tailored_CVs" if os.path.exists("/Users/vinoth/Downloads") else OUTPUT_DIR,
)
TRACKER_PATH = os.path.join(BASE_DIR, "backend", "application_tracker.json")

app = FastAPI(
    title="AI Career Search, Match & Exact-Format ATS CV Tailoring Portal",
    version="1.0.0",
    description="Google Material Design 3 Job Discovery, Deterministic ATS Match Scoring, and 1:1 Grounded-Truth CV Tailoring Engine.",
)

# In-memory store initialized with curated verified jobs + any live/custom jobs
JOBS_STORE: Dict[str, Dict[str, Any]] = {j["id"]: j for j in get_all_enriched_jobs()}


def _load_tracker() -> Dict[str, Dict[str, Any]]:
    if os.path.exists(TRACKER_PATH):
        try:
            with open(TRACKER_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_tracker(data: Dict[str, Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(TRACKER_PATH), exist_ok=True)
    with open(TRACKER_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


class TrackerUpdate(BaseModel):
    job_id: str
    status: str = Field(..., pattern="^(New|Saved|Tailored|Applied|Interviewing)$")
    notes: str = ""


class CustomJobRequest(BaseModel):
    title: str
    company: str
    location_bucket: str = "Chennai"
    work_mode: str = "Hybrid"
    track: str = "AI Strategy"
    url: str = "https://www.linkedin.com/jobs"
    salary_estimate: str = "Competitive Enterprise Package"
    experience_range: str = "12–16 yrs"
    description: str


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "curated_jobs_count": len(JOBS_STORE),
        "master_variations_count": len(MASTER_VARIATIONS),
        "director_roles_excluded": True,
    }


@app.get("/api/jobs")
def list_jobs():
    tracker = _load_tracker()
    items = list(JOBS_STORE.values())
    for item in items:
        t_entry = tracker.get(item["id"], {})
        item["app_status"] = t_entry.get("status", item.get("app_status", "Tailored"))
        item["app_notes"] = t_entry.get("notes", item.get("app_notes", ""))
    items.sort(key=lambda x: x["match_score"], reverse=True)
    return {
        "total": len(items),
        "jobs": items,
        "downloads_folder": DOWNLOADS_CV_DIR,
    }


@app.get("/api/jobs/live-search")
def live_search(
    q: str = Query("Agentic AI Manager", description="Search keywords"),
    location: str = Query("Chennai", description="Chennai | Bengaluru | Hyderabad | Global Remote"),
    track: str = Query("Agentic AI", description="AI Strategy | AI Builder | Analytics | Gen AI Leader | Agentic AI"),
):
    discovered = discover_live_jobs(q, location, track)
    added = 0
    for j in discovered:
        if j["id"] not in JOBS_STORE:
            JOBS_STORE[j["id"]] = j
            added += 1
    return {
        "discovered_count": len(discovered),
        "newly_added": added,
        "jobs": discovered,
    }


@app.post("/api/jobs/custom-tailor")
def custom_tailor_job(payload: CustomJobRequest):
    if re.search(r"\b(director|vp|vice president)\b", payload.title, re.I):
        raise HTTPException(
            status_code=400,
            detail="Director and VP roles are excluded by your search policy. Please provide a Senior Manager, Principal, Lead, or Manager role.",
        )

    # Extract grounded keywords present in description
    jd_lower = f"{payload.title} {payload.description}".lower()
    extracted_kws: List[str] = []
    for kw_list in VINOTH_SKILLS_TAXONOMY.values():
        for kw in kw_list:
            if kw.lower() in jd_lower and kw not in extracted_kws:
                extracted_kws.append(kw)
    if not extracted_kws:
        extracted_kws = VINOTH_SKILLS_TAXONOMY.get(payload.track, VINOTH_SKILLS_TAXONOMY["AI Strategy"])[:8]

    jid = f"custom_{int(time.time() * 1000) % 10000000}"
    job_obj: Dict[str, Any] = {
        "id": jid,
        "title": payload.title.strip(),
        "company": payload.company.strip(),
        "location_bucket": payload.location_bucket,
        "raw_location": f"{payload.location_bucket}, India" if payload.location_bucket != "Global Remote" else "Global Remote (Worldwide)",
        "work_mode": payload.work_mode,
        "track": payload.track,
        "posted_date": "2026-10-30",
        "salary_estimate": payload.salary_estimate,
        "experience_range": payload.experience_range,
        "url": payload.url.strip() or "https://www.linkedin.com/jobs",
        "apply_portal": "Custom JD Tailored",
        "jd_keywords": extracted_kws,
        "description": payload.description.strip(),
        "why_you_match": (
            f"Custom-tailored against your 13+ years of progressive leadership at Verizon ($54.8M savings, 100+ Agentic AI use cases) "
            f"and CCLYTICX ($5B+ consumer credit portfolio) using the '{payload.track}' archetype."
        ),
        "app_status": "Tailored",
        "app_notes": "",
    }
    match_info = score_job_against_profile(job_obj)
    job_obj["match_score"] = match_info["overall_score"]
    job_obj["match_details"] = match_info
    job_obj["tailored_cv"] = tailor_cv_for_job(job_obj)

    JOBS_STORE[jid] = job_obj
    return {"ok": True, "job": job_obj}


@app.get("/api/master-variations")
def list_master_variations():
    variations = [get_master_cv(vid) for vid in MASTER_VARIATIONS]
    return {"variations": variations, "downloads_folder": f"{DOWNLOADS_CV_DIR}/Master_Variations"}


@app.get("/api/cv/master/{variation_id}/{fmt}")
def download_master_cv(variation_id: str, fmt: str, inline: bool = False):
    if variation_id not in MASTER_VARIATIONS:
        raise HTTPException(status_code=404, detail="Variation not found")
    fmt_l = fmt.lower()
    if fmt_l not in ("pdf", "docx"):
        raise HTTPException(status_code=400, detail="Format must be pdf or docx")

    cv = get_master_cv(variation_id)
    fname = f"Vinoth_Nataraj_Senior_Manager_{variation_id.upper()}.{fmt_l}"
    out_path = os.path.join(DOWNLOADS_CV_DIR, "Master_Variations", fname)
    if not os.path.exists(out_path):
        if fmt_l == "pdf":
            render_cv_pdf(cv, out_path)
        else:
            render_cv_docx(cv, out_path)

    media_type = (
        "application/pdf"
        if fmt_l == "pdf"
        else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    disposition = "inline" if (inline and fmt_l == "pdf") else "attachment"
    return FileResponse(
        out_path,
        media_type=media_type,
        headers={"Content-Disposition": f'{disposition}; filename="{fname}"'},
    )


@app.get("/api/cv/job/{job_id}/{fmt}")
def download_job_cv(job_id: str, fmt: str, inline: bool = False):
    job = JOBS_STORE.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    fmt_l = fmt.lower()
    if fmt_l not in ("pdf", "docx"):
        raise HTTPException(status_code=400, detail="Format must be pdf or docx")

    safe_co = re.sub(r"[^A-Za-z0-9]+", "_", job["company"]).strip("_")[:25]
    safe_tr = re.sub(r"[^A-Za-z0-9]+", "_", job["track"]).strip("_")
    fname = f"Vinoth_Nataraj_{safe_co}_{safe_tr}_{job['id']}.{fmt_l}"
    out_path = os.path.join(DOWNLOADS_CV_DIR, "Job_Specific", fname)

    cv_data = job.get("tailored_cv") or tailor_cv_for_job(job)
    if not os.path.exists(out_path):
        if fmt_l == "pdf":
            render_cv_pdf(cv_data, out_path)
        else:
            render_cv_docx(cv_data, out_path)

    media_type = (
        "application/pdf"
        if fmt_l == "pdf"
        else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    disposition = "inline" if (inline and fmt_l == "pdf") else "attachment"
    return FileResponse(
        out_path,
        media_type=media_type,
        headers={"Content-Disposition": f'{disposition}; filename="{fname}"'},
    )


@app.post("/api/tracker")
def update_tracker(payload: TrackerUpdate):
    tracker = _load_tracker()
    tracker[payload.job_id] = {
        "status": payload.status,
        "notes": payload.notes,
    }
    _save_tracker(tracker)
    if payload.job_id in JOBS_STORE:
        JOBS_STORE[payload.job_id]["app_status"] = payload.status
        JOBS_STORE[payload.job_id]["app_notes"] = payload.notes
    return {"ok": True, "job_id": payload.job_id, "status": payload.status, "notes": payload.notes}


@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()


if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
