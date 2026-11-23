from pathlib import Path

import pandas as pd
import streamlit as st

from model.portfolio import (
    EQUAL_WEIGHT_WEIGHTS,
    PROPOSED_WEIGHTS,
    SIXTY_FORTY_WEIGHTS,
    evaluate_portfolio,
    stress_table,
)


ROOT = Path(__file__).parent
st.set_page_config(page_title="Project 2 | Conservative ETF Mandate", layout="wide")


@st.cache_data
def load_inputs():
    return pd.read_csv(ROOT / "data" / "point_in_time_inputs.csv")


def percent(value):
    return f"{value:.2%}"


def show_portfolio(name, result):
    with st.container(border=True):
        st.subheader(name)
        st.metric("Mandate verdict", result["verdict"])
        first, second, third = st.columns(3)
        first.metric("Net expected return", percent(result["net_return"]))
        second.metric("Annualized volatility", percent(result["volatility"]))
        third.metric("Largest ETF weight", percent(result["largest_weight"]))
        st.caption("Failed rule(s): " + ("; ".join(result["failures"]) if result["failures"] else "None"))
        st.dataframe(
            result["holdings"][["ticker", "name", "asset_class", "weight"]].assign(
                weight=lambda frame: frame["weight"].map(percent)
            ),
            hide_index=True,
            use_container_width=True,
        )


inputs = load_inputs()
st.title("Conservative U.S. ETF Mandate")
st.caption("As-of data fixture: 2025-12-31 | Education only — not investment advice.")

with st.sidebar:
    st.header("Committee controls")
    max_position = st.slider("Maximum single ETF weight", min_value=0.20, max_value=0.60, value=0.35, step=0.05)
    trading_cost = st.slider("Trading cost (basis points)", min_value=0, max_value=75, value=10, step=5)
    st.info("Move the maximum single ETF weight to 30% to test the proposed portfolio's mandate verdict.")

st.markdown("""
**Mandate:** Seek a lower-volatility U.S. equity sleeve with Treasury ballast. The eligible universe is six liquid U.S.-listed equity-factor and Treasury ETFs. Benchmark: 60% SPY / 40% IEF. Limits: at least 60% equity, at least 20% fixed income, no ETF above the selected position limit, and annualized volatility at or below 12%.
""")

proposed = evaluate_portfolio(inputs, PROPOSED_WEIGHTS, max_position, trading_cost)
equal_weight = evaluate_portfolio(inputs, EQUAL_WEIGHT_WEIGHTS, max_position, trading_cost)
sixty_forty = evaluate_portfolio(inputs, SIXTY_FORTY_WEIGHTS, max_position, trading_cost)

st.header("Baseline comparison and mandate verdict")
col1, col2, col3 = st.columns(3)
with col1:
    show_portfolio("Constrained defensive-factor portfolio", proposed)
with col2:
    show_portfolio("Equal-weight baseline", equal_weight)
with col3:
    show_portfolio("Transparent 60/40 baseline", sixty_forty)

st.header("Point-in-time signal and data card")
st.write("Signal rule: a positive trailing-12-month return supports eligibility; Treasury holdings are classified as defensive ballast. The stress run also checks a six-month signal window.")
st.dataframe(
    inputs[["ticker", "name", "asset_class", "trailing_12m_return", "trailing_6m_return", "signal", "as_of", "source_note"]].assign(
        trailing_12m_return=lambda frame: frame["trailing_12m_return"].map(percent)
    ).assign(
        trailing_6m_return=lambda frame: frame["trailing_6m_return"].map(percent)
    ),
    hide_index=True,
    use_container_width=True,
)

st.header("Stress run")
st.caption("The process stops or pauses if a mandate rule fails, net expected return falls below the compliant equal-weight baseline after costs, or a proposed equity ETF loses positive eligibility at the scheduled signal-window review.")
stress = stress_table(inputs, max_position)
st.dataframe(
    stress.assign(
        **{
            "Net expected return": stress["Net expected return"].map(percent),
            "Volatility": stress["Volatility"].map(percent),
        }
    ),
    hide_index=True,
    use_container_width=True,
)

st.header("Committee recommendation")
if proposed["verdict"] == "PASS" and proposed["net_return"] >= equal_weight["net_return"]:
    st.success("PILOT at a 10%–20% sleeve allocation. Monitor the mandate limits, net expected-return advantage over equal weight, and factor-signal deterioration.")
else:
    st.error("REJECT OR PAUSE until the mandate failure is resolved. A passing mandate verdict and net expected return at least equal to the compliant equal-weight baseline are required to proceed.")

st.caption("AI use: Codex scaffolded this classroom app. The student must verify all assumptions, sources, calculations, and decision statements.")
