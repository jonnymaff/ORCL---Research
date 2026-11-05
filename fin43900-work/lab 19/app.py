"""Streamlit Lab 19 Legend Panel: three reproducible readings of one 10-K data set."""
from __future__ import annotations

import re

import pandas as pd
import streamlit as st

from edgar_buffett import NOT_KNOWN, analyze

st.set_page_config(page_title="Legend Panel", page_icon="LP", layout="wide")
st.markdown(
    """
    <style>
      .block-container {max-width: 1320px; padding-top: 2.3rem; padding-bottom: 3rem;}
      [data-testid="stSidebar"] {background: #102a43;}
      [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
      [data-testid="stSidebar"] label, [data-testid="stSidebar"] p,
      [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {color: #f5f7fa !important;}
      [data-testid="stSidebar"] input {background: #ffffff !important; color: #102a43 !important;}
      [data-testid="stSidebar"] [data-baseweb="select"] > div {background: #ffffff !important; color: #102a43 !important;}
      [data-testid="stSidebar"] [data-baseweb="select"] span {color: #102a43 !important;}
      .eyebrow {color: #147d92; font-size: .8rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase;}
      .hero {background: linear-gradient(115deg, #102a43, #184e5b); border-radius: 16px; color: #fff; padding: 1.5rem 1.75rem; margin: .35rem 0 1.5rem;}
      .hero h2 {color: #fff; margin: 0 0 .25rem;}
      .hero p {color: #dce9ed; margin: 0;}
      .investor-card {border: 1px solid #d9e2ec; border-top: 5px solid #147d92; border-radius: 12px; padding: 1rem 1.1rem; background: #fff; min-height: 135px;}
      .investor-card h3 {margin: 0 0 .25rem; color: #102a43;}
      .investor-card p {margin: .3rem 0 0; color: #52606d; font-size: .9rem;}
      .pill {border-radius: 999px; display: inline-block; font-size: .78rem; font-weight: 750; letter-spacing: .04em; padding: .22rem .58rem; text-transform: uppercase;}
      .pass {background: #d9f7e7; color: #146c43;}
      .watch {background: #fff0c2; color: #7a4b00;}
      .incomplete {background: #e7edf3; color: #334e68;}
      .memo-note {color: #627d98; font-size: .85rem;}
      h1 {color: #102a43; letter-spacing: -.02em;}
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="eyebrow">Lab 19 / SEC EDGAR / Five annual 10-Ks</div>', unsafe_allow_html=True)
st.title("Legend Panel")
st.caption("Three investor screens. One shared fact set. Transparent gaps.")


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def display_number(value: object, suffix: str = "") -> str:
    return f"{value:,.2f}{suffix}" if is_number(value) else str(value)


def verdict(results: dict[str, str]) -> str:
    passed, failed, unknown = (sum(result == state for result in results.values()) for state in ("pass", "fail", NOT_KNOWN))
    if failed:
        return f"watch ({passed} pass, {failed} fail, {unknown} not known)"
    if unknown:
        return f"incomplete ({passed} pass, {unknown} not known)"
    return f"pass ({passed} of {len(results)})"


def verdict_style(label: str) -> tuple[str, str]:
    if label.startswith("pass"):
        return "pass", "Pass"
    if label.startswith("incomplete"):
        return "incomplete", "Incomplete"
    return "watch", "Watch"


def memo(investor: str, data: dict, results: dict[str, str]) -> str:
    """Compose each persona's memo only from values present in collector output."""
    first, latest = data["rows"][0], data["rows"][-1]
    if investor == "Buffett":
        evidence = (f"Revenue moved from ${display_number(first['revenue'])}m to ${display_number(latest['revenue'])}m. "
                    f"Net income moved from ${display_number(first['net_income'])}m to ${display_number(latest['net_income'])}m. "
                    f"Latest ROE was {display_number(latest['roe'], '%')} and owner earnings were ${display_number(latest['owner_earnings'])}m.")
        lens = "Durable profitability and cash left after capital spending."
    elif investor == "Graham":
        evidence = (f"Latest current assets were ${display_number(latest['assets_current'])}m and current liabilities were ${display_number(latest['liabilities_current'])}m, "
                    f"for a current ratio of {display_number(latest['current_ratio'])}. "
                    f"Net income moved from ${display_number(first['net_income'])}m to ${display_number(latest['net_income'])}m.")
        lens = f"Conservative liquidity, with a {data['graham_current_ratio_threshold']:.1f} current-ratio threshold."
    else:
        evidence = (f"Latest operating cash flow was ${display_number(latest['operating_cash_flow'])}m versus net income of ${display_number(latest['net_income'])}m. "
                    f"Latest liabilities were ${display_number(latest['liabilities'])}m and equity was ${display_number(latest['equity'])}m, "
                    f"for liabilities / equity of {display_number(latest['liabilities_to_equity'])}.")
        lens = "Cash conversion and a bounded balance sheet."
    checks_text = "  ".join(f"- **{name}:** {result}" for name, result in results.items())
    return f"<span class='memo-note'>{lens}</span>\n\n{evidence}\n\n{checks_text}\n\n*Business-quality screen only; it does not measure valuation or give buy/sell advice.*"


def memo_number_flags(memo_text: str, data: dict) -> list[str]:
    """Flag decimal/dollar claims that collector JSON does not print in some form."""
    allowed: set[str] = set()
    for row in data["rows"]:
        for value in row.values():
            if is_number(value):
                allowed.update({str(value), f"{value:.1f}", f"{value:.2f}", f"{value:,.0f}", f"{value:,.1f}", f"{value:,.2f}"})
    claims = re.findall(r"\$?\d{1,3}(?:,\d{3})*(?:\.\d+)?%?", memo_text)
    flags = []
    for claim in claims:
        token = claim.replace("$", "").replace("%", "")
        if token not in allowed and claim not in flags and token not in {"1.0", "2", "2.0"}:
            flags.append(claim)
    return flags


with st.sidebar:
    st.header("Panel controls")
    st.caption("Use the same annual SEC EDGAR facts for every investor.")
    ticker = st.selectbox("Company ticker", options=["COST", "ORCL"], index=0)
    threshold = st.number_input("Graham current-ratio threshold", min_value=0.1, max_value=5.0, value=2.0, step=0.1)
    load = st.button("Analyze 10-K facts", type="primary", use_container_width=True)
    st.divider()
    st.markdown("**Threshold probe**")
    st.caption("Set the threshold to 1.0 to see Graham pass COST. Restore 2.0 for the stated rule.")

if load or ticker == "COST":
    try:
        with st.spinner("Downloading annual 10-K facts from SEC EDGAR..."):
            data = analyze(ticker, threshold)
        rows, panel = data["rows"], data["panel_checks"]
        st.markdown(
            f"<div class='hero'><h2>{data['company']} <span style='font-weight:400'>({data['ticker']})</span></h2>"
            "<p>Five annual 10-K fact rows | Dollar amounts in millions | Missing inputs remain visible</p></div>",
            unsafe_allow_html=True,
        )

        cards = st.columns(3)
        for column, (investor, results) in zip(cards, panel.items()):
            outcome = verdict(results)
            css, label = verdict_style(outcome)
            passed = sum(value == "pass" for value in results.values())
            with column:
                st.markdown(
                    f"<div class='investor-card'><h3>{investor}</h3><span class='pill {css}'>{label}</span>"
                    f"<p>{passed} passing check{'s' if passed != 1 else ''} of {len(results)}<br>{outcome}</p></div>",
                    unsafe_allow_html=True,
                )

        tab_panel, tab_facts, tab_sources = st.tabs(["Panel overview", "Five-year facts", "Data lineage"])
        with tab_panel:
            st.subheader("Check-by-check panel")
            panel_rows = [
                {"Investor": investor, "Check": check, "Result": result, "Verdict": verdict(results)}
                for investor, results in panel.items() for check, result in results.items()
            ]
            st.dataframe(pd.DataFrame(panel_rows), hide_index=True, width="stretch")
            st.subheader("Memos from the same printed facts")
            memos = {investor: memo(investor, data, results) for investor, results in panel.items()}
            for column, (investor, memo_text) in zip(st.columns(3), memos.items()):
                with column:
                    st.container(border=True).markdown(f"### {investor}\n\n{memo_text}", unsafe_allow_html=True)
            bad = {investor: flagged for investor, text in memos.items() if (flagged := memo_number_flags(text, data))}
            if bad:
                st.error("Unprinted-number flag: " + "; ".join(f"{investor}: {', '.join(values)}" for investor, values in bad.items()))
            else:
                st.success("Unprinted-number flag: clear across all three memos.")
        with tab_facts:
            st.subheader("Five-year facts and computed ratios")
            st.caption("All dollars in $ millions. `not found` and `not known` are preserved rather than estimated.")
            st.dataframe(pd.DataFrame(rows).drop(columns=["tags"]), hide_index=True, width="stretch")
        with tab_sources:
            st.subheader("XBRL tags used")
            st.caption("Each tag identifies the annual SEC company-fact source or the formula used for a computed measure.")
            st.dataframe(pd.DataFrame([{"Fiscal year end": row["fiscal_year_end"], **row["tags"]} for row in rows]), hide_index=True, width="stretch")
    except Exception as error:
        st.error(f"Could not load {ticker}: {error}")
