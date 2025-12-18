import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page config
st.set_page_config(
    page_title="Projectz AI - Growth Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for polished dark theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    
    /* Main background */
    .stApp {
        background: linear-gradient(180deg, #0a0f1a 0%, #111827 100%);
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 32px;
    }
    
    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 32px;
        font-weight: 700;
        background: linear-gradient(90deg, #f1f5f9 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .main-subtitle {
        font-family: 'Inter', sans-serif;
        color: #64748b;
        font-size: 14px;
        margin-top: 8px;
    }
    
    .live-badge {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #10b981;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    
    /* Section headers */
    .section-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 20px;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Metric cards */
    .metric-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 16px;
        padding: 24px;
        height: 100%;
    }
    
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        font-weight: 500;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 36px;
        font-weight: 700;
        color: #f1f5f9;
        line-height: 1;
    }
    
    .metric-delta-positive {
        color: #10b981;
        font-size: 14px;
        font-weight: 600;
        margin-top: 8px;
    }
    
    .metric-delta-negative {
        color: #ef4444;
        font-size: 14px;
        font-weight: 600;
        margin-top: 8px;
    }
    
    /* Chart containers */
    .chart-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 16px;
        padding: 24px;
    }
    
    .chart-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 18px;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 4px;
    }
    
    .chart-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: #64748b;
        margin-bottom: 16px;
    }
    
    /* Insight boxes */
    .insight-box {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 12px;
        padding: 16px 20px;
        margin-top: 16px;
    }
    
    .insight-text {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        font-weight: 500;
        color: #fbbf24;
        line-height: 1.5;
    }
    
    .insight-box-success {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .insight-box-success .insight-text {
        color: #34d399;
    }
    
    .insight-box-purple {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    
    .insight-box-purple .insight-text {
        color: #a78bfa;
    }
    
    /* Growth opportunities */
    .opportunities-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 16px;
        padding: 28px;
    }
    
    .opportunity-item {
        margin-bottom: 20px;
        padding-bottom: 20px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .opportunity-item:last-child {
        margin-bottom: 0;
        padding-bottom: 0;
        border-bottom: none;
    }
    
    .opportunity-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 15px;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 8px;
    }
    
    .opportunity-bullet {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: #94a3b8;
        margin-left: 16px;
        line-height: 1.7;
    }
    
    /* Footer */
    .footer-container {
        text-align: center;
        padding: 32px 0;
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        margin-top: 40px;
    }
    
    .footer-note {
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        color: #475569;
        margin-bottom: 8px;
    }
    
    .footer-author {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 14px;
        font-weight: 600;
        color: #64748b;
    }
    
    /* Divider */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(148, 163, 184, 0.2), transparent);
        margin: 32px 0;
    }
    
    /* Override Streamlit metric styling */
    [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 32px !important;
        font-weight: 700 !important;
        color: #f1f5f9 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 12px !important;
        color: #94a3b8 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============ HEADER ============
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 class="main-title">Projectz AI - Growth & Retention Dashboard</h1>
            <p class="main-subtitle">KPI tracking for home design + contractor matching platform</p>
        </div>
        <span class="live-badge">● Demo Data</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============ GENERATE DATA ============
np.random.seed(42)
dates = pd.date_range(end=datetime.now(), periods=90, freq='D')

base_visitors = 150
growth_rate = 1.02
visitors = [int(base_visitors * (growth_rate ** i) * np.random.uniform(0.8, 1.2)) for i in range(90)]
signups = [int(v * np.random.uniform(0.08, 0.12)) for v in visitors]
designs_generated = [int(s * np.random.uniform(0.45, 0.65)) for s in signups]
contractor_requests = [int(d * np.random.uniform(0.15, 0.25)) for d in designs_generated]

df = pd.DataFrame({
    'date': dates,
    'visitors': visitors,
    'signups': signups,
    'designs_generated': designs_generated,
    'contractor_requests': contractor_requests
})

# Calculate metrics
total_visitors = sum(visitors[-30:])
total_signups = sum(signups[-30:])
total_designs = sum(designs_generated[-30:])
total_requests = sum(contractor_requests[-30:])

wow_visitors = (sum(visitors[-7:]) - sum(visitors[-14:-7])) / sum(visitors[-14:-7]) * 100
wow_signups = (sum(signups[-7:]) - sum(signups[-14:-7])) / sum(signups[-14:-7]) * 100
design_rate = (total_designs / total_signups * 100) if total_signups > 0 else 0
conversion_rate = (total_requests / total_designs * 100) if total_designs > 0 else 0

# ============ KEY METRICS ============
st.markdown('<p class="section-header">📊 Last 30 Days - Key Metrics</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-container">
        <p class="metric-label">Website Visitors</p>
        <p class="metric-value">{total_visitors:,}</p>
        <p class="metric-delta-positive">↑ {wow_visitors:.1f}% WoW</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-container">
        <p class="metric-label">New Signups</p>
        <p class="metric-value">{total_signups:,}</p>
        <p class="metric-delta-positive">↑ {wow_signups:.1f}% WoW</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-container">
        <p class="metric-label">Designs Generated</p>
        <p class="metric-value">{total_designs:,}</p>
        <p class="metric-delta-positive">↑ {design_rate:.0f}% activation</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-container">
        <p class="metric-label">Contractor Requests</p>
        <p class="metric-value">{total_requests:,}</p>
        <p class="metric-delta-positive">↑ {conversion_rate:.0f}% of designs</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============ FUNNEL + TREND ============
col_left, col_right = st.columns([1, 1.5])

with col_left:
    st.markdown("""
    <div class="chart-container">
        <p class="chart-title">🎯 Conversion Funnel</p>
        <p class="chart-subtitle">Where users drop off in the journey</p>
    </div>
    """, unsafe_allow_html=True)
    
    funnel_data = {
        'Stage': ['Visitors', 'Signups', 'Designs Created', 'Contractor Requests'],
        'Count': [total_visitors, total_signups, total_designs, total_requests]
    }
    
    fig_funnel = go.Figure(go.Funnel(
        y=funnel_data['Stage'],
        x=funnel_data['Count'],
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(color=['#6366f1', '#8b5cf6', '#a855f7', '#d946ef']),
        connector={"line": {"color": "#334155", "dash": "dot", "width": 2}}
    ))
    
    fig_funnel.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", color="#94a3b8")
    )
    st.plotly_chart(fig_funnel, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        <p class="insight-text">⚡ <strong>Insight:</strong> 70% drop-off between Design → Match. Consider adding "Save & Share" to capture leads not ready to hire.</p>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div class="chart-container">
        <p class="chart-title">📈 Daily Trend (90 Days)</p>
        <p class="chart-subtitle">User acquisition and engagement over time</p>
    </div>
    """, unsafe_allow_html=True)
    
    fig_trend = go.Figure()
    
    fig_trend.add_trace(go.Scatter(
        x=df['date'], y=df['visitors'],
        name='Visitors', line=dict(color='#6366f1', width=2),
        fill='tozeroy', fillcolor='rgba(99, 102, 241, 0.1)'
    ))
    fig_trend.add_trace(go.Scatter(
        x=df['date'], y=df['signups'],
        name='Signups', line=dict(color='#8b5cf6', width=2)
    ))
    fig_trend.add_trace(go.Scatter(
        x=df['date'], y=df['designs_generated'],
        name='Designs', line=dict(color='#a855f7', width=2)
    ))
    fig_trend.add_trace(go.Scatter(
        x=df['date'], y=df['contractor_requests'],
        name='Contractor Requests', line=dict(color='#d946ef', width=2)
    ))
    
    fig_trend.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02,
            font=dict(size=11, color="#94a3b8")
        ),
        hovermode='x unified',
        xaxis=dict(gridcolor='rgba(148, 163, 184, 0.1)', color='#64748b'),
        yaxis=dict(gridcolor='rgba(148, 163, 184, 0.1)', color='#64748b'),
        font=dict(family="Inter", color="#94a3b8")
    )
    st.plotly_chart(fig_trend, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============ GROWTH METRICS ============
st.markdown('<p class="section-header">🚀 Growth & Retention Metrics That Matter</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="chart-container">
        <p class="chart-title">Design-to-Match Rate</p>
        <p class="chart-subtitle">% of users who generate a design AND request a contractor</p>
    </div>
    """, unsafe_allow_html=True)
    
    weekly_data = df.groupby(df['date'].dt.isocalendar().week).agg({
        'designs_generated': 'sum',
        'contractor_requests': 'sum'
    }).reset_index()
    weekly_data['match_rate'] = (weekly_data['contractor_requests'] / weekly_data['designs_generated'] * 100).round(1)
    weekly_data = weekly_data.tail(12)
    
    colors = ['#7c3aed' if r < 15 else '#a855f7' if r < 18 else '#fbbf24' for r in weekly_data['match_rate']]
    
    fig_match = go.Figure(data=[
        go.Bar(
            x=weekly_data['week'],
            y=weekly_data['match_rate'],
            marker_color=colors,
            text=weekly_data['match_rate'].apply(lambda x: f'{x:.0f}%'),
            textposition='outside',
            textfont=dict(size=10, color='#94a3b8')
        )
    ])
    
    fig_match.add_hline(y=20, line_dash="dash", line_color="#ef4444", 
                        annotation_text="Target: 20%",
                        annotation_font_color="#ef4444")
    
    fig_match.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=10, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title="Week", gridcolor='rgba(148, 163, 184, 0.1)', color='#64748b'),
        yaxis=dict(gridcolor='rgba(148, 163, 184, 0.1)', color='#64748b', range=[0, 25]),
        font=dict(family="Inter", color="#94a3b8"),
        showlegend=False
    )
    st.plotly_chart(fig_match, use_container_width=True)
    
    current_match_rate = (total_requests / total_designs * 100) if total_designs > 0 else 0
    st.markdown(f"""
    <div class="insight-box insight-box-purple">
        <p class="insight-text">📊 <strong>Current Rate: {current_match_rate:.1f}%</strong> — Target: 20%+</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="chart-container">
        <p class="chart-title">Time-to-First-Design</p>
        <p class="chart-subtitle">How quickly new users generate their first design</p>
    </div>
    """, unsafe_allow_html=True)
    
    np.random.seed(42)
    ttfd = np.concatenate([
        np.random.exponential(5, 300),
        np.random.normal(15, 5, 200),
        np.random.normal(45, 10, 100)
    ])
    ttfd = ttfd[(ttfd > 0) & (ttfd < 80)]
    
    fig_ttfd = go.Figure(data=[
        go.Histogram(
            x=ttfd,
            nbinsx=25,
            marker_color='#8b5cf6',
            opacity=0.8
        )
    ])
    
    fig_ttfd.add_vline(x=10, line_dash="dash", line_color="#10b981",
                       annotation_text="Target: <10 min",
                       annotation_font_color="#10b981")
    
    fig_ttfd.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=10, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title="Minutes to First Design", gridcolor='rgba(148, 163, 184, 0.1)', color='#64748b'),
        yaxis=dict(title="Count", gridcolor='rgba(148, 163, 184, 0.1)', color='#64748b'),
        font=dict(family="Inter", color="#94a3b8"),
        bargap=0.1
    )
    st.plotly_chart(fig_ttfd, use_container_width=True)
    
    median_ttfd = np.median(ttfd)
    st.markdown(f"""
    <div class="insight-box insight-box-success">
        <p class="insight-text">✓ <strong>Median: {median_ttfd:.0f} min</strong> — Target: <10 min (lower = better activation)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============ RETENTION COHORT ============
st.markdown('<p class="section-header">📅 Weekly Retention Cohort</p>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748b; font-size: 13px; margin-top: -12px; margin-bottom: 20px;">% of users returning each week after signup</p>', unsafe_allow_html=True)

cohort_weeks = 8
cohort_data = []
for week in range(cohort_weeks):
    row = [100]
    for retention_week in range(1, cohort_weeks - week):
        base_retention = 100 * (0.55 ** retention_week) + np.random.uniform(-3, 3)
        row.append(max(5, min(100, base_retention)))
    while len(row) < cohort_weeks:
        row.append(None)
    cohort_data.append(row)

cohort_df = pd.DataFrame(
    cohort_data,
    index=[f'Week {i+1}' for i in range(cohort_weeks)],
    columns=[f'Week {i}' for i in range(cohort_weeks)]
)

# Create text annotations
text_vals = []
for row in cohort_df.values:
    text_row = []
    for val in row:
        if val is not None:
            text_row.append(f'{val:.0f}%')
        else:
            text_row.append('')
    text_vals.append(text_row)

fig_cohort = go.Figure(data=go.Heatmap(
    z=cohort_df.values,
    x=cohort_df.columns,
    y=cohort_df.index,
    colorscale=[
        [0, '#dc2626'],
        [0.25, '#f97316'],
        [0.5, '#eab308'],
        [0.75, '#22c55e'],
        [1, '#16a34a']
    ],
    text=text_vals,
    texttemplate="%{text}",
    textfont={"size": 11, "color": "#f1f5f9"},
    hoverongaps=False,
    showscale=True,
    colorbar=dict(
        title=dict(text="Retention %", font=dict(color="#94a3b8")),
        tickfont=dict(color="#94a3b8")
    )
))

fig_cohort.update_layout(
    height=320,
    margin=dict(l=20, r=20, t=10, b=10),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(title="Weeks Since Signup", color='#64748b', tickfont=dict(color='#94a3b8')),
    yaxis=dict(title="Signup Cohort", color='#64748b', tickfont=dict(color='#94a3b8')),
    font=dict(family="Inter", color="#94a3b8")
)
st.plotly_chart(fig_cohort, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============ TRAFFIC + OPPORTUNITIES ============
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown('<p class="section-header">🌐 Traffic Sources (Estimated)</p>', unsafe_allow_html=True)
    
    sources = {
        'Source': ['Organic Search', 'Direct', 'Social', 'Referral', 'Paid'],
        'Percentage': [35, 28, 18, 12, 7]
    }
    
    fig_sources = go.Figure(data=[go.Pie(
        labels=sources['Source'],
        values=sources['Percentage'],
        hole=0.5,
        marker=dict(colors=['#6366f1', '#8b5cf6', '#f59e0b', '#10b981', '#64748b']),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(size=11, color='#94a3b8')
    )])
    
    fig_sources.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(family="Inter", color="#94a3b8")
    )
    st.plotly_chart(fig_sources, use_container_width=True)

with col2:
    st.markdown('<p class="section-header">💡 Growth Opportunities</p>', unsafe_allow_html=True)
    
    opportunities_html = """
<div class="opportunities-container">
<p style="color: #94a3b8; font-size: 13px; margin-bottom: 20px;">Based on funnel analysis:</p>
<div class="opportunity-item">
<p class="opportunity-title">1. Design → Contractor gap (18% conversion)</p>
<p class="opportunity-bullet">• Add "Save & Share Design" with email capture</p>
<p class="opportunity-bullet">• Re-engagement emails for users with saved designs</p>
</div>
<div class="opportunity-item">
<p class="opportunity-title">2. Time-to-First-Design too high</p>
<p class="opportunity-bullet">• Simplify onboarding flow</p>
<p class="opportunity-bullet">• Add pre-loaded design templates</p>
</div>
<div class="opportunity-item">
<p class="opportunity-title">3. Week 2 retention drop-off</p>
<p class="opportunity-bullet">• Implement design reminders</p>
<p class="opportunity-bullet">• Add contractor availability notifications</p>
</div>
</div>
"""
    st.markdown(opportunities_html, unsafe_allow_html=True)

# ============ FOOTER ============
st.markdown("""
<div class="footer-container">
    <p class="footer-note">This dashboard uses illustrative data modeled on early-stage SaaS benchmarks. Connect to actual analytics (GA4, Mixpanel, Amplitude) for real metrics.</p>
    <p class="footer-author">Built by Bhavan Kumar Basavaraju | Data Insights for Projectz AI</p>
</div>
""", unsafe_allow_html=True)