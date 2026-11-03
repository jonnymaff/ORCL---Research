"""Streamlit viewer for the Lab 18 reproducible Buffett analysis."""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import streamlit as st

from edgar_buffett import NOT_FOUND, analyze

st.set_page_config(page_title="Legend Investor", layout="wide")
st.title("Legend Investor as Skill")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")


def memo_number_flags(memo: str, data: dict) -> list[str]:
    """Flag numeric claims whose numeric token is absent from this script's output."""
    allowed = set()
    for row in data["rows"]:
        for key, value in row.items():
            if isinstance(value, (int, float)):
                allowed.add(f"{value:,.0f}")
                allowed.add(f"{value:.1f}")
                allowed.add(str(round(value, 1)))
    claims = re.findall(r"\$?\d{1,3}(?:,\d{3})+(?:\.\d+)?%?|\b\d+\.\d+%", memo)
    flagged = []
    for claim in claims:
        token = claim.replace("$", "").replace("%", "")
        if token not in allowed and token not in flagged:
            flagged.append(claim)
    return flagged


ticker = st.text_input("Ticker", value="COST", max_chars=8).upper().strip()
if st.button("Load SEC 10-K facts", type="primary") or ticker == "COST":
    try:
        with st.spinner("Downloading company facts from SEC EDGAR..."):
            data = analyze(ticker)
        st.subheader(f"{data['company']} ({data['ticker']})")
        frame = pd.DataFrame(data["rows"])
        display = frame.drop(columns=["tags"])
        st.line_chart(display.set_index("fiscal_year_end")[["owner_earnings", "net_income"]])
        st.caption("$ millions; owner earnings = operating cash flow − capital spending")
        st.dataframe(display, width="stretch")
        st.subheader("XBRL tags used")
        st.dataframe(pd.DataFrame([{"fiscal year end": r["fiscal_year_end"], **r["tags"]} for r in data["rows"]]), width="stretch")
        st.subheader("Buffett checks")
        st.dataframe(pd.DataFrame(data["checks"].items(), columns=["Check", "Result"]), hide_index=True, width="stretch")

        memo_file = Path(__file__).with_name(f"{ticker}_buffett_memo.md")
        st.subheader("Memo")
        if memo_file.exists():
            memo = memo_file.read_text(encoding="utf-8")
            st.markdown(memo)
            flags = memo_number_flags(memo, data)
            if flags:
                st.error("Memo numbers not printed by the script: " + ", ".join(flags))
            else:
                st.success("Every numeric memo claim appears in the script output.")
        else:
            st.info(f"No saved memo yet. Use the skill to create {memo_file.name} from these printed values only.")
    except Exception as error:
        st.error(f"Could not load {ticker}: {error}")
