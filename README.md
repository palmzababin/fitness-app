# ⚡ FitOS — Fitness Operating System

A complete fitness tracking and planning app built with Streamlit.

## Features
- BMR & TDEE calculator (Mifflin-St Jeor)
- 3/4/5-day workout split generator with progression logic
- Daily log: weight, calories, protein, steps, sleep, alcohol, workouts
- Progress charts: weight trend, calories vs target, strength over time, sleep & steps
- Behavior analysis: auto-insights and calorie auto-adjustment alerts
- Goal prediction: estimated weeks to reach target weight
- Body recomposition estimation
- Weekly check-in summary
- Data saved locally in CSV / JSON (no account needed)

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

The app opens at http://localhost:8501

## Data storage
All data is saved to a `fitness_data/` folder in the same directory:
- `fitness_data/profile.json` — your profile settings
- `fitness_data/daily_log.csv` — daily tracking entries
- `fitness_data/strength_log.csv` — lift history

## Tabs
| Tab | What it does |
|-----|-------------|
| Dashboard | KPI metrics, weight trend, weekly check-in |
| Workout plan | Full weekly split + strength logger |
| Nutrition | Macros, meal timing, calorie trend |
| Daily log | Log today's data |
| Progress | Sleep/steps charts, behavior insights, adaptive rules |
