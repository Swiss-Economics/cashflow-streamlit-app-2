# streamlit_app.py
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="DCF Assumptions Sandbox", layout="centered")

DISCOUNT_RATE = 0.10
LINE_COLOR = "#AF1A1D"  # RGB (175, 26, 29)

# ---------- Preset scenarios ----------
SCENARIOS = {
    "Advisor Base": [2.76, 3.15, 3.53, 3.90, 4.14],
    "Advisor Case 1": [3.85, 3.36, 3.28, 3.17, 2.98],
    "Advisor Case 2": [3.85, 3.44, 3.70, 4.01, 3.82],
    "Bank Base": [3.85, 3.61, 4.54, 5.69, 5.50],
}

years = [1, 2, 3, 4, 5]

# ---------- Scenario selection ----------
st.subheader("Cash flow inputs")

selected_scenario = st.selectbox(
    "Choose a cash flow evolution",
    options=list(SCENARIOS.keys())
)

# Track previous scenario so values only reset when scenario changes
if "previous_scenario" not in st.session_state:
    st.session_state.previous_scenario = selected_scenario

# Initialize cash flow inputs on first load
if "cf_values" not in st.session_state:
    st.session_state.cf_values = SCENARIOS[selected_scenario].copy()

# If the user changes scenario, replace all five cash flows
if selected_scenario != st.session_state.previous_scenario:
    st.session_state.cf_values = SCENARIOS[selected_scenario].copy()
    st.session_state.previous_scenario = selected_scenario

# ---------- Manual inputs ----------
col1, col2 = st.columns(2)

with col1:
    st.session_state.cf_values[0] = st.number_input(
        "Cash flow year 1 (mUSD)",
        value=float(st.session_state.cf_values[0]),
        step=1.0,
        format="%.2f"
    )
    st.session_state.cf_values[1] = st.number_input(
        "Cash flow year 2 (mUSD)",
        value=float(st.session_state.cf_values[1]),
        step=1.0,
        format="%.2f"
    )
    st.session_state.cf_values[2] = st.number_input(
        "Cash flow year 3 (mUSD)",
        value=float(st.session_state.cf_values[2]),
        step=1.0,
        format="%.2f"
    )

with col2:
    st.session_state.cf_values[3] = st.number_input(
        "Cash flow year 4 (mUSD)",
        value=float(st.session_state.cf_values[3]),
        step=1.0,
        format="%.2f"
    )
    st.session_state.cf_values[4] = st.number_input(
        "Cash flow year 5 (mUSD)",
        value=float(st.session_state.cf_values[4]),
        step=1.0,
        format="%.2f"
    )

cash_flows = st.session_state.cf_values

# ---------- Data ----------
df = pd.DataFrame(
    {
        "Year": years,
        "Cash flow": cash_flows,
    }
)

# ---------- Chart ----------
st.subheader("Cash flow profile")

line = (
    alt.Chart(df)
    .mark_line(point=True, strokeWidth=3, color=LINE_COLOR)
    .encode(
        x=alt.X("Year:O", title="Year", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Cash flow:Q", title="Cash flow (mUSD)"),
        tooltip=[
            alt.Tooltip("Year:O", title="Year"),
            alt.Tooltip("Cash flow:Q", title="Cash flow (mUSD)", format=",.2f"),
        ],
    )
)

st.altair_chart(line, use_container_width=True)

# ---------- Valuation ----------
present_values = [
    cf / ((1 + DISCOUNT_RATE) ** (year - 1))
    for cf, year in zip(cash_flows, years)
]

valuation = sum(present_values)

st.subheader("Valuation")
st.metric("Valuation", f"USD {valuation:,.0f}m")