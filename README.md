# SafetyPulse — HSE Inspection & Corrective Action Manager

SafetyPulse is a working commercial MVP for recording workplace safety observations, calculating risk, assigning corrective actions and tracking closure performance.

## Current capabilities

- Observation, unsafe-act, unsafe-condition, near-miss and positive-observation reporting
- Automatic 5×5 likelihood × consequence risk scoring
- Low, Medium, High and Critical severity classification
- Corrective-action owner, target date, status and closure evidence
- Automatic overdue identification
- Executive KPI dashboard and priority queue
- Status, category, owner and weekly trend analytics
- Search, filtering and CSV export
- SQLite storage and first-run demonstration records
- Docker image, Docker Compose and GitHub Actions CI

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open `http://localhost:8501`.

## Run with Docker

```bash
docker compose up --build
```

Open `http://localhost:8501`.

## Streamlit Community Cloud

Create an app from this repository and use `streamlit_app.py` as the entry point. The included requirements file contains all runtime packages.

## Verification

The CI workflow performs the following checks on pushes and pull requests:

1. Installs the Python dependencies.
2. Compiles the application with `py_compile`.
3. Verifies runtime imports.
4. Builds the production Docker image.

## Commercial positioning

SafetyPulse is designed for contractors and small-to-medium companies that still control inspections and CAPA through spreadsheets, email and messaging applications.

Suggested packages:

- Starter: AED 99–199 per month
- Professional: AED 399–799 per month
- Enterprise: annual white-label licence plus implementation
- Services: checklist configuration, data migration, training, branding and support

## Production roadmap

- Authentication and role-based access control
- Multi-company tenant isolation
- PostgreSQL and managed backups
- Configurable inspection checklist builder
- Photo evidence, signatures and QR codes
- PDF inspection reports
- Email and WhatsApp escalation
- Mobile offline mode
- Subscription billing
- AI-assisted classification, JSA and corrective-action recommendations

## Important limitation

This release is a functional commercial MVP, not yet a fully hardened enterprise SaaS platform. Before storing confidential, personal or regulated information, implement the controls listed in `SECURITY.md`.

## Technology

Python, Streamlit, SQLite, Pandas, Plotly, Docker and GitHub Actions.

## Licence

Copyright © 2026. All rights reserved. This repository is published for product demonstration. No permission is granted to copy, redistribute, commercially host or create derivative commercial products without written authorisation from the repository owner.
