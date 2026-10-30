## Summary of Changes

- 

## Verification & Invariants Checklist

- [ ] **Grounded Truth Preserved**: No fabricated employers, metrics, or skills added to `backend/cv_data.py`.
- [ ] **Zero-Director Policy**: `Director` and `VP` roles remain strictly excluded.
- [ ] **Location Filter**: Only `Chennai`, `Bengaluru`, `Hyderabad`, and `Global Remote` roles are included.
- [ ] **1:1 Document Fidelity**: Both `.pdf` and `.docx` exports render cleanly across 2 pages.
- [ ] **Tests Passing**: `pytest -v` passes with 0 failures.
