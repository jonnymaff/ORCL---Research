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
st.set_page_config(
    page_title="Committee Dashboard | Conservative ETF Mandate",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_inputs():
    return pd.read_csv(ROOT / "data" / "point_in_time_inputs.csv")


def percent(value):
    return f"{value:.2%}"


def verdict_badge(result):
    if result["verdict"] == "PASS":
        return "<span class='verdict pass'>PASS</span>"
    return "<span class='verdict fail'>FAIL</span>"


def portfolio_summary(name, subtitle, result):
    with st.container(border=True):
        st.markdown(f"<div class='portfolio-label'>{subtitle}</div><h3>{name}</h3>", unsafe_allow_html=True)
        st.markdown(verdict_badge(result), unsafe_allow_html=True)
        first, second = st.columns(2)
        first.metric("Net expected return", percent(result["net_return"]))
        second.metric("Annualized volatility", percent(result["volatility"]))
        st.metric("Largest position", percent(result["largest_weight"]))
        if result["failures"]:
            st.error("Failed rule: " + "; ".join(result["failures"]))
        else:
            st.success("All mandate rules pass.")


def formatted_holdings(result):
    return result["holdings"][["ticker", "name", "asset_class", "weight"]].assign(
        weight=lambda frame: frame["weight"].map(percent)
    )


st.markdown(
    """
    <style>
    .stApp { background: #f7f9fc; color: #152536; }
    [data-testid="stSidebar"] { background: #102b46; }
    [data-testid="stSidebar"] * { color: #f7fbff; }
    [data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div { color: #f7fbff; }
    .block-container { max-width: 1420px; padding-top: 2rem; padding-bottom: 3rem; }
    .hero { background: linear-gradient(120deg, #102b46 0%, #1f5d7a 100%); border-radius: 18px; color: white; padding: 2.2rem 2.4rem; margin-bottom: 1.25rem; box-shadow: 0 8px 24px rgba(16,43,70,.18); }
    .hero h1 { color: white; font-size: 2.25rem; margin: 0 0 .3rem 0; }
    .hero p { color: #dcecf5; font-size: 1.05rem; margin: 0; }
    .eyebrow, .portfolio-label { color: #56758b; font-size: .76rem; letter-spacing: .09em; font-weight: 700; text-transform: uppercase; }
    .hero .eyebrow { color: #9ed3e7; }
    .verdict { display: inline-block; border-radius: 999px; font-size: .78rem; font-weight: 800; letter-spacing: .06em; padding: .22rem .62rem; margin: .2rem 0 .75rem 0; }
    .pass { background: #dff4e7; color: #11633c; }
    .fail { background: #ffe4e0; color: #a32921; }
    .decision-card { border-left: 5px solid #1f8a5b; background: white; border-radius: 10px; padding: 1rem 1.2rem; box-shadow: 0 2px 12px rgba(16,43,70,.08); }
    .decision-card.pause { border-left-color: #c53b32; }
    .decision-title { color: #56758b; font-size: .76rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
    .decision-text { font-size: 1.1rem; font-weight: 700; color: #152536; margin-top: .25rem; }
    div[data-testid="stMetric"] { background: #fff; border: 1px solid #e1e9ef; border-radius: 10px; padding: .65rem .75rem; }
    div[data-testid="stMetricLabel"] p { font-size: .76rem; line-height: 1.15; }
    div[data-testid="stMetricValue"] { font-size: 1.45rem; }
    h2, h3 { color: #173b59; }
    </style>
    """,
    unsafe_allow_html=True,
)

inputs = load_inputs()

with st.sidebar:
    st.markdown("## Committee controls")
    st.caption("Adjust the load-bearing constraints to test the decision process.")
    max_position = st.slider("Maximum single ETF weight", min_value=0.20, max_value=0.60, value=0.35, step=0.05)
    trading_cost = st.slider("Trading cost (basis points)", min_value=0, max_value=75, value=10, step=5)
    st.divider()
    st.markdown("**Changed-input test**")
    st.caption("Set the position limit to 30% to test the documented prediction. USMV remains 35%, so the proposed portfolio should fail the position rule.")
    st.divider()
    st.caption("Classroom analysis only. Not investment advice.")

proposed = evaluate_portfolio(inputs, PROPOSED_WEIGHTS, max_position, trading_cost)
equal_weight = evaluate_portfolio(inputs, EQUAL_WEIGHT_WEIGHTS, max_position, trading_cost)
sixty_forty = evaluate_portfolio(inputs, SIXTY_FORTY_WEIGHTS, max_position, trading_cost)
stress = stress_table(inputs, max_position)

st.markdown(
    """
    <section class="hero">
      <div class="eyebrow">Investment committee decision dashboard</div>
      <h1>Conservative U.S. ETF Mandate</h1>
      <p>Point-in-time fixture as of 2025-12-31 | Defensive-factor equity sleeve with Treasury ballast</p>
    </section>
    """,
    unsafe_allow_html=True,
)

eligible_gate = proposed["verdict"] == "PASS"
return_gate = proposed["net_return"] >= equal_weight["net_return"]
if eligible_gate and return_gate:
    decision_html = "<div class='decision-card'><div class='decision-title'>Committee decision</div><div class='decision-text'>PILOT: allocate 10% to 20% sleeve capacity</div><div>Both decision gates pass: mandate compliance and return at least equal to the compliant equal-weight baseline after costs.</div></div>"
else:
    decision_html = "<div class='decision-card pause'><div class='decision-title'>Committee decision</div><div class='decision-text'>PAUSE OR REJECT until the failure is resolved</div><div>The process requires a passing mandate verdict and net expected return at least equal to the compliant equal-weight baseline after costs.</div></div>"
st.markdown(decision_html, unsafe_allow_html=True)

gate_a, gate_b, gate_c, gate_d = st.columns(4)
gate_a.metric("Mandate gate", "PASS" if eligible_gate else "FAIL")
gate_b.metric("Return gate", "PASS" if return_gate else "FAIL", delta=percent(proposed["net_return"] - equal_weight["net_return"]))
gate_c.metric("Selected position limit", percent(max_position))
gate_d.metric("Cost assumption", f"{trading_cost:.0f} bps")

tab_overview, tab_portfolios, tab_evidence = st.tabs(["Committee overview", "Portfolio analysis", "Evidence and controls"])

with tab_overview:
    st.markdown("## Mandate and benchmark")
    left, right = st.columns([1.2, 1])
    with left:
        st.markdown(
            """
            **Objective:** Seek a lower-volatility U.S. equity sleeve with Treasury ballast.  
            **Eligible universe:** SPY, ESGU, USMV, QUAL, IEF, and SHY.  
            **Benchmark:** 60% SPY / 40% IEF.  
            **Risk measure:** Annualized volatility under the documented correlation assumptions.
            """
        )
    with right:
        st.info("**Mandate limits**\n\n- Equity allocation at least 60%\n- Fixed income allocation at least 20%\n- Single ETF no greater than selected limit\n- Annualized volatility at or below 12%")

    st.markdown("## Baseline comparison")
    first, second, third = st.columns(3)
    with first:
        portfolio_summary("Proposed portfolio", "Constrained defensive-factor", proposed)
    with second:
        portfolio_summary("Equal-weight", "Compliant baseline", equal_weight)
    with third:
        portfolio_summary("60/40 benchmark", "Transparent baseline", sixty_forty)

    st.markdown("## Return and risk snapshot")
    compare = pd.DataFrame(
        {
            "Portfolio": ["Proposed", "Equal weight", "60/40 benchmark"],
            "Net expected return": [proposed["net_return"], equal_weight["net_return"], sixty_forty["net_return"]],
            "Annualized volatility": [proposed["volatility"], equal_weight["volatility"], sixty_forty["volatility"]],
        }
    ).set_index("Portfolio")
    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.caption("Net expected return")
        st.bar_chart(compare[["Net expected return"]], color="#1f8a5b", width="stretch")
    with chart_right:
        st.caption("Annualized volatility")
        st.bar_chart(compare[["Annualized volatility"]], color="#1f5d7a", width="stretch")

with tab_portfolios:
    st.markdown("## Proposed portfolio construction")
    construction, weights = st.columns([1, 1])
    with construction:
        st.dataframe(formatted_holdings(proposed), hide_index=True, width="stretch")
    with weights:
        st.caption("Proposed portfolio weights")
        weight_chart = proposed["holdings"].set_index("ticker")[["weight"]]
        st.bar_chart(weight_chart, color="#1f5d7a", width="stretch")

    st.markdown("## Rule-by-rule audit")
    audit_rows = []
    for rule, passed in proposed["rules"].items():
        audit_rows.append({"Mandate rule": rule, "Result": "PASS" if passed else "FAIL"})
    st.dataframe(pd.DataFrame(audit_rows), hide_index=True, width="stretch")

    with st.expander("View baseline holdings"):
        baseline_left, baseline_right = st.columns(2)
        with baseline_left:
            st.markdown("**Equal-weight baseline**")
            st.dataframe(formatted_holdings(equal_weight), hide_index=True, width="stretch")
        with baseline_right:
            st.markdown("**60/40 SPY / IEF baseline**")
            st.dataframe(formatted_holdings(sixty_forty), hide_index=True, width="stretch")

with tab_evidence:
    st.markdown("## Point-in-time signal")
    st.caption("Signal rule: a positive trailing return supports equity-factor eligibility. IEF and SHY are defensive Treasury ballast. The six-month window is included as a stress check.")
    signal_view = inputs[["ticker", "name", "asset_class", "trailing_12m_return", "trailing_6m_return", "signal", "as_of", "source_note"]].assign(
        trailing_12m_return=lambda frame: frame["trailing_12m_return"].map(percent),
        trailing_6m_return=lambda frame: frame["trailing_6m_return"].map(percent),
    )
    st.dataframe(signal_view, hide_index=True, width="stretch")

    st.markdown("## Stress and stop conditions")
    st.caption("Stop or pause if any mandate rule fails, net expected return falls below the compliant equal-weight baseline after costs, or a proposed equity ETF loses positive eligibility at scheduled signal-window review.")
    stress_display = stress.assign(
        **{
            "Net expected return": stress["Net expected return"].map(percent),
            "Volatility": stress["Volatility"].map(percent),
        }
    )
    st.dataframe(stress_display, hide_index=True, width="stretch")

    with st.expander("Calculation and data-quality notes"):
        st.markdown(
            """
            - Net expected return subtracts weighted ETF expense ratios and trading cost.
            - Equity-pair correlation is 0.70; equity/fixed-income correlation is 0.15; IEF/SHY correlation is 0.55.
            - The source file is a dated classroom fixture. Replace it with checked vendor data and retain a source export before real-world use.
            - The application is deterministic and does not fetch live market data.
            """
        )

st.divider()
st.caption("AI use: Codex assisted with application scaffolding, documentation structure, and calculation-review prompts. The analysis and decision are the student's responsibility. Education only - not investment advice.")
