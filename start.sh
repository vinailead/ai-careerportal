#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "Starting Vinoth Nataraj AI Career Search, Match & ATS CV Studio on http://127.0.0.1:8765 ..."
./.venv/bin/uvicorn backend.app:app --host 127.0.0.1 --port 8765
