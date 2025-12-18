# Projectz AI - Growth & Retention Dashboard

A data analytics dashboard built to visualize key growth and retention metrics for [Projectz AI](https://projectzai.com/), a home design + contractor matching platform.

![Dashboard Preview](preview.png)

## Overview

This dashboard demonstrates the KPIs that matter most for a consumer marketplace startup:

- **Conversion Funnel** — Track drop-off from visitors → signups → designs → contractor requests
- **Design-to-Match Rate** — Core monetization metric (users who generate designs AND request contractors)
- **Time-to-First-Design** — Activation speed as a leading indicator of retention
- **Weekly Retention Cohorts** — Visualize user engagement decay over time
- **Traffic Sources** — Estimated channel mix for acquisition strategy

## Key Metrics Tracked

| Metric | Why It Matters |
|--------|----------------|
| Design-to-Match Rate | Directly measures product-market fit and monetization potential |
| Time-to-First-Design | Lower = less friction = better activation and retention |
| Week-over-Week Growth | Tracks acquisition momentum |
| Cohort Retention | Identifies when users drop off and where to intervene |

## Tech Stack

- **Python 3.10+**
- **Streamlit** — Dashboard framework
- **Plotly** — Interactive visualizations
- **Pandas / NumPy** — Data manipulation

## Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/projectz-dashboard.git
cd projectz-dashboard

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

## Project Structure

```
projectz-dashboard/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── preview.png         # Dashboard screenshot (optional)
```

## Data Note

This dashboard uses **illustrative data** modeled on early-stage SaaS benchmarks. In production, connect to:

- **Google Analytics 4** — Traffic and funnel events
- **Mixpanel / Amplitude** — Product analytics and cohorts
- **Internal database** — User actions and contractor matches

## Growth Opportunities Identified

Based on the funnel analysis:

1. **Design → Contractor gap (18% conversion)**
   - Add "Save & Share Design" with email capture
   - Re-engagement emails for users with saved designs

2. **Time-to-First-Design optimization**
   - Simplify onboarding flow
   - Add pre-loaded design templates

3. **Week 2 retention drop-off**
   - Implement design reminders
   - Add contractor availability notifications

## Author

**Bhavan Kumar Basavaraju**  
Data Analyst | [LinkedIn](https://www.linkedin.com/in/bhavan-kumar-358755158/) | [GitHub](https://github.com/bhavanbk2)

---

*Built as a data insights demonstration for Projectz AI*