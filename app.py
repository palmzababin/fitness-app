"""
FitOS — Complete Fitness Tracking & Planning Application
========================================================
A full-stack fitness app built with Streamlit.
Covers: BMR/TDEE calculation, workout generation, daily logging,
progress charts, behavior analysis, and goal prediction.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime, timedelta, date
import math

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FitOS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* Hide default streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* App background */
    .stApp {
        background-color: #0d0f14;
        color: #e8eaf0;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #12151c;
        border-right: 1px solid #1e2330;
    }
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #8892a4;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
    }

    /* Metric cards */
    .metric-card {
        background: #12151c;
        border: 1px solid #1e2330;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 12px;
    }
    .metric-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #5a6680;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 600;
        color: #e8eaf0;
        line-height: 1;
    }
    .metric-sub {
        font-size: 12px;
        color: #5a6680;
        margin-top: 4px;
    }
    .metric-accent { color: #4f9cf9; }
    .metric-green  { color: #34d399; }
    .metric-amber  { color: #fbbf24; }
    .metric-red    { color: #f87171; }

    /* Section headers */
    .section-title {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #5a6680;
        font-weight: 600;
        margin: 24px 0 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid #1e2330;
    }

    /* Insight boxes */
    .insight-box {
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
        font-size: 13px;
        line-height: 1.6;
    }
    .insight-warn { background: #2a1f0e; border-left: 3px solid #fbbf24; color: #fde68a; }
    .insight-good { background: #0d2218; border-left: 3px solid #34d399; color: #6ee7b7; }
    .insight-info { background: #0d1a2e; border-left: 3px solid #4f9cf9; color: #93c5fd; }
    .insight-bad  { background: #2a0e0e; border-left: 3px solid #f87171; color: #fca5a5; }

    /* Workout exercise card */
    .exercise-card {
        background: #12151c;
        border: 1px solid #1e2330;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .exercise-name { font-weight: 500; font-size: 14px; color: #e8eaf0; }
    .exercise-detail { font-size: 12px; color: #5a6680; margin-top: 2px; }
    .exercise-badge {
        font-size: 11px;
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: 600;
    }

    /* Day header */
    .day-header {
        background: linear-gradient(135deg, #1a1f2e, #12151c);
        border: 1px solid #1e2330;
        border-radius: 10px;
        padding: 12px 18px;
        margin: 16px 0 10px;
        font-weight: 600;
        font-size: 15px;
        color: #4f9cf9;
        letter-spacing: 0.02em;
    }

    /* Progress bar */
    .progress-bar-container {
        background: #1e2330;
        border-radius: 6px;
        height: 8px;
        margin: 8px 0;
        overflow: hidden;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 6px;
        transition: width 0.3s ease;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #12151c;
        border-bottom: 1px solid #1e2330;
        gap: 0;
    }
    .stTabs [data-baseweb="tab"] {
        color: #5a6680;
        font-size: 13px;
        font-weight: 500;
        padding: 12px 20px;
        border-bottom: 2px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        color: #4f9cf9;
        border-bottom-color: #4f9cf9;
        background: transparent;
    }

    /* Input styling */
    .stNumberInput input, .stTextInput input, .stSelectbox select {
        background: #12151c !important;
        border: 1px solid #1e2330 !important;
        color: #e8eaf0 !important;
        border-radius: 8px !important;
    }
    .stSlider .st-bx { background: #1e2330; }

    /* Button */
    .stButton > button {
        background: #4f9cf9;
        color: #0d0f14;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 13px;
        padding: 8px 20px;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: #6aadff;
        transform: translateY(-1px);
    }

    /* Dataframe */
    .stDataFrame { border: 1px solid #1e2330; border-radius: 10px; overflow: hidden; }

    /* Logo */
    .logo {
        font-size: 22px;
        font-weight: 700;
        color: #4f9cf9;
        letter-spacing: -0.5px;
    }
    .logo-sub { font-size: 11px; color: #5a6680; letter-spacing: 0.08em; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# ─── File paths ───────────────────────────────────────────────────────────────
DATA_DIR     = "fitness_data"
PROFILE_FILE = os.path.join(DATA_DIR, "profile.json")
LOG_FILE     = os.path.join(DATA_DIR, "daily_log.csv")
STRENGTH_FILE= os.path.join(DATA_DIR, "strength_log.csv")

os.makedirs(DATA_DIR, exist_ok=True)


# ══════════════════════════════════════════════════════════════════════════════
# DATA HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def load_profile():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_profile(data: dict):
    with open(PROFILE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_log() -> pd.DataFrame:
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE, parse_dates=["date"])
        return df
    cols = ["date","weight","calories","protein","steps","sleep","workout","alcohol","notes"]
    return pd.DataFrame(columns=cols)

def save_log(df: pd.DataFrame):
    df.to_csv(LOG_FILE, index=False)

def load_strength() -> pd.DataFrame:
    if os.path.exists(STRENGTH_FILE):
        df = pd.read_csv(STRENGTH_FILE, parse_dates=["date"])
        return df
    cols = ["date","exercise","weight_kg","reps","sets"]
    return pd.DataFrame(columns=cols)

def save_strength(df: pd.DataFrame):
    df.to_csv(STRENGTH_FILE, index=False)


# ══════════════════════════════════════════════════════════════════════════════
# FITNESS CALCULATIONS
# ══════════════════════════════════════════════════════════════════════════════

def calc_bmr(weight_kg: float, height_cm: float, age: int, sex: str) -> float:
    """Mifflin-St Jeor equation."""
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    return base + 5 if sex == "Male" else base - 161

def calc_tdee(bmr: float, activity: str) -> float:
    multipliers = {
        "Sedentary (desk job, no exercise)":        1.2,
        "Lightly active (1–3 workouts/week)":       1.375,
        "Moderately active (3–5 workouts/week)":    1.55,
        "Very active (6–7 workouts/week)":          1.725,
        "Extremely active (athlete / 2× day)":      1.9,
    }
    return bmr * multipliers.get(activity, 1.55)

def calc_targets(tdee: float, goal: str, weight_kg: float):
    """Return calorie target and macros (g)."""
    if goal == "Fat Loss":
        calories = tdee - 400
    elif goal == "Muscle Gain":
        calories = tdee + 300
    else:  # Recomposition
        calories = tdee - 200

    protein  = round(weight_kg * 2.4)         # 2.4g/kg
    fat      = round(weight_kg * 1.0)          # 1g/kg
    carbs    = round((calories - protein * 4 - fat * 9) / 4)
    carbs    = max(carbs, 50)                  # floor
    return int(calories), protein, carbs, fat

def bmi(weight_kg: float, height_cm: float) -> float:
    h = height_cm / 100
    return round(weight_kg / h ** 2, 1)

def predict_goal(current_weight: float, target_weight: float,
                 calories: float, tdee: float) -> int:
    """Estimate weeks to reach target weight."""
    delta_kcal = tdee - calories          # weekly deficit/surplus per day
    weekly_kg  = (delta_kcal * 7) / 7700  # 7700 kcal ≈ 1 kg of body mass
    if abs(weekly_kg) < 0.01:
        return 999
    weeks = abs((target_weight - current_weight) / weekly_kg)
    return int(math.ceil(weeks))

def consistency_score(log_df: pd.DataFrame, days: int = 30) -> float:
    """Workout consistency % over last N days."""
    if log_df.empty:
        return 0.0
    cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)
    recent = log_df[log_df["date"] >= cutoff]
    if recent.empty:
        return 0.0
    return round(recent["workout"].sum() / len(recent) * 100, 1)


# ══════════════════════════════════════════════════════════════════════════════
# WORKOUT GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

WORKOUT_LIBRARY = {
    "Push – Chest & Triceps": [
        {"name": "Barbell Bench Press",      "sets": 4, "reps": "6–8",  "rest": "90s", "physique": "Chest mass"},
        {"name": "Incline DB Press",          "sets": 3, "reps": "8–10", "rest": "75s", "physique": "Upper chest"},
        {"name": "Cable Fly",                 "sets": 3, "reps": "12–15","rest": "60s", "physique": "Chest definition"},
        {"name": "Overhead Tricep Extension", "sets": 3, "reps": "10–12","rest": "60s", "physique": "Tricep long head"},
        {"name": "Cable Pushdown (rope)",     "sets": 3, "reps": "12–15","rest": "60s", "physique": "Arm definition"},
    ],
    "Pull – Back & Biceps": [
        {"name": "Weighted Pull-up / Lat Pulldown","sets": 4, "reps": "6–8",  "rest": "90s", "physique": "V-taper width"},
        {"name": "Barbell Row",               "sets": 4, "reps": "8–10", "rest": "75s", "physique": "Back thickness"},
        {"name": "Seated Cable Row",          "sets": 3, "reps": "10–12","rest": "60s", "physique": "Mid-back detail"},
        {"name": "Face Pull",                 "sets": 3, "reps": "15–20","rest": "45s", "physique": "Rear delts / posture"},
        {"name": "Barbell Curl",              "sets": 3, "reps": "10–12","rest": "60s", "physique": "Bicep peak"},
        {"name": "Hammer Curl",               "sets": 3, "reps": "12–15","rest": "60s", "physique": "Forearm / brachialis"},
    ],
    "Legs – Quad Dominant": [
        {"name": "Barbell Back Squat",        "sets": 4, "reps": "6–8",  "rest": "120s","physique": "Overall legs"},
        {"name": "Leg Press",                 "sets": 3, "reps": "10–12","rest": "90s", "physique": "Quad volume"},
        {"name": "Leg Extension",             "sets": 3, "reps": "12–15","rest": "60s", "physique": "Quad sweep"},
        {"name": "Romanian Deadlift",         "sets": 3, "reps": "10–12","rest": "90s", "physique": "Hamstring length"},
        {"name": "Leg Curl",                  "sets": 3, "reps": "12–15","rest": "60s", "physique": "Hamstring detail"},
        {"name": "Standing Calf Raise",       "sets": 4, "reps": "15–20","rest": "60s", "physique": "Calf shape"},
    ],
    "Shoulders & Arms": [
        {"name": "Seated DB Overhead Press",  "sets": 4, "reps": "8–10", "rest": "90s", "physique": "Shoulder mass"},
        {"name": "Lateral Raise",             "sets": 4, "reps": "15–20","rest": "45s", "physique": "Width / V-taper"},
        {"name": "Rear Delt Fly",             "sets": 3, "reps": "15–20","rest": "45s", "physique": "3D roundness"},
        {"name": "Incline DB Curl",           "sets": 3, "reps": "12–15","rest": "60s", "physique": "Bicep stretch"},
        {"name": "EZ-Bar Curl",              "sets": 3, "reps": "10–12","rest": "60s", "physique": "Bicep peak"},
        {"name": "Skull Crusher",             "sets": 3, "reps": "10–12","rest": "60s", "physique": "Tricep mass"},
    ],
    "Posterior Chain & Core": [
        {"name": "Conventional Deadlift",     "sets": 4, "reps": "5–6",  "rest": "120s","physique": "Total posterior"},
        {"name": "Hip Thrust",                "sets": 3, "reps": "10–12","rest": "90s", "physique": "Glute shape"},
        {"name": "Leg Curl",                  "sets": 3, "reps": "12–15","rest": "60s", "physique": "Hamstring"},
        {"name": "Ab Wheel Rollout",          "sets": 3, "reps": "10–12","rest": "60s", "physique": "Deep core"},
        {"name": "Cable Crunch",              "sets": 3, "reps": "15–20","rest": "45s", "physique": "Rectus abdominis"},
        {"name": "Hanging Leg Raise",         "sets": 3, "reps": "12–15","rest": "45s", "physique": "Lower abs"},
    ],
    "Full Body (3-day)": [
        {"name": "Squat",                     "sets": 3, "reps": "6–8",  "rest": "90s", "physique": "Overall legs"},
        {"name": "Bench Press",               "sets": 3, "reps": "6–8",  "rest": "90s", "physique": "Chest / triceps"},
        {"name": "Bent-over Row",             "sets": 3, "reps": "8–10", "rest": "90s", "physique": "Back / biceps"},
        {"name": "Overhead Press",            "sets": 3, "reps": "8–10", "rest": "75s", "physique": "Shoulders"},
        {"name": "Romanian Deadlift",         "sets": 3, "reps": "10–12","rest": "75s", "physique": "Posterior"},
        {"name": "Plank",                     "sets": 3, "reps": "45s",  "rest": "45s", "physique": "Core stability"},
    ],
}

SPLITS = {
    3: [
        ("Monday",    "Full Body (3-day)"),
        ("Wednesday", "Full Body (3-day)"),
        ("Friday",    "Full Body (3-day)"),
    ],
    4: [
        ("Monday",    "Push – Chest & Triceps"),
        ("Tuesday",   "Pull – Back & Biceps"),
        ("Thursday",  "Legs – Quad Dominant"),
        ("Friday",    "Shoulders & Arms"),
    ],
    5: [
        ("Monday",    "Push – Chest & Triceps"),
        ("Tuesday",   "Pull – Back & Biceps"),
        ("Wednesday", "Legs – Quad Dominant"),
        ("Thursday",  "Shoulders & Arms"),
        ("Friday",    "Posterior Chain & Core"),
    ],
}

DAY_COLORS = {
    "Push – Chest & Triceps":     "#f87171",
    "Pull – Back & Biceps":       "#60a5fa",
    "Legs – Quad Dominant":       "#34d399",
    "Shoulders & Arms":           "#a78bfa",
    "Posterior Chain & Core":     "#fbbf24",
    "Full Body (3-day)":          "#fb923c",
}


# ══════════════════════════════════════════════════════════════════════════════
# CHART HELPERS
# ══════════════════════════════════════════════════════════════════════════════

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#8892a4", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(gridcolor="#1e2330", zerolinecolor="#1e2330", tickfont=dict(size=11)),
    yaxis=dict(gridcolor="#1e2330", zerolinecolor="#1e2330", tickfont=dict(size=11)),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
)

def make_chart(**kwargs) -> dict:
    layout = {**CHART_LAYOUT, **kwargs}
    return layout

def weight_chart(log_df: pd.DataFrame, target_weight: float = None):
    df = log_df.dropna(subset=["weight"]).sort_values("date")
    if df.empty:
        return None

    fig = go.Figure()

    # 7-day rolling average
    if len(df) >= 3:
        df["rolling"] = df["weight"].rolling(7, min_periods=1).mean()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["rolling"],
            name="7-day avg", mode="lines",
            line=dict(color="#4f9cf9", width=2.5),
        ))

    # Raw daily weight
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["weight"],
        name="Daily weight", mode="markers",
        marker=dict(color="#4f9cf9", size=6, opacity=0.4),
    ))

    if target_weight:
        fig.add_hline(
            y=target_weight, line_dash="dash",
            line_color="#34d399", opacity=0.6,
            annotation_text=f"Target {target_weight} kg",
            annotation_font_color="#34d399",
        )

    fig.update_layout(**make_chart(title="Weight trend (kg)"), height=300)
    return fig

def calories_chart(log_df: pd.DataFrame, target_cal: int):
    df = log_df.dropna(subset=["calories"]).sort_values("date").tail(30)
    if df.empty:
        return None

    colors = ["#34d399" if v <= target_cal * 1.05 else "#f87171" for v in df["calories"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["date"], y=df["calories"],
        name="Calories eaten",
        marker_color=colors, opacity=0.8,
    ))
    fig.add_hline(
        y=target_cal, line_dash="dash",
        line_color="#fbbf24", opacity=0.8,
        annotation_text=f"Target {target_cal} kcal",
        annotation_font_color="#fbbf24",
    )
    fig.update_layout(**make_chart(title="Calories vs target (last 30 days)"), height=280)
    return fig

def sleep_steps_chart(log_df: pd.DataFrame):
    df = log_df.sort_values("date").tail(30)
    if df.empty:
        return None

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=df["date"], y=df["sleep"],
        name="Sleep (h)", marker_color="#a78bfa", opacity=0.7,
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["steps"],
        name="Steps", mode="lines+markers",
        line=dict(color="#34d399", width=2),
        marker=dict(size=4),
    ), secondary_y=True)
    fig.update_layout(**make_chart(title="Sleep & steps (last 30 days)"), height=280)
    fig.update_yaxes(title_text="Hours", secondary_y=False,
                     gridcolor="#1e2330", tickfont=dict(size=11), title_font=dict(size=11))
    fig.update_yaxes(title_text="Steps", secondary_y=True,
                     gridcolor="rgba(0,0,0,0)", tickfont=dict(size=11), title_font=dict(size=11))
    return fig

def strength_chart(strength_df: pd.DataFrame, exercise: str):
    df = strength_df[strength_df["exercise"] == exercise].sort_values("date")
    if df.empty:
        return None
    df["volume"] = df["weight_kg"] * df["reps"] * df["sets"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["weight_kg"],
        name="Weight (kg)", mode="lines+markers",
        line=dict(color="#4f9cf9", width=2.5),
        marker=dict(size=7),
    ))
    fig.update_layout(**make_chart(title=f"{exercise} — working weight (kg)"), height=260)
    return fig

def macro_donut(protein_g: int, carbs_g: int, fat_g: int):
    labels  = ["Protein", "Carbs", "Fats"]
    values  = [protein_g * 4, carbs_g * 4, fat_g * 9]
    colors  = ["#4f9cf9", "#34d399", "#fbbf24"]
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.65,
        marker_colors=colors,
        textinfo="label+percent",
        textfont=dict(size=12, color="#e8eaf0"),
        hovertemplate="%{label}: %{value} kcal<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=220,
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# BEHAVIOR ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

def analyze_behavior(log_df: pd.DataFrame, target_cal: int, target_sleep: float = 7.5):
    insights = []
    if log_df.empty or len(log_df) < 5:
        insights.append(("info", "Log at least 5 days of data to unlock behavior insights."))
        return insights

    recent = log_df.tail(14)

    # Sleep
    avg_sleep = recent["sleep"].dropna().mean()
    if avg_sleep < 6.5:
        insights.append(("bad",
            f"⚠️ Your average sleep is {avg_sleep:.1f}h — critically low. "
            "GH release during deep sleep is cut by up to 60%, directly reducing muscle gains and fat loss."))
    elif avg_sleep < target_sleep:
        insights.append(("warn",
            f"⚠️ Average sleep is {avg_sleep:.1f}h. Aim for 7.5–8.5h. "
            "Even 30 extra minutes improves recovery measurably."))
    else:
        insights.append(("good",
            f"✅ Sleep is solid at {avg_sleep:.1f}h average. Keep it up."))

    # Alcohol vs weight
    if "alcohol" in recent.columns and recent["alcohol"].sum() > 0:
        alcohol_days = recent[recent["alcohol"] > 0]
        if len(alcohol_days) >= 2:
            insights.append(("warn",
                f"⚠️ You drank on {len(alcohol_days)} of the last 14 days. "
                "Alcohol blunts protein synthesis for 24–48h and disrupts sleep quality."))

    # Calorie consistency
    if "calories" in recent.columns:
        cal_data = recent["calories"].dropna()
        if len(cal_data) > 3:
            avg_cal = cal_data.mean()
            over_days = (cal_data > target_cal * 1.1).sum()
            under_days = (cal_data < target_cal * 0.85).sum()
            if over_days > 3:
                insights.append(("warn",
                    f"⚠️ You exceeded your calorie target by 10%+ on {over_days} of the last {len(cal_data)} logged days. "
                    "This can stall fat loss even with consistent training."))
            elif under_days > 4:
                insights.append(("warn",
                    f"⚠️ You ate significantly under target on {under_days} days. "
                    "Severe under-eating increases muscle loss risk on a recomposition."))
            else:
                insights.append(("good",
                    f"✅ Calorie consistency is good — averaging {int(avg_cal)} kcal (target: {target_cal})."))

    # Workout consistency
    w_days = recent["workout"].sum()
    total  = len(recent)
    pct    = w_days / total * 100
    if pct < 50:
        insights.append(("bad",
            f"⚠️ Workout consistency is only {pct:.0f}% over the last 14 days. "
            "At this rate, progressive overload breaks down. Aim for ≥80%."))
    elif pct < 75:
        insights.append(("warn",
            f"📊 Workout consistency: {pct:.0f}%. Good, but there's room to improve. Target ≥80%."))
    else:
        insights.append(("good",
            f"✅ Workout consistency: {pct:.0f}% — excellent discipline."))

    # Auto-calorie adjustment: weight stall check
    if "weight" in log_df.columns and len(log_df) >= 21:
        w_data = log_df["weight"].dropna()
        if len(w_data) >= 14:
            early = w_data.iloc[:7].mean()
            late  = w_data.iloc[-7:].mean()
            diff  = late - early
            if abs(diff) < 0.3:
                insights.append(("info",
                    "📌 Auto-adjust: your weight has barely moved in 3+ weeks. "
                    "Try reducing carbs by 50g/day OR adding 20 min of LISS cardio 3×/week."))
            elif diff < -1.5:
                insights.append(("warn",
                    f"⚠️ Auto-adjust: you've lost {abs(diff):.1f} kg in the past 3 weeks — faster than ideal. "
                    "Add 150 kcal/day (carbs) to preserve muscle."))

    # Steps
    avg_steps = recent["steps"].dropna().mean()
    if avg_steps < 6000:
        insights.append(("warn",
            f"⚠️ Average daily steps: {int(avg_steps):,}. NEAT (non-exercise activity) "
            "is a major fat-loss lever. Aim for 8,000–10,000 steps."))
    elif avg_steps >= 8000:
        insights.append(("good", f"✅ Great step count — {int(avg_steps):,}/day on average."))

    return insights


# ══════════════════════════════════════════════════════════════════════════════
# UI COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════

def metric_card(label: str, value: str, sub: str = "", color_class: str = "metric-accent"):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value <{color_class}">{value}</div>
        {'<div class="metric-sub">' + sub + '</div>' if sub else ''}
    </div>
    """, unsafe_allow_html=True)

def render_insight(kind: str, text: str):
    css = f"insight-{kind}"
    st.markdown(f'<div class="insight-box {css}">{text}</div>', unsafe_allow_html=True)

def render_exercise(ex: dict, day_color: str):
    st.markdown(f"""
    <div class="exercise-card">
        <div>
            <div class="exercise-name">{ex["name"]}</div>
            <div class="exercise-detail">{ex["sets"]} sets · {ex["reps"]} reps · rest {ex["rest"]}</div>
        </div>
        <span class="exercise-badge" style="background:{day_color}22; color:{day_color}; border: 1px solid {day_color}44">
            {ex["physique"]}
        </span>
    </div>
    """, unsafe_allow_html=True)

def progress_bar(label: str, value: float, total: float, color: str = "#4f9cf9"):
    pct = min(value / total * 100, 100) if total else 0
    st.markdown(f"""
    <div style="margin-bottom:10px">
        <div style="display:flex;justify-content:space-between;font-size:12px;color:#8892a4;margin-bottom:4px">
            <span>{label}</span>
            <span>{value:.0f} / {total:.0f}</span>
        </div>
        <div class="progress-bar-container">
            <div class="progress-bar-fill" style="width:{pct:.1f}%;background:{color}"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — USER PROFILE
# ══════════════════════════════════════════════════════════════════════════════

def render_sidebar() -> dict:
    profile = load_profile()

    st.sidebar.markdown('<div class="logo">⚡ FitOS</div><div class="logo-sub">Fitness Operating System</div>', unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Profile**")

    sex    = st.sidebar.selectbox("Sex", ["Male", "Female"], index=0 if profile.get("sex","Male")=="Male" else 1)
    age    = st.sidebar.number_input("Age", 15, 80, profile.get("age", 25))
    height = st.sidebar.number_input("Height (cm)", 140, 220, profile.get("height", 175))
    weight = st.sidebar.number_input("Current weight (kg)", 35.0, 200.0, float(profile.get("weight", 70.0)), step=0.1)
    bf     = st.sidebar.number_input("Body fat % (est.)", 5.0, 50.0, float(profile.get("bf", 18.0)), step=0.5)

    st.sidebar.markdown("**Goals**")
    goal   = st.sidebar.selectbox("Goal", ["Recomposition","Fat Loss","Muscle Gain"],
                                  index=["Recomposition","Fat Loss","Muscle Gain"].index(profile.get("goal","Recomposition")))
    target_w = st.sidebar.number_input("Target weight (kg)", 35.0, 200.0, float(profile.get("target_weight", weight)), step=0.1)
    days   = st.sidebar.selectbox("Training days/week", [3,4,5], index=[3,4,5].index(profile.get("days",5)))

    st.sidebar.markdown("**Activity**")
    activity_opts = [
        "Sedentary (desk job, no exercise)",
        "Lightly active (1–3 workouts/week)",
        "Moderately active (3–5 workouts/week)",
        "Very active (6–7 workouts/week)",
        "Extremely active (athlete / 2× day)",
    ]
    activity = st.sidebar.selectbox("Activity level", activity_opts,
        index=activity_opts.index(profile.get("activity", activity_opts[2])))

    if st.sidebar.button("💾  Save profile"):
        data = dict(sex=sex, age=age, height=height, weight=weight, bf=bf,
                    goal=goal, target_weight=target_w, days=days, activity=activity)
        save_profile(data)
        st.sidebar.success("Profile saved!")

    return dict(sex=sex, age=age, height=height, weight=weight, bf=bf,
                goal=goal, target_weight=target_w, days=days, activity=activity)


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════

def tab_dashboard(p: dict, bmr: float, tdee: float, calories: int,
                  protein: int, carbs: int, fat: int, log_df: pd.DataFrame):
    """Overview metrics + quick charts."""

    weeks_to_goal = predict_goal(p["weight"], p["target_weight"], calories, tdee)
    cons          = consistency_score(log_df)
    lean_mass     = p["weight"] * (1 - p["bf"] / 100)

    # ── KPI row ──────────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("BMR", f"{int(bmr):,} kcal", help="Basal metabolic rate")
    with c2:
        st.metric("TDEE", f"{int(tdee):,} kcal", help="Total daily energy expenditure")
    with c3:
        st.metric("Calorie target", f"{calories:,} kcal")
    with c4:
        st.metric("BMI", bmi(p["weight"], p["height"]))
    with c5:
        st.metric("Lean mass", f"{lean_mass:.1f} kg")

    st.markdown('<div class="section-title">Progress overview</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns([2, 1])

    with col_a:
        fig = weight_chart(log_df, p["target_weight"])
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Start logging your weight to see the trend chart.")

    with col_b:
        st.markdown('<div class="section-title">Goal prediction</div>', unsafe_allow_html=True)
        delta = round(p["target_weight"] - p["weight"], 1)
        direction = "lose" if delta < 0 else "gain"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Time to goal</div>
            <div class="metric-value">{weeks_to_goal if weeks_to_goal < 200 else '—'} <span style="font-size:16px;color:#8892a4">weeks</span></div>
            <div class="metric-sub">Need to {direction} {abs(delta):.1f} kg</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Workout consistency</div>
            <div class="metric-value" style="color:{'#34d399' if cons>=80 else '#fbbf24' if cons>=60 else '#f87171'}">{cons}%</div>
            <div class="metric-sub">Last 30 days</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Calories chart ────────────────────────────────────────────────────────
    if not log_df.empty and "calories" in log_df.columns:
        st.markdown('<div class="section-title">Calorie log</div>', unsafe_allow_html=True)
        fig2 = calories_chart(log_df, calories)
        if fig2:
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # ── Weekly check-in ───────────────────────────────────────────────────────
    if len(log_df) >= 7:
        st.markdown('<div class="section-title">Weekly check-in summary</div>', unsafe_allow_html=True)
        last7 = log_df.tail(7)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Avg weight", f"{last7['weight'].dropna().mean():.1f} kg")
        with c2:
            st.metric("Avg calories", f"{int(last7['calories'].dropna().mean()):,}")
        with c3:
            st.metric("Avg sleep", f"{last7['sleep'].dropna().mean():.1f} h")
        with c4:
            workouts = int(last7["workout"].sum())
            st.metric("Workouts done", f"{workouts} / 7")


def tab_workout(p: dict):
    """Weekly training plan."""
    days = p["days"]
    split = SPLITS.get(days, SPLITS[5])

    st.markdown(f'<div class="section-title">{days}-day training split</div>', unsafe_allow_html=True)
    st.markdown(
        "**Progression rule:** Hit the top of your rep range on all sets for 2 consecutive sessions "
        "→ add the smallest weight increment. Reset to bottom of range and repeat.",
        unsafe_allow_html=False,
    )

    for day_name, session_name in split:
        color = DAY_COLORS.get(session_name, "#4f9cf9")
        st.markdown(
            f'<div class="day-header" style="color:{color}">📅 {day_name} — {session_name}</div>',
            unsafe_allow_html=True,
        )
        exercises = WORKOUT_LIBRARY.get(session_name, [])
        for ex in exercises:
            render_exercise(ex, color)

    # Rest days
    all_days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    scheduled = [d for d, _ in split]
    rest_days  = [d for d in all_days if d not in scheduled]
    if rest_days:
        st.markdown(
            f'<div class="day-header" style="color:#5a6680">🛌 Rest days — {", ".join(rest_days)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="insight-box insight-info">Active recovery: 30–40 min incline walk or light cycling. '
            'Hit 8,000+ steps. Mobility work is encouraged.</div>',
            unsafe_allow_html=True,
        )

    # Strength log section
    st.markdown('<div class="section-title">Log a lift</div>', unsafe_allow_html=True)
    strength_df = load_strength()

    key_lifts = ["Barbell Bench Press","Barbell Back Squat","Conventional Deadlift",
                 "Weighted Pull-up / Lat Pulldown","Seated DB Overhead Press","Barbell Row"]

    with st.form("strength_form"):
        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            s_exercise = st.selectbox("Exercise", key_lifts)
        with sc2:
            s_weight = st.number_input("Weight (kg)", 0.0, 500.0, 60.0, step=1.25)
        with sc3:
            s_reps = st.number_input("Reps", 1, 30, 6)
        with sc4:
            s_sets = st.number_input("Sets", 1, 10, 4)

        if st.form_submit_button("Log lift"):
            new_row = pd.DataFrame([{
                "date": pd.Timestamp.now().normalize(),
                "exercise": s_exercise,
                "weight_kg": s_weight,
                "reps": s_reps,
                "sets": s_sets,
            }])
            strength_df = pd.concat([strength_df, new_row], ignore_index=True)
            save_strength(strength_df)
            st.success(f"Logged {s_weight}kg × {s_reps} reps on {s_exercise}!")

    if not strength_df.empty:
        st.markdown('<div class="section-title">Strength progress</div>', unsafe_allow_html=True)
        sel = st.selectbox("Select lift to view", strength_df["exercise"].unique())
        fig = strength_chart(strength_df, sel)
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def tab_nutrition(p: dict, calories: int, protein: int, carbs: int, fat: int, log_df: pd.DataFrame):
    """Nutrition targets and today's progress."""
    st.markdown('<div class="section-title">Daily targets</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        fig = macro_donut(protein, carbs, fat)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        st.markdown("&nbsp;", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Calories", f"{calories:,}")
        c2.metric("Protein", f"{protein}g", help="2.4g per kg bodyweight")
        c3.metric("Carbs",   f"{carbs}g")
        c4.metric("Fats",    f"{fat}g")

        progress_bar("Protein", protein, protein, "#4f9cf9")
        progress_bar("Carbs",   carbs,   carbs,   "#34d399")
        progress_bar("Fats",    fat,     fat,     "#fbbf24")

    # Meal timing guide
    st.markdown('<div class="section-title">Meal timing guide</div>', unsafe_allow_html=True)
    meals = [
        ("Breakfast",        "Within 60 min of waking",    "Protein + carbs",             "~450 kcal",  "Eggs, oats, Greek yogurt"),
        ("Pre-workout",      "60–90 min before training",   "Carbs + moderate protein",    "~400 kcal",  "Rice, chicken, banana"),
        ("Post-workout",     "Within 60 min after training","Fast protein + carbs",         "~450 kcal",  "Shake, fruit, white rice"),
        ("Dinner",           "Evening",                     "Protein + veg + fats",        "~550 kcal",  "Fish, steak, olive oil, salad"),
        ("Pre-bed (opt.)",   "30 min before sleep",         "Slow-digesting protein",      "~200 kcal",  "Cottage cheese, casein shake"),
    ]
    meal_df = pd.DataFrame(meals, columns=["Meal","Timing","Focus","~Calories","Examples"])
    st.dataframe(meal_df, use_container_width=True, hide_index=True)

    # Rest day adjustment
    st.markdown('<div class="section-title">Rest day adjustment</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="insight-box insight-info">On rest days, reduce carbs by ~50g (−200 kcal) → '
        f'target ~{calories-200:,} kcal. Shift 10–15g toward healthy fats. '
        f'Protein stays at {protein}g every day.</div>',
        unsafe_allow_html=True,
    )

    # Calorie trend vs target
    if not log_df.empty and "calories" in log_df.columns:
        fig2 = calories_chart(log_df, calories)
        if fig2:
            st.markdown('<div class="section-title">Calorie trend</div>', unsafe_allow_html=True)
            st.plotly_chart(
                fig2,
    use_container_width=True,
    config={"displayModeBar": False},
    key="nutrition_chart"
)


def tab_log(calories: int, protein: int, log_df: pd.DataFrame):
    """Daily logging form + recent history."""
    st.markdown('<div class="section-title">Log today</div>', unsafe_allow_html=True)

    with st.form("daily_log_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            log_date   = st.date_input("Date", value=date.today())
            log_weight = st.number_input("Body weight (kg)", 30.0, 200.0, 70.0, step=0.1)
            log_sleep  = st.number_input("Sleep hours", 0.0, 14.0, 7.0, step=0.25)
        with c2:
            log_cal    = st.number_input("Calories eaten", 0, 8000, calories)
            log_prot   = st.number_input("Protein (g)", 0, 400, protein)
            log_steps  = st.number_input("Steps", 0, 50000, 8000, step=100)
        with c3:
            log_workout= st.checkbox("Workout completed ✓", value=True)
            log_alcohol= st.number_input("Alcohol (units, 0 = none)", 0, 20, 0)
            log_notes  = st.text_area("Notes (optional)", height=88)

        submitted = st.form_submit_button("📝  Save today's log")

    if submitted:
        new_entry = pd.DataFrame([{
            "date":     pd.Timestamp(log_date),
            "weight":   log_weight,
            "calories": log_cal,
            "protein":  log_prot,
            "steps":    log_steps,
            "sleep":    log_sleep,
            "workout":  int(log_workout),
            "alcohol":  log_alcohol,
            "notes":    log_notes,
        }])
        # Remove duplicate date entry if exists
        existing = log_df[log_df["date"] != pd.Timestamp(log_date)]
        log_df = pd.concat([existing, new_entry], ignore_index=True).sort_values("date")
        save_log(log_df)
        st.success("Logged! Great job tracking.")
        st.rerun()

    # Recent log table
    if not log_df.empty:
        st.markdown('<div class="section-title">Recent log (last 14 days)</div>', unsafe_allow_html=True)
        show = log_df.sort_values("date", ascending=False).head(14).copy()
        show["date"]    = show["date"].dt.strftime("%d %b")
        show["workout"] = show["workout"].map({1: "✅", 0: "❌"})
        show["alcohol"] = show["alcohol"].apply(lambda x: f"{int(x)} units" if x > 0 else "—")
        st.dataframe(show.rename(columns={
            "date":"Date","weight":"Weight (kg)","calories":"Calories",
            "protein":"Protein (g)","steps":"Steps","sleep":"Sleep (h)",
            "workout":"Workout","alcohol":"Alcohol","notes":"Notes"
        }), use_container_width=True, hide_index=True)


def tab_progress(log_df: pd.DataFrame, p: dict, target_cal: int):
    """Charts + behavior analysis + insights."""
    if log_df.empty:
        st.info("No data yet. Log a few days in the Daily Log tab to see your progress.")
        return

    # Sleep + steps chart
    st.markdown('<div class="section-title">Sleep & activity</div>', unsafe_allow_html=True)
    fig = sleep_steps_chart(log_df)
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Body recomposition estimate
    st.markdown('<div class="section-title">Body recomposition estimate</div>', unsafe_allow_html=True)
    if len(log_df) >= 14:
        early_w = log_df["weight"].dropna().iloc[:7].mean()
        late_w  = log_df["weight"].dropna().iloc[-7:].mean()
        total_weeks = max(len(log_df) / 7, 1)
        delta_w  = late_w - early_w
        # Estimate lean/fat change (simplified)
        fat_lost  = round(delta_w * -0.7, 2) if delta_w < 0 else 0
        fat_gained= round(delta_w * 0.3, 2)  if delta_w > 0 else 0
        c1, c2, c3 = st.columns(3)
        c1.metric("Weight change",  f"{delta_w:+.1f} kg", f"over ~{int(total_weeks)} weeks")
        c2.metric("Est. fat change", f"{fat_lost:+.2f} kg", help="Simplified estimate")
        c3.metric("Weekly rate",    f"{delta_w/total_weeks:+.2f} kg/wk")
    else:
        st.info("Need 14+ days of weight data for recomposition estimates.")

    # Behavior insights
    st.markdown('<div class="section-title">Behavior analysis & auto-insights</div>', unsafe_allow_html=True)
    insights = analyze_behavior(log_df, target_cal)
    for kind, text in insights:
        render_insight(kind, text)

    # Workout streak
    st.markdown('<div class="section-title">Adaptive rules reminder</div>', unsafe_allow_html=True)
    rules = [
        ("info",  "📈  Strength: add weight when you hit the top rep range on all sets for 2 consecutive sessions."),
        ("info",  "📉  Calories: if weight stalls for 3+ weeks, cut carbs by 50g/day OR add 20 min LISS 3×/week."),
        ("warn",  "⚠️  If losing >0.7 kg/week for 2 weeks, add 150 kcal/day to protect muscle mass."),
        ("good",  "🔄  Every 6–8 weeks: take a deload (−40% weight, −50% volume). Every 8–10 weeks: diet break at TDEE."),
    ]
    for kind, text in rules:
        render_insight(kind, text)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    profile = render_sidebar()

    # Core calculations
    bmr      = calc_bmr(profile["weight"], profile["height"], profile["age"], profile["sex"])
    tdee     = calc_tdee(bmr, profile["activity"])
    calories, protein, carbs, fat = calc_targets(tdee, profile["goal"], profile["weight"])

    # Load stored data
    log_df      = load_log()
    strength_df = load_strength()

    # Page title
    st.markdown(
        '<h1 style="font-size:26px;font-weight:600;margin-bottom:0;color:#e8eaf0">⚡ FitOS Dashboard</h1>'
        f'<p style="color:#5a6680;font-size:13px;margin-top:4px">{profile["goal"]} · {profile["days"]}-day split · {profile["sex"]}, {profile["age"]}y · {profile["weight"]} kg</p>',
        unsafe_allow_html=True,
    )

    tabs = st.tabs(["🏠  Dashboard", "💪  Workout plan", "🥗  Nutrition", "📝  Daily log", "📊  Progress"])

    with tabs[0]:
        tab_dashboard(profile, bmr, tdee, calories, protein, carbs, fat, log_df)

    with tabs[1]:
        tab_workout(profile)

    with tabs[2]:
        tab_nutrition(profile, calories, protein, carbs, fat, log_df)

    with tabs[3]:
        tab_log(calories, protein, log_df)

    with tabs[4]:
        tab_progress(log_df, profile, calories)


if __name__ == "__main__":
    main()
