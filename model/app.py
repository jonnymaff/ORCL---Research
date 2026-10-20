"""Semi-adjustable Streamlit workbench; analysis remains in analysis.py."""
from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

import streamlit as st

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import analysis  # noqa: E402

st.set_page_config(page_title="ORCL FCFF Workbench", layout="wide")
st.title("Oracle FCFF Workbench")
st.caption("USD millions except per-share values | Evidence cutoff: 2026-10-16 | Forecasts are analyst judgments")
inputs = analysis.load_inputs()
base = deepcopy(inputs["assumptions"]["base"])

with st.sidebar:
    st.header("Bounded driver panel")
    revenue_shift = st.slider("All-year revenue-growth shift", -0.05, 0.05, 0.00, 0.005, format="%.1f%%")
    margin_shift = st.slider("All-year EBIT-margin shift", -0.03, 0.03, 0.00, 0.005, format="%.1f%%")
    capex_shift = st.slider("All-year capex/revenue shift", -0.08, 0.08, 0.00, 0.005, format="%.1f%%")
    wacc = st.number_input("WACC (decimal; 0.11936 = 11.936%)", min_value=0.08, max_value=0.14, value=float(base["wacc"]), step=0.0001, format="%.5f")
    terminal_growth = st.number_input("Terminal growth (decimal; 0.0250 = 2.5%)", min_value=0.015, max_value=0.035, value=float(base["terminal_growth"]), step=0.0001, format="%.4f")
    if st.button("Reset base"):
        st.rerun()

overrides = {
    "revenue_growth": [value + revenue_shift for value in base["revenue_growth"]],
    "ebit_margin": [value + margin_shift for value in base["ebit_margin"]],
    "capex_to_revenue": [value + capex_shift for value in base["capex_to_revenue"]],
    "wacc": wacc, "terminal_growth": terminal_growth,
}
try:
    case = analysis.run_case(inputs, "base", overrides)
    valuation = case["valuation"]
    checks = analysis.checks(inputs, case)
    scenario_cases = {name: analysis.run_case(inputs, name) for name in ("downside", "base", "upside")}
    sensitivity = analysis.sensitivity(inputs)
    peer_references = analysis.peer_references(inputs)
except ValueError as error:
    st.error(f"MODEL CHECK FAILED: {error}")
    st.stop()

cols = st.columns(4)
cols[0].metric("Value / diluted share", f"${valuation['per_share']:,.2f}")
cols[1].metric("Market close", f"${inputs['valuation_date_bridge']['market_price']:,.2f}")
cols[2].metric("Enterprise value", f"${valuation['enterprise_value']:,.0f}m")
cols[3].metric("PV terminal share", f"{valuation['terminal_value_share']:.1%}")

st.subheader("Five-year pro forma")
table = [{"Year": row["year"], "Revenue": round(row["revenue"], 1), "EBIT": round(row["ebit"], 1),
          "CFO": round(row["cfo"], 1), "Capex": round(row["capex"], 1), "FCFF": round(row["fcff"], 1),
          "Cash": round(row["cash"], 1), "Debt": round(row["debt"], 1), "BS gap": round(row["balance_sheet_gap"], 3)} for row in case["rows"]]
st.dataframe(table, use_container_width=True, hide_index=True)

st.subheader("Frozen base-case valuation range")
st.caption("These are the documented downside/base/upside cases. The bounded panel above changes only the live base-case view.")
scenario_table = [{"Scenario": name.title(), "Value / diluted share": round(result["valuation"]["per_share"], 2)}
                  for name, result in scenario_cases.items()]
st.dataframe(scenario_table, use_container_width=True, hide_index=True)

st.subheader("Frozen base-case WACC / terminal-growth sensitivity")
sensitivity_table = [{"WACC": wacc_label, **{growth_label: round(value, 2) for growth_label, value in values.items()}}
                     for wacc_label, values in sensitivity.items()]
st.dataframe(sensitivity_table, use_container_width=True, hide_index=True)

st.subheader("Qualified peer-reference observations")
peer_table = [{"Peer": peer["peer"], "P/E": round(peer["peer_pe"], 2),
               "EV / Revenue": round(peer["peer_ev_revenue"], 2),
               "P/E-implied ORCL price": round(peer["pe_implied_orcl_price"], 2)}
              for peer in peer_references["references"]]
st.dataframe(peer_table, use_container_width=True, hide_index=True)
st.caption(peer_references["limitation"])

st.subheader("Checks")
st.json(checks)
st.info("A red failure means stop: resolve source, convention, or statement articulation before using the output. The full frozen base output is generated with `python model/analysis.py`.")
