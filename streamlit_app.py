import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

APP_NAME = "SafetyPulse"
DB_PATH = Path("safetypulse.db")

st.set_page_config(page_title=f"{APP_NAME} | HSE Action Manager", page_icon="🛡️", layout="wide")


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reported_at TEXT NOT NULL,
                project TEXT NOT NULL,
                location TEXT NOT NULL,
                category TEXT NOT NULL,
                observation_type TEXT NOT NULL,
                description TEXT NOT NULL,
                likelihood INTEGER NOT NULL,
                consequence INTEGER NOT NULL,
                risk_score INTEGER NOT NULL,
                severity TEXT NOT NULL,
                action_required TEXT NOT NULL,
                owner TEXT NOT NULL,
                target_date TEXT NOT NULL,
                status TEXT NOT NULL,
                closed_at TEXT,
                evidence TEXT,
                created_by TEXT NOT NULL
            )
            """
        )
        count = conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0]
        if count == 0:
            seed_demo(conn)


def severity_from_score(score):
    if score >= 17:
        return "Critical"
    if score >= 10:
        return "High"
    if score >= 5:
        return "Medium"
    return "Low"


def seed_demo(conn):
    today = date.today()
    samples = [
        (-10, "Solar Restoration", "Phase C - Block 10", "Welfare", "Unsafe Condition", "Drinking-water point had no replenishment record.", 3, 3, "Provide filled dispensers and introduce twice-daily checks.", "Welfare Supervisor", 2, "Closed", "Photo and checklist uploaded", "Demo User"),
        (-8, "Solar Restoration", "Phase B - Block 37", "Plant & Equipment", "Unsafe Condition", "Forklift reverse alarm was not functioning during inspection.", 4, 4, "Isolate equipment, repair alarm and verify before release.", "Plant Manager", 0, "Closed", "Repair work order attached", "Demo User"),
        (-6, "Solar Restoration", "Main Laydown", "Housekeeping", "Unsafe Condition", "Loose packaging and timber obstructed the pedestrian route.", 3, 2, "Clear route and mark material storage zones.", "Area Supervisor", 1, "Closed", "Closure photograph", "Demo User"),
        (-4, "Solar Restoration", "Phase C - Block 28", "Electrical", "Unsafe Act", "Temporary extension lead crossed a wet access route without protection.", 4, 5, "Stop use, install protected routing and inspect all temporary supplies.", "Electrical Manager", 1, "Open", "", "Demo User"),
        (-3, "Solar Restoration", "Workshop", "Fire Safety", "Unsafe Condition", "Combustible waste accumulated near the welding bay.", 3, 4, "Remove waste and maintain a five-metre clear zone.", "Workshop Supervisor", -1, "Overdue", "", "Demo User"),
        (-2, "Solar Restoration", "Phase A - Block 12", "Work at Height", "Near Miss", "A loose hand tool fell within the barricaded drop zone; no injury occurred.", 4, 4, "Introduce tool tethering and repeat dropped-object briefing.", "Construction Manager", 2, "In Progress", "", "Demo User"),
        (-1, "Solar Restoration", "Gate 2", "Traffic Management", "Positive Observation", "Banksman maintained safe separation during reversing activity.", 1, 1, "Recognise the team and share the good practice.", "Logistics Manager", 5, "Closed", "Recognition note", "Demo User"),
        (0, "Solar Restoration", "Phase C - Block 31", "Heat Stress", "Unsafe Condition", "Crew thermos provision was below the site ratio.", 4, 4, "Provide one thermos per 15 workers before permit validation.", "Subcontractor PM", 1, "Open", "", "Demo User"),
    ]
    for offset, project, location, category, obs_type, desc, likelihood, consequence, action, owner, due_offset, status, evidence, creator in samples:
        reported = today + timedelta(days=offset)
        target = today + timedelta(days=due_offset)
        score = likelihood * consequence
        closed_at = str(reported + timedelta(days=1)) if status == "Closed" else None
        conn.execute(
            """INSERT INTO observations
            (reported_at, project, location, category, observation_type, description,
             likelihood, consequence, risk_score, severity, action_required, owner,
             target_date, status, closed_at, evidence, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (str(reported), project, location, category, obs_type, desc, likelihood,
             consequence, score, severity_from_score(score), action, owner, str(target),
             status, closed_at, evidence, creator),
        )


def load_data():
    with get_conn() as conn:
        return pd.read_sql_query("SELECT * FROM observations ORDER BY id DESC", conn)


def add_observation(values):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO observations
            (reported_at, project, location, category, observation_type, description,
             likelihood, consequence, risk_score, severity, action_required, owner,
             target_date, status, closed_at, evidence, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            values,
        )


def update_action(record_id, status, evidence):
    closed_at = str(date.today()) if status == "Closed" else None
    with get_conn() as conn:
        conn.execute(
            "UPDATE observations SET status=?, evidence=?, closed_at=? WHERE id=?",
            (status, evidence, closed_at, int(record_id)),
        )


def apply_overdue(df):
    if df.empty:
        return df
    today = pd.Timestamp(date.today())
    due = pd.to_datetime(df["target_date"], errors="coerce")
    mask = (~df["status"].eq("Closed")) & (due < today)
    df.loc[mask, "status"] = "Overdue"
    return df


init_db()

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.3rem; padding-bottom: 2rem;}
    [data-testid="stMetric"] {background: rgba(127,127,127,.08); border: 1px solid rgba(127,127,127,.18); padding: 14px; border-radius: 14px;}
    .hero {padding: 22px 24px; border-radius: 18px; background: linear-gradient(120deg,#102a43,#1f7a8c); color:white; margin-bottom:18px;}
    .hero h1 {margin:0; font-size:2.2rem;}
    .hero p {margin:.45rem 0 0; opacity:.9;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="hero"><h1>🛡️ {APP_NAME}</h1><p>Inspection, risk and corrective-action management for safer projects.</p></div>',
    unsafe_allow_html=True,
)

page = st.sidebar.radio("Workspace", ["Executive Dashboard", "Report Observation", "Action Register", "Analytics", "About Product"])
st.sidebar.caption("Commercial MVP • Local SQLite storage • CSV export")

df = apply_overdue(load_data())

if page == "Executive Dashboard":
    total = len(df)
    open_count = int((df["status"] != "Closed").sum()) if total else 0
    overdue = int((df["status"] == "Overdue").sum()) if total else 0
    critical_high = int(df["severity"].isin(["Critical", "High"]).sum()) if total else 0
    closed = int((df["status"] == "Closed").sum()) if total else 0
    closure_rate = (closed / total * 100) if total else 0

    cols = st.columns(5)
    cols[0].metric("Total Observations", total)
    cols[1].metric("Open Actions", open_count)
    cols[2].metric("Overdue", overdue)
    cols[3].metric("High / Critical", critical_high)
    cols[4].metric("Closure Rate", f"{closure_rate:.0f}%")

    left, right = st.columns(2)
    with left:
        st.subheader("Actions by status")
        status_data = df.groupby("status").size().reset_index(name="count")
        st.plotly_chart(px.pie(status_data, names="status", values="count", hole=.55), use_container_width=True)
    with right:
        st.subheader("Risk by category")
        risk_data = df.groupby("category", as_index=False)["risk_score"].mean().sort_values("risk_score", ascending=False)
        st.plotly_chart(px.bar(risk_data, x="risk_score", y="category", orientation="h", labels={"risk_score":"Average risk", "category":""}), use_container_width=True)

    st.subheader("Priority action queue")
    priority = df[df["status"] != "Closed"].sort_values(["risk_score", "target_date"], ascending=[False, True])
    st.dataframe(priority[["id", "severity", "category", "location", "owner", "target_date", "status", "action_required"]], use_container_width=True, hide_index=True)

elif page == "Report Observation":
    st.subheader("Create a safety observation")
    with st.form("new_observation", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        reported_at = c1.date_input("Date reported", date.today())
        project = c2.text_input("Project", "Solar Restoration")
        location = c3.text_input("Location / block")
        c4, c5 = st.columns(2)
        category = c4.selectbox("Category", ["Work at Height", "Electrical", "Plant & Equipment", "Traffic Management", "Lifting", "Excavation", "Fire Safety", "Heat Stress", "Welfare", "Housekeeping", "Environmental", "Other"])
        obs_type = c5.selectbox("Observation type", ["Unsafe Condition", "Unsafe Act", "Near Miss", "Positive Observation"])
        description = st.text_area("Observation description", height=110)
        c6, c7, c8 = st.columns(3)
        likelihood = c6.slider("Likelihood", 1, 5, 3)
        consequence = c7.slider("Consequence", 1, 5, 3)
        score = likelihood * consequence
        severity = severity_from_score(score)
        c8.metric("Calculated risk", f"{score} — {severity}")
        action = st.text_area("Corrective / preventive action", height=90)
        c9, c10, c11 = st.columns(3)
        owner = c9.text_input("Action owner")
        target = c10.date_input("Target date", date.today() + timedelta(days=3))
        creator = c11.text_input("Reported by", "HSE Team")
        submitted = st.form_submit_button("Save observation", type="primary", use_container_width=True)
        if submitted:
            required = [project, location, description, action, owner, creator]
            if not all(x.strip() for x in required):
                st.error("Complete all required text fields.")
            else:
                add_observation((str(reported_at), project.strip(), location.strip(), category, obs_type,
                                 description.strip(), likelihood, consequence, score, severity,
                                 action.strip(), owner.strip(), str(target), "Open", None, "", creator.strip()))
                st.success("Observation saved and added to the action register.")
                st.rerun()

elif page == "Action Register":
    st.subheader("Corrective action register")
    f1, f2, f3 = st.columns(3)
    status_filter = f1.multiselect("Status", sorted(df["status"].unique()), default=sorted(df["status"].unique()))
    severity_filter = f2.multiselect("Severity", ["Low", "Medium", "High", "Critical"], default=["Low", "Medium", "High", "Critical"])
    search = f3.text_input("Search")
    view = df[df["status"].isin(status_filter) & df["severity"].isin(severity_filter)].copy()
    if search:
        text = view.astype(str).agg(" ".join, axis=1)
        view = view[text.str.contains(search, case=False, na=False)]
    st.dataframe(view[["id", "reported_at", "project", "location", "category", "description", "severity", "risk_score", "owner", "target_date", "status"]], use_container_width=True, hide_index=True)
    st.download_button("Download filtered register (CSV)", view.to_csv(index=False).encode("utf-8"), "safetypulse_action_register.csv", "text/csv")

    st.divider()
    st.subheader("Update an action")
    open_df = df[df["status"] != "Closed"]
    if open_df.empty:
        st.success("No open actions.")
    else:
        options = {f"#{r.id} | {r.category} | {r.location}": r.id for r in open_df.itertuples()}
        selected = st.selectbox("Select action", options.keys())
        record_id = options[selected]
        row = open_df[open_df["id"] == record_id].iloc[0]
        st.info(row["action_required"])
        with st.form("update_action"):
            new_status = st.selectbox("New status", ["Open", "In Progress", "Closed"], index=1)
            evidence = st.text_area("Closure evidence / remarks", value=row.get("evidence", "") or "")
            if st.form_submit_button("Update action", type="primary"):
                if new_status == "Closed" and not evidence.strip():
                    st.error("Closure evidence is required before closing an action.")
                else:
                    update_action(record_id, new_status, evidence.strip())
                    st.success("Action updated.")
                    st.rerun()

elif page == "Analytics":
    st.subheader("Trend and performance analytics")
    chart_df = df.copy()
    chart_df["reported_at"] = pd.to_datetime(chart_df["reported_at"])
    chart_df["week"] = chart_df["reported_at"].dt.to_period("W").astype(str)
    weekly = chart_df.groupby(["week", "observation_type"]).size().reset_index(name="count")
    st.plotly_chart(px.line(weekly, x="week", y="count", color="observation_type", markers=True, labels={"week":"Week", "count":"Observations"}), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        owner_data = df[df["status"] != "Closed"].groupby("owner").size().reset_index(name="open_actions").sort_values("open_actions", ascending=False)
        st.plotly_chart(px.bar(owner_data, x="owner", y="open_actions", title="Open actions by owner"), use_container_width=True)
    with c2:
        severity_data = df.groupby("severity").size().reindex(["Low", "Medium", "High", "Critical"], fill_value=0).reset_index(name="count")
        st.plotly_chart(px.bar(severity_data, x="severity", y="count", title="Risk distribution"), use_container_width=True)

    closed_df = df[df["status"] == "Closed"].copy()
    if not closed_df.empty:
        closed_df["reported_at"] = pd.to_datetime(closed_df["reported_at"])
        closed_df["closed_at"] = pd.to_datetime(closed_df["closed_at"])
        closed_df["days_to_close"] = (closed_df["closed_at"] - closed_df["reported_at"]).dt.days.clip(lower=0)
        st.metric("Average action closure time", f"{closed_df['days_to_close'].mean():.1f} days")

else:
    st.subheader("A product designed to be sold")
    st.markdown(
        """
        **SafetyPulse** is a lightweight, deployable HSE inspection and corrective-action platform for contractors, facilities, warehouses and construction projects.

        **Current MVP capabilities**
        - Safety observation and near-miss reporting
        - Automatic 5×5 risk scoring and severity classification
        - Corrective-action ownership, due dates and closure evidence
        - Overdue action visibility and executive KPI dashboard
        - Category, owner and trend analytics
        - CSV exports for management reporting
        - Local SQLite database with no external service dependency

        **Commercial expansion path**
        1. Multi-company accounts and role-based access
        2. Photo uploads, signatures and QR-code inspections
        3. Configurable checklists and PDF report generation
        4. Email/WhatsApp reminders and escalation workflows
        5. Subscription billing, white-label branding and API access

        Suggested positioning: **“The simple HSE action tracker teams actually use.”**
        """
    )
    st.warning("This MVP is suitable for demonstration and early customer validation. Add authentication, backups and managed database hosting before production deployment.")

st.caption(f"{APP_NAME} MVP • Built with Streamlit, SQLite, Pandas and Plotly")
