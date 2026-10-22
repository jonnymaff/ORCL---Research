"""Streamlit interface for the Lab 15 portfolio-stability decision."""

from copy import deepcopy

import streamlit as st

from portfolio import (
    CORRELATIONS,
    OBJECTIVE_RETURN,
    SLEEVES,
    covariance_matrix,
    estimate_from_prices,
    expected_return,
    find_lowest_risk_mix,
    portfolio_volatility,
    reserve_eligible_weight,
)


def loaded_inputs(uploaded_prices):
    """Return all-month CSV estimates, or the Meridian inputs when no CSV is uploaded."""
    if uploaded_prices is None:
        return deepcopy(SLEEVES), deepcopy(CORRELATIONS), "Meridian training inputs"
    uploaded_prices.seek(0)
    sleeves, correlations = estimate_from_prices(uploaded_prices, last_36_months=False)
    return sleeves, correlations, "CSV estimates using all monthly returns"


def current_inputs(uploaded_prices, last_36_months):
    """Return current estimates, using the sidebar's 36-month choice for a CSV."""
    if uploaded_prices is None:
        return deepcopy(SLEEVES), deepcopy(CORRELATIONS)
    uploaded_prices.seek(0)
    return estimate_from_prices(uploaded_prices, last_36_months=last_36_months)


def show_answer(title, weights, sleeves, correlations):
    """Display one optimizer result using calculation functions imported from portfolio.py."""
    st.subheader(title)
    if weights is None:
        st.warning("No mix meets the objective and reserve rule at these inputs.")
        return
    covariances = covariance_matrix(sleeves, correlations)
    rows = [
        {"Asset": name, "Weight": f"{weights[name] * 100:.1f}%"}
        for name in sleeves
    ]
    st.table(rows)
    metric_one, metric_two, metric_three = st.columns(3)
    metric_one.metric("Expected return", f"{expected_return(weights, sleeves) * 100:.2f}%")
    metric_two.metric("Volatility", f"{portfolio_volatility(weights, covariances) * 100:.2f}%")
    metric_three.metric(
        "Reserve eligible", f"{reserve_eligible_weight(weights, sleeves) * 100:.1f}%"
    )


def main():
    st.set_page_config(page_title="Portfolio Stability Decision", layout="wide")
    st.title("Portfolio Stability Decision")
    st.caption("Built with AI help, a learning demonstration, not investment advice.")

    st.sidebar.header("Mandate and data")
    objective = st.sidebar.number_input(
        "Objective return (%)", min_value=-100.0, max_value=100.0,
        value=OBJECTIVE_RETURN * 100, step=0.1,
    ) / 100
    reserve_minimum = st.sidebar.number_input(
        "Minimum reserve-eligible weight (%)", min_value=0.0, max_value=100.0,
        value=3.0, step=1.0,
    ) / 100
    uploaded_prices = st.sidebar.file_uploader(
        "Upload prices.csv", type=["csv"],
        help="Date first, oldest month first, with one adjusted-close column per ticker.",
    )
    last_36_months = st.sidebar.toggle(
        "Use only the last 36 monthly returns", value=False,
    )

    try:
        loaded_sleeves, loaded_correlations, loaded_label = loaded_inputs(uploaded_prices)
        sleeves, correlations = current_inputs(uploaded_prices, last_36_months)
    except (ValueError, KeyError, UnicodeDecodeError) as error:
        st.error(f"Could not estimate from this CSV: {error}")
        return

    st.caption(
        f"Return and volatility figures are {'historical estimates from monthly prices' if uploaded_prices else 'Meridian training inputs'}, not forecasts."
    )
    st.subheader("Editable inputs")
    edited_sleeves = deepcopy(sleeves)
    for asset in sleeves:
        left, right = st.columns([3, 1])
        edited_sleeves[asset]["return"] = left.number_input(
            f"{asset} expected return (%)", min_value=-100.0, max_value=100.0,
            value=float(sleeves[asset]["return"] * 100), step=0.1, key=f"return_{asset}",
        ) / 100
        edited_sleeves[asset]["reserve_eligible"] = right.checkbox(
            f"{asset} reserve eligible", value=sleeves[asset]["reserve_eligible"],
            key=f"reserve_{asset}",
        )

    current_answer = find_lowest_risk_mix(
        edited_sleeves, correlations, objective, reserve_minimum
    )
    loaded_with_current_flags = deepcopy(loaded_sleeves)
    for asset in loaded_with_current_flags:
        loaded_with_current_flags[asset]["reserve_eligible"] = edited_sleeves[asset]["reserve_eligible"]
    loaded_answer = find_lowest_risk_mix(
        loaded_with_current_flags, loaded_correlations, objective, reserve_minimum
    )

    current_label = "Current answer"
    if uploaded_prices and last_36_months:
        current_label += " (last 36 monthly returns)"
    elif uploaded_prices:
        current_label += " (all monthly returns)"
    left, right = st.columns(2)
    with left:
        show_answer(current_label, current_answer, edited_sleeves, correlations)
    with right:
        show_answer(f"Answer as loaded: {loaded_label}", loaded_answer, loaded_with_current_flags, loaded_correlations)

    if current_answer is not None and loaded_answer is not None:
        largest_change = max(
            abs(current_answer[asset] - loaded_answer[asset])
            for asset in edited_sleeves
        )
        st.info(f"Largest weight change versus inputs as loaded: {largest_change * 100:.0f} points.")
    else:
        st.info("Largest weight change is unavailable because one answer is infeasible.")


if __name__ == "__main__":
    main()
