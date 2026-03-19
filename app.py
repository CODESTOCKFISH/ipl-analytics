import streamlit as st
import pandas as pd
import numpy as np

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="IPL Analytics", layout="wide")
st.title("🏏 IPL Analytics Dashboard")

# -------------------------
# LOAD DATA
# -------------------------
matches = pd.read_csv("data/matches.csv")
deliveries = pd.read_csv("data/deliveries.csv")

# -------------------------
# SEARCH
# -------------------------
player_name = st.text_input("🔍 Search Player (optional)")

# -------------------------
# FUNCTIONS
# -------------------------

def batting_analysis(df):
    st.subheader("Top Batters")

    metric = st.selectbox(
        "Batting Metric",
        ["Most Runs", "Best Strike Rate (Adjusted)"],
        key=str(df.shape)
    )

    batting = df.groupby("batter").agg({
        "batsman_runs": "sum",
        "ball": "count"
    })

    batting["strike_rate"] = (batting["batsman_runs"] / batting["ball"]) * 100
    batting = batting[batting["ball"] > 200]

    batting["impact_score"] = batting["strike_rate"] * np.log(batting["ball"])

    if player_name:
        batting = batting[batting.index.str.contains(player_name, case=False)]

    if metric == "Most Runs":
        batting = batting.sort_values("batsman_runs", ascending=False)
        chart = batting["batsman_runs"]
    else:
        batting = batting.sort_values("impact_score", ascending=False)
        chart = batting["impact_score"]

    st.caption("⚡ SR adjusted using volume (SR × log(balls faced))")
    st.bar_chart(chart.head(10))
    st.dataframe(batting.head(10))


def bowling_analysis(df, phase_name):
    st.subheader(f"Top Bowlers ({phase_name})")

    career_balls = deliveries.groupby("bowler")["ball"].count()
    career_wickets = deliveries.groupby("bowler")["is_wicket"].sum()

    bowler_stats = df.groupby("bowler").agg({
        "total_runs": "sum",
        "ball": "count",
        "is_wicket": "sum"
    })

    # Filters (ONLY experienced bowlers now)
    bowler_stats = bowler_stats[
        bowler_stats.index.isin(career_balls[career_balls > 800].index)
    ]

    bowler_stats = bowler_stats[
        bowler_stats.index.isin(career_wickets[career_wickets > 35].index)
    ]

    bowler_stats = bowler_stats[
        (bowler_stats["ball"] > 120) &
        (bowler_stats["is_wicket"] > 10)
    ]

    # Metrics
    bowler_stats["economy"] = (bowler_stats["total_runs"] / bowler_stats["ball"]) * 6
    bowler_stats["strike_rate"] = bowler_stats["ball"] / bowler_stats["is_wicket"]
    bowler_stats["wickets_per_over"] = bowler_stats["is_wicket"] / (bowler_stats["ball"] / 6)

    # Impact score
    bowler_stats["impact_score"] = (
        bowler_stats["is_wicket"] * 1.2 +
        bowler_stats["wickets_per_over"] * 45 +
        (6 / bowler_stats["economy"]) * 30
    )

    if player_name:
        bowler_stats = bowler_stats[
            bowler_stats.index.str.contains(player_name, case=False)
        ]

    top = bowler_stats.sort_values("impact_score", ascending=False).head(10)

    st.bar_chart(top["impact_score"])
    st.dataframe(top[["economy", "strike_rate", "wickets_per_over", "impact_score"]])


def allrounders_phase(df, phase_name):
    st.subheader(f"All-Rounders ({phase_name})")
    st.caption("Includes part-time contributors depending on phase role")

    batting = df.groupby("batter").agg({
        "batsman_runs": "sum",
        "ball": "count"
    }).rename(columns={"ball": "bat_balls"})

    bowling = df.groupby("bowler").agg({
        "is_wicket": "sum",
        "ball": "count"
    }).rename(columns={"ball": "bowl_balls"})

    ar = batting.merge(bowling, left_index=True, right_index=True)

    ar = ar[
        (ar["bat_balls"] > 100) &
        (ar["bowl_balls"] > 60) &
        (ar["is_wicket"] > 5)
    ]

    ar["score"] = (
        ar["batsman_runs"] * 0.6 +
        ar["is_wicket"] * 15 * 0.4
    )

    if player_name:
        ar = ar[ar.index.str.contains(player_name, case=False)]

    top = ar.sort_values("score", ascending=False).head(10)

    st.bar_chart(top["score"])
    st.dataframe(top[["batsman_runs", "is_wicket", "score"]])


def overall_batting():
    st.subheader("Overall Best Batters")

    batting = deliveries.groupby("batter").agg({
        "batsman_runs": "sum",
        "ball": "count"
    })

    batting["strike_rate"] = (batting["batsman_runs"] / batting["ball"]) * 100
    batting = batting[batting["ball"] > 500]

    batting["impact_score"] = batting["strike_rate"] * np.log(batting["ball"])

    if player_name:
        batting = batting[batting.index.str.contains(player_name, case=False)]

    top = batting.sort_values("impact_score", ascending=False).head(10)

    st.bar_chart(top["impact_score"])
    st.dataframe(top[["batsman_runs", "strike_rate", "impact_score"]])


def overall_bowling():
    st.subheader("Overall Best Bowlers")

    overall = deliveries.groupby("bowler").agg({
        "total_runs": "sum",
        "ball": "count",
        "is_wicket": "sum"
    })

    overall = overall[
        (overall["ball"] > 800) &
        (overall["is_wicket"] > 50)
    ]

    overall["economy"] = (overall["total_runs"] / overall["ball"]) * 6
    overall["strike_rate"] = overall["ball"] / overall["is_wicket"]
    overall["wickets_per_over"] = overall["is_wicket"] / (overall["ball"] / 6)

    overall["impact_score"] = (
        overall["is_wicket"] * 1.5 +
        overall["wickets_per_over"] * 40 +
        (6 / overall["economy"]) * 30
    )

    if player_name:
        overall = overall[overall.index.str.contains(player_name, case=False)]

    top = overall.sort_values("impact_score", ascending=False).head(10)

    st.bar_chart(top["impact_score"])
    st.dataframe(top[["economy", "strike_rate", "wickets_per_over", "impact_score"]])


def overall_allrounders():
    st.subheader("Overall All-Rounders")

    batting = deliveries.groupby("batter").agg({
        "batsman_runs": "sum",
        "ball": "count"
    }).rename(columns={"ball": "bat_balls"})

    bowling = deliveries.groupby("bowler").agg({
        "is_wicket": "sum",
        "ball": "count"
    }).rename(columns={"ball": "bowl_balls"})

    ar = batting.merge(bowling, left_index=True, right_index=True)

    ar = ar[
        (ar["bat_balls"] > 500) &
        (ar["bowl_balls"] > 300) &
        (ar["is_wicket"] > 45)
    ]

    ar["score"] = (
        ar["batsman_runs"] * 0.6 +
        ar["is_wicket"] * 20 * 0.4
    )

    if player_name:
        ar = ar[ar.index.str.contains(player_name, case=False)]

    top = ar.sort_values("score", ascending=False).head(10)

    st.bar_chart(top["score"])
    st.dataframe(top[["batsman_runs", "is_wicket", "score"]])


# -------------------------
# TABS
# -------------------------
tabs = st.tabs(["Powerplay", "Middle Overs", "Death Overs", "Overall"])

# Powerplay
with tabs[0]:
    st.header("Powerplay")
    df = deliveries[deliveries["over"] <= 6]
    batting_analysis(df)
    bowling_analysis(df, "Powerplay")
    allrounders_phase(df, "Powerplay")

# Middle
with tabs[1]:
    st.header("Middle Overs")
    df = deliveries[(deliveries["over"] > 6) & (deliveries["over"] < 16)]
    batting_analysis(df)
    bowling_analysis(df, "Middle Overs")
    allrounders_phase(df, "Middle Overs")

# Death
with tabs[2]:
    st.header("Death Overs")
    df = deliveries[deliveries["over"] >= 16]
    batting_analysis(df)
    bowling_analysis(df, "Death Overs")
    allrounders_phase(df, "Death Overs")

# Overall
with tabs[3]:
    st.header("Overall")
    overall_batting()
    overall_bowling()
    overall_allrounders()