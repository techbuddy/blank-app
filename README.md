# SafetyPulse — HSE Inspection & Corrective Action Manager

SafetyPulse is a lightweight commercial MVP for recording workplace safety observations, calculating risk, assigning corrective actions and tracking closure performance.

## Why this product

Many small contractors still manage inspections and corrective actions through spreadsheets and WhatsApp. SafetyPulse offers a simpler path to a structured digital register, dashboard and management reporting without requiring expensive enterprise EHS software.

## Features

- Observation, unsafe-act, unsafe-condition and near-miss reporting
- Automatic 5×5 likelihood × consequence risk scoring
- Low, Medium, High and Critical severity classification
- Corrective-action owner, target date, status and closure evidence
- Automatic overdue identification
- Executive KPI dashboard
- Status, category, owner and weekly trend analytics
- Search, filtering and CSV export
- Demo records included on first launch
- SQLite storage with no external database needed

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy

The app can be deployed using Streamlit Community Cloud by selecting this repository and setting `streamlit_app.py` as the entry point.

For commercial production use, replace local SQLite storage with PostgreSQL and add authentication, backups, file storage and tenant separation.

## Commercial roadmap

- Multi-company SaaS accounts and role-based permissions
- Configurable inspection checklist builder
- Photo evidence, signatures and QR codes
- PDF inspection reports and branded dashboards
- Automated email and WhatsApp escalations
- Mobile offline mode
- Subscription billing and white-label licensing
- AI-assisted observation classification and action recommendations

## Suggested monetisation

- Starter: AED 99–199/month for small companies
- Professional: AED 399–799/month with analytics and automation
- Enterprise: annual white-label licence and implementation fee
- Optional paid setup, checklist migration, training and support

## Technology

Python, Streamlit, SQLite, Pandas and Plotly.

## Licence

Copyright © 2026. All rights reserved. This repository is published for product demonstration. No permission is granted to copy, redistribute, host commercially or create derivative commercial products without written authorisation from the repository owner.
