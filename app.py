import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="IPL Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------
# GLOBAL STYLES
# -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;500&display=swap');

/* Base */
html, body, [class*="css"] {
    background-color: #0a0d12 !important;
    color: #e8eaf0 !important;
    font-family: 'Inter', sans-serif;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Main container */
.block-container {
    padding: 2rem 3rem !important;
    max-width: 1400px;
}

/* Title */
.ipl-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: 2px;
    background: linear-gradient(135deg, #f5a623 0%, #ff6b35 50%, #e8eaf0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0;
    line-height: 1.1;
}

.ipl-subtitle {
    font-size: 0.85rem;
    color: #5a6070;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 4px;
    margin-bottom: 2rem;
}

/* Divider */
.ipl-divider {
    height: 1px;
    background: linear-gradient(90deg, #f5a623, #ff6b35, transparent);
    margin: 1.5rem 0;
    border: none;
}

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, #111520 0%, #161b28 100%);
    border: 1px solid #1e2535;
    border-radius: 12px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #f5a623, #ff6b35);
}
.kpi-label {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #5a6070;
    margin-bottom: 6px;
}
.kpi-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #f5a623;
    line-height: 1;
}
.kpi-icon {
    position: absolute;
    top: 16px; right: 18px;
    font-size: 1.4rem;
    opacity: 0.15;
}

/* Section headers */
.section-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.4rem;
    font-weight: 600;
    letter-spacing: 1px;
    color: #e8eaf0;
    margin: 2rem 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1e2535;
    margin-left: 12px;
}

/* Phase badge */
.phase-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    background: linear-gradient(135deg, #f5a623, #ff6b35);
    color: #0a0d12;
    margin-bottom: 1.5rem;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #111520;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #1e2535;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    letter-spacing: 1px;
    font-size: 0.95rem;
    color: #5a6070 !important;
    border-radius: 8px !important;
    padding: 8px 24px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #f5a623, #ff6b35) !important;
    color: #0a0d12 !important;
}

/* Search */
.stTextInput input {
    background: #111520 !important;
    border: 1px solid #1e2535 !important;
    border-radius: 8px !important;
    color: #e8eaf0 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 10px 16px !important;
}
.stTextInput input:focus {
    border-color: #f5a623 !important;
    box-shadow: 0 0 0 1px #f5a62322 !important;
}

/* Dataframe */
.stDataFrame {
    border: 1px solid #1e2535 !important;
    border-radius: 10px !important;
    overflow: hidden;
}

/* Expander */
.streamlit-expanderHeader {
    background: #111520 !important;
    border: 1px solid #1e2535 !important;
    border-radius: 8px !important;
    color: #e8eaf0 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0d12; }
::-webkit-scrollbar-thumb { background: #1e2535; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #f5a623; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# PLOTLY THEME
# -------------------------
PLOT_THEME = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#9aa0b0', size=12),
    xaxis=dict(
        gridcolor='#1e2535',
        linecolor='#1e2535',
        tickcolor='#1e2535',
        title_font=dict(color='#5a6070', size=11),
    ),
    yaxis=dict(
        gridcolor='#1e2535',
        linecolor='#1e2535',
        tickcolor='#1e2535',
        title_font=dict(color='#5a6070', size=11),
    ),
    margin=dict(l=10, r=10, t=40, b=10),
    hoverlabel=dict(
        bgcolor='#161b28',
        bordercolor='#f5a623',
        font=dict(color='#e8eaf0', size=12)
    ),
    coloraxis_showscale=False,
)

ORANGE_SCALE = [[0, '#ff6b35'], [0.5, '#f5a623'], [1.0, '#ffd97d']]
BLUE_SCALE   = [[0, '#1a3a5c'], [0.5, '#2e86c1'], [1.0, '#7fb3d3']]

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    matches = pd.read_csv("data/matches.csv")
    deliveries = pd.read_csv("data/deliveries.csv")
    return matches, deliveries

matches, deliveries = load_data()

# -------------------------
# HEADER
# -------------------------
col_title, col_search = st.columns([3, 1])
with col_title:
    st.markdown('<div class="ipl-title">IPL ANALYTICS</div>', unsafe_allow_html=True)
    st.markdown('<div class="ipl-subtitle">Performance Intelligence · 2008 – 2023</div>', unsafe_allow_html=True)
with col_search:
    st.markdown("<br>", unsafe_allow_html=True)
    player_name = st.text_input("", placeholder="🔍 Search player...")

st.markdown('<hr class="ipl-divider">', unsafe_allow_html=True)

# -------------------------
# KPI CARDS
# -------------------------
def show_kpis(df, phase_name):
    total_runs    = int(df['batsman_runs'].sum())
    total_wickets = int(df['is_wicket'].sum())
    economy       = round((df['total_runs'].sum() / df['ball'].count()) * 6, 2)
    total_balls   = int(df['ball'].count())

    st.markdown(f'<div class="phase-badge">{phase_name}</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "Total Runs",    f"{total_runs:,}",    "🏏"),
        (c2, "Wickets",       f"{total_wickets:,}",  "🎯"),
        (c3, "Avg Economy",   f"{economy}",           "📊"),
        (c4, "Balls Bowled",  f"{total_balls:,}",    "⚡"),
    ]
    for col, label, value, icon in cards:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

# -------------------------
# BATTING
# -------------------------
def batting_analysis(df):
    st.markdown('<div class="section-header">📊 Batting Impact</div>', unsafe_allow_html=True)

    bat = df.groupby("batter").agg(
        runs=("batsman_runs", "sum"),
        balls=("ball", "count")
    ).reset_index()

    bat["strike_rate"] = (bat["runs"] / bat["balls"]) * 100
    bat = bat[bat["balls"] > 200]
    bat["impact"] = bat["strike_rate"] * np.log(bat["balls"])

    if player_name:
        bat = bat[bat["batter"].str.contains(player_name, case=False)]

    col1, col2 = st.columns([3, 2])

    with col1:
        top = bat.sort_values("impact", ascending=True).tail(10)
        fig = go.Figure(go.Bar(
            x=top["impact"],
            y=top["batter"],
            orientation='h',
            marker=dict(
                color=top["impact"],
                colorscale=ORANGE_SCALE,
                line=dict(width=0)
            ),
            hovertemplate="<b>%{y}</b><br>Impact: %{x:.1f}<extra></extra>"
        ))
        fig.update_layout(
            title=dict(text="Top 10 — Impact Score (SR × log Volume)", font=dict(size=13, color='#9aa0b0')),
            xaxis_title="Impact Score",
            yaxis_title="",
            height=380,
            **PLOT_THEME
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        top_sr = bat[bat["balls"] > 300].sort_values("strike_rate", ascending=True).tail(10)
        fig2 = go.Figure(go.Bar(
            x=top_sr["strike_rate"],
            y=top_sr["batter"],
            orientation='h',
            marker=dict(
                color=top_sr["strike_rate"],
                colorscale=BLUE_SCALE,
                line=dict(width=0)
            ),
            hovertemplate="<b>%{y}</b><br>SR: %{x:.1f}<extra></extra>"
        ))
        fig2.update_layout(
            title=dict(text="Top 10 — Strike Rate (min 300 balls)", font=dict(size=13, color='#9aa0b0')),
            xaxis_title="Strike Rate",
            yaxis_title="",
            height=380,
            **PLOT_THEME
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Scatter — runs vs SR
    top_scatter = bat.sort_values("impact", ascending=False).head(30)
    fig3 = px.scatter(
        top_scatter, x="runs", y="strike_rate",
        text="batter", size="impact",
        color="impact", color_continuous_scale=["#ff6b35", "#f5a623", "#ffd97d"],
        hover_data={"impact": ":.1f", "balls": True}
    )
    fig3.update_traces(textposition='top center', textfont=dict(size=9, color='#9aa0b0'))
    fig3.update_layout(
        title=dict(text="Runs vs Strike Rate — Top 30 by Impact", font=dict(size=13, color='#9aa0b0')),
        xaxis_title="Total Runs", yaxis_title="Strike Rate",
        height=420,
        **PLOT_THEME
    )
    st.plotly_chart(fig3, use_container_width=True)

    with st.expander("📋 Full Batting Table"):
        display = bat.sort_values("impact", ascending=False).head(25).copy()
        display.columns = ["Player", "Runs", "Balls", "Strike Rate", "Impact Score"]
        display = display.round(2)
        st.dataframe(display, use_container_width=True, hide_index=True)

# -------------------------
# BOWLING
# -------------------------
def bowling_analysis(df, phase):
    st.markdown('<div class="section-header">🎯 Bowling Impact</div>', unsafe_allow_html=True)

    # Career-level filters — only include bowlers with serious IPL careers
    career = deliveries.groupby("bowler").agg(
        career_balls=("ball", "count"),
        career_wickets=("is_wicket", "sum")
    ).reset_index()
    qualified = career[
        (career["career_balls"] >= 1200) &
        (career["career_wickets"] >= 60)
    ]["bowler"]

    # Phase-level stats
    bowl = df.groupby("bowler").agg(
        runs=("total_runs", "sum"),
        balls=("ball", "count"),
        wickets=("is_wicket", "sum")
    ).reset_index()

    # Phase-aware minimums — death overs have fewer balls per bowler by nature
    phase_ball_min = {
        "Powerplay": 240,
        "Middle":    300,
        "Death":     150,   # 25 overs in death phase — realistic for specialists
        "Overall":   500
    }
    phase_wkt_min = {
        "Powerplay": 15,
        "Middle":    20,
        "Death":     12,
        "Overall":   40
    }
    ball_min = phase_ball_min.get(phase, 240)
    wkt_min  = phase_wkt_min.get(phase, 15)

    bowl = bowl[
        bowl["bowler"].isin(qualified) &
        (bowl["balls"] >= ball_min) &
        (bowl["wickets"] >= wkt_min)
    ]

    bowl["economy"] = (bowl["runs"] / bowl["balls"]) * 6
    bowl["sr"]      = bowl["balls"] / bowl["wickets"]
    bowl["wpo"]     = bowl["wickets"] / (bowl["balls"] / 6)

    # Normalise each component before combining
    bowl["wpo_norm"] = bowl["wpo"] / bowl["wpo"].max()
    bowl["eco_norm"] = (1 / bowl["economy"]) / (1 / bowl["economy"]).max()
    bowl["sr_norm"]  = (1 / bowl["sr"])  / (1 / bowl["sr"]).max()

    bowl["impact"] = (
        bowl["wpo_norm"] * 0.5 +
        bowl["eco_norm"] * 0.3 +
        bowl["sr_norm"]  * 0.2
    ) * 100

    if player_name:
        bowl = bowl[bowl["bowler"].str.contains(player_name, case=False)]

    col1, col2 = st.columns([3, 2])

    with col1:
        top = bowl.sort_values("impact", ascending=True).tail(10)
        # Manual colour mapping so low=dark, high=bright
        norm_vals = (top["impact"] - top["impact"].min()) / (top["impact"].max() - top["impact"].min() + 1e-9)
        colors = [f"rgba({int(42 + v*171)}, {int(204 - v*50)}, {int(113 - v*60)}, 1)" for v in norm_vals]
        fig = go.Figure(go.Bar(
            x=top["impact"],
            y=top["bowler"],
            orientation='h',
            marker=dict(color=colors, line=dict(width=0)),
            hovertemplate="<b>%{y}</b><br>Impact: %{x:.1f}<extra></extra>"
        ))
        fig.update_layout(
            title=dict(text="Top 10 — Bowling Impact Score", font=dict(size=13, color='#9aa0b0')),
            xaxis_title="Impact Score",
            yaxis_title="",
            height=380,
            **PLOT_THEME
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Economy chart — lower is better, so sort ascending and invert colour
        top_eco = bowl.sort_values("economy").head(10)
        norm_eco = 1 - (top_eco["economy"] - top_eco["economy"].min()) / (top_eco["economy"].max() - top_eco["economy"].min() + 1e-9)
        eco_colors = [f"rgba({int(42 + v*171)}, {int(204 - v*50)}, {int(113 - v*60)}, 1)" for v in norm_eco]
        fig2 = go.Figure(go.Bar(
            x=top_eco["economy"],
            y=top_eco["bowler"],
            orientation='h',
            marker=dict(color=eco_colors, line=dict(width=0)),
            hovertemplate="<b>%{y}</b><br>Economy: %{x:.2f}<extra></extra>"
        ))
        fig2.update_layout(
            title=dict(text="Best Economy (qualified bowlers)", font=dict(size=13, color='#9aa0b0')),
            xaxis_title="Economy Rate",
            yaxis_title="",
            height=380,
            **PLOT_THEME
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Scatter — economy vs wickets
    top_scatter = bowl.sort_values("impact", ascending=False).head(30)
    fig3 = px.scatter(
        top_scatter, x="economy", y="wickets",
        text="bowler",
        size="impact",
        color="impact",
        color_continuous_scale=["#1a3a2a", "#2ecc71", "#a8e6cf"],
        hover_data={"impact": ":.1f", "wpo": ":.3f", "sr": ":.1f"}
    )
    fig3.update_traces(textposition='top center', textfont=dict(size=9, color='#9aa0b0'))
    fig3.update_layout(
        title=dict(text="Economy vs Wickets — Top 30 Qualified Bowlers", font=dict(size=13, color='#9aa0b0')),
        xaxis_title="Economy Rate", yaxis_title="Phase Wickets",
        height=420,
        **PLOT_THEME
    )
    st.plotly_chart(fig3, use_container_width=True)

    with st.expander("📋 Full Bowling Table"):
        display = bowl.sort_values("impact", ascending=False).head(25).copy()
        display = display[["bowler", "wickets", "balls", "economy", "sr", "wpo", "impact"]].round(3)
        display.columns = ["Bowler", "Wickets", "Balls", "Economy", "Strike Rate", "Wkts/Over", "Impact"]
        st.dataframe(display, use_container_width=True, hide_index=True)

# -------------------------
# ALL ROUNDERS
# -------------------------
def allrounders_phase(df, phase):
    st.markdown('<div class="section-header">🔥 All-Rounder Rankings</div>', unsafe_allow_html=True)

    with st.expander("ℹ️ Impact Formula"):
        st.markdown("""
        **Score = (Batting Impact × 0.6) + (Bowling Impact × 0.4)**
        
        - Batting Impact = `Strike Rate × log(Balls)`
        - Bowling Impact = `Wickets/Over + Economy Control`
        - Both normalised to 0–1 before combining
        """)

    bat = df.groupby("batter").agg(
        runs=("batsman_runs", "sum"),
        balls=("ball", "count")
    )
    bat["sr"]         = (bat["runs"] / bat["balls"]) * 100
    bat["bat_impact"] = bat["sr"] * np.log(bat["balls"])

    bowl = df.groupby("bowler").agg(
        wickets=("is_wicket", "sum"),
        bowl_balls=("ball", "count"),
        total_runs=("total_runs", "sum")
    )
    bowl["econ"]        = (bowl["total_runs"] / bowl["bowl_balls"]) * 6
    bowl["wpo"]         = bowl["wickets"] / (bowl["bowl_balls"] / 6)
    bowl["bowl_impact"] = bowl["wpo"] + (1 / bowl["econ"])

    ar = bat.merge(bowl, left_index=True, right_index=True)
    ar["bat_norm"]  = ar["bat_impact"] / ar["bat_impact"].max()
    ar["bowl_norm"] = ar["bowl_impact"] / ar["bowl_impact"].max()
    ar["impact"]    = ar["bat_norm"] * 0.6 + ar["bowl_norm"] * 0.4
    ar = ar[(ar["runs"] > 300) & (ar["wickets"] > 10)]

    if player_name:
        ar = ar[ar.index.str.contains(player_name, case=False)]

    top = ar.sort_values("impact", ascending=False).head(10).reset_index()
    top.rename(columns={"index": "player", "batter": "player"}, inplace=True)
    if "batter" in top.columns:
        top.rename(columns={"batter": "player"}, inplace=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Batting',
            x=top["player"] if "player" in top.columns else top.index,
            y=top["bat_norm"],
            marker_color='#f5a623',
            hovertemplate="<b>%{x}</b><br>Batting: %{y:.3f}<extra></extra>"
        ))
        fig.add_trace(go.Bar(
            name='Bowling',
            x=top["player"] if "player" in top.columns else top.index,
            y=top["bowl_norm"],
            marker_color='#2ecc71',
            hovertemplate="<b>%{x}</b><br>Bowling: %{y:.3f}<extra></extra>"
        ))
        fig.update_layout(
            barmode='stack',
            title=dict(text="All-Rounder Impact — Batting vs Bowling Split", font=dict(size=13, color='#9aa0b0')),
            xaxis_title="", yaxis_title="Normalised Impact",
            height=400,
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#9aa0b0')),
            **PLOT_THEME
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        player_col = "player" if "player" in top.columns else top.index
        fig2 = go.Figure(go.Scatterpolar(
            r=top["impact"],
            theta=top["player"] if "player" in top.columns else [str(i) for i in top.index],
            fill='toself',
            line_color='#f5a623',
            fillcolor='rgba(245,166,35,0.15)',
            hovertemplate="<b>%{theta}</b><br>Impact: %{r:.3f}<extra></extra>"
        ))
        fig2.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, color='#1e2535', gridcolor='#1e2535'),
                angularaxis=dict(color='#9aa0b0', gridcolor='#1e2535')
            ),
            title=dict(text="All-Rounder Radar", font=dict(size=13, color='#9aa0b0')),
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#9aa0b0'),
            margin=dict(l=40, r=40, t=40, b=40),
            hoverlabel=dict(bgcolor='#161b28', bordercolor='#f5a623', font=dict(color='#e8eaf0'))
        )
        st.plotly_chart(fig2, use_container_width=True)

    with st.expander("📋 Full All-Rounder Table"):
        display = top[["player", "runs", "wickets", "bat_norm", "bowl_norm", "impact"]].round(3)
        display.columns = ["Player", "Runs", "Wickets", "Batting Score", "Bowling Score", "Impact"]
        st.dataframe(display, use_container_width=True, hide_index=True)

# -------------------------
# TEAM CONTRIBUTION
# -------------------------
def team_contribution(df):
    st.markdown('<div class="section-header">🏆 Team Contribution</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        runs = df.groupby(["batting_team", "batter"])["batsman_runs"].sum().reset_index()
        top_runs = runs.sort_values("batsman_runs", ascending=False).head(15)
        fig = px.bar(
            top_runs, x="batter", y="batsman_runs",
            color="batting_team",
            color_discrete_sequence=px.colors.qualitative.Bold,
            hover_data=["batting_team"]
        )
        fig.update_layout(
            title=dict(text="Top Run Scorers by Team", font=dict(size=13, color='#9aa0b0')),
            xaxis_title="", yaxis_title="Runs",
            xaxis_tickangle=-35,
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#9aa0b0'), title_text=''),
            height=380,
            **PLOT_THEME
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        wkts = df.groupby(["bowling_team", "bowler"])["is_wicket"].sum().reset_index()
        top_wkts = wkts.sort_values("is_wicket", ascending=False).head(15)
        fig2 = px.bar(
            top_wkts, x="bowler", y="is_wicket",
            color="bowling_team",
            color_discrete_sequence=px.colors.qualitative.Vivid,
            hover_data=["bowling_team"]
        )
        fig2.update_layout(
            title=dict(text="Top Wicket Takers by Team", font=dict(size=13, color='#9aa0b0')),
            xaxis_title="", yaxis_title="Wickets",
            xaxis_tickangle=-35,
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#9aa0b0'), title_text=''),
            height=380,
            **PLOT_THEME
        )
        st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# TABS
# -------------------------
tabs = st.tabs(["⚡ Powerplay", "🔄 Middle Overs", "💀 Death Overs", "🏏 Overall"])

phases = {
    "Powerplay":   deliveries[deliveries["over"] <= 6],
    "Middle":      deliveries[(deliveries["over"] > 6) & (deliveries["over"] < 16)],
    "Death":       deliveries[deliveries["over"] >= 16],
    "Overall":     deliveries
}

phase_labels = {
    "Powerplay": "⚡ Powerplay — Overs 1–6",
    "Middle":    "🔄 Middle Overs — 7–15",
    "Death":     "💀 Death Overs — 16–20",
    "Overall":   "🏏 Full Tournament"
}

for tab, name in zip(tabs, phases.keys()):
    with tab:
        df = phases[name]
        show_kpis(df, phase_labels[name])
        st.markdown('<hr class="ipl-divider">', unsafe_allow_html=True)
        batting_analysis(df)
        st.markdown('<hr class="ipl-divider">', unsafe_allow_html=True)
        bowling_analysis(df, name)
        st.markdown('<hr class="ipl-divider">', unsafe_allow_html=True)
        allrounders_phase(df, name)
        st.markdown('<hr class="ipl-divider">', unsafe_allow_html=True)
        team_contribution(df)