#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=========================================="
echo "  SafetyPulse - macOS/Linux Local Launcher"
echo "=========================================="

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "Python 3.10 or newer is required."
  exit 1
fi

if [ ! -x ".venv/bin/python" ]; then
  echo "Creating local virtual environment..."
  "$PYTHON" -m venv .venv
fi

.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

echo "Starting SafetyPulse at http://localhost:8501"
if command -v open >/dev/null 2>&1; then
  open http://localhost:8501 >/dev/null 2>&1 || true
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open http://localhost:8501 >/dev/null 2>&1 || true
fi

exec .venv/bin/python -m streamlit run streamlit_app.py --server.address localhost --server.port 8501
