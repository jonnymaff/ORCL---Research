"""Deterministic portfolio calculations for the Project 2 classroom app."""

from __future__ import annotations

import numpy as np
import pandas as pd


PROPOSED_WEIGHTS = {"USMV": 0.35, "QUAL": 0.25, "ESGU": 0.15, "IEF": 0.15, "SHY": 0.10}
EQUAL_WEIGHT_WEIGHTS = {"SPY": 1 / 6, "ESGU": 1 / 6, "USMV": 1 / 6, "QUAL": 1 / 6, "IEF": 1 / 6, "SHY": 1 / 6}
SIXTY_FORTY_WEIGHTS = {"SPY": 0.60, "IEF": 0.40}


def correlation_matrix(inputs: pd.DataFrame) -> pd.DataFrame:
    """Return a transparent, conservative cross-asset correlation matrix."""
    tickers = inputs["ticker"].tolist()
    matrix = pd.DataFrame(np.eye(len(tickers)), index=tickers, columns=tickers)
    for left in tickers:
        for right in tickers:
            if left == right:
                continue
            left_class = inputs.loc[inputs.ticker == left, "asset_class"].iloc[0]
            right_class = inputs.loc[inputs.ticker == right, "asset_class"].iloc[0]
            matrix.loc[left, right] = 0.70 if left_class == right_class == "Equity" else 0.15
    matrix.loc["IEF", "SHY"] = matrix.loc["SHY", "IEF"] = 0.55
    return matrix


def evaluate_portfolio(
    inputs: pd.DataFrame,
    weights: dict[str, float],
    max_position: float,
    cost_bps: float = 10.0,
    turnover: float = 0.35,
) -> dict:
    """Calculate net expected return, volatility, and mandate-rule results."""
    portfolio = inputs.set_index("ticker").loc[list(weights)].copy()
    portfolio["weight"] = pd.Series(weights)
    gross_return = float((portfolio["weight"] * portfolio["expected_return"]).sum())
    weighted_expense = float((portfolio["weight"] * portfolio["expense_ratio"]).sum())
    trading_cost = turnover * cost_bps / 10_000
    net_return = gross_return - weighted_expense - trading_cost

    corr = correlation_matrix(inputs).loc[portfolio.index, portfolio.index].to_numpy()
    vol = portfolio["volatility"].to_numpy()
    weight_vector = portfolio["weight"].to_numpy()
    covariance = np.outer(vol, vol) * corr
    portfolio_vol = float(np.sqrt(weight_vector @ covariance @ weight_vector))
    equity_weight = float(portfolio.loc[portfolio.asset_class == "Equity", "weight"].sum())
    fixed_income_weight = float(portfolio.loc[portfolio.asset_class == "Fixed Income", "weight"].sum())
    largest_weight = float(portfolio["weight"].max())

    rules = {
        "Weights sum to 100%": np.isclose(portfolio["weight"].sum(), 1.0),
        f"Single ETF ≤ {max_position:.0%}": largest_weight <= max_position + 1e-9,
        "Equity allocation ≥ 60%": equity_weight >= 0.60,
        "Fixed-income allocation ≥ 20%": fixed_income_weight >= 0.20,
        "Annualized volatility ≤ 12%": portfolio_vol <= 0.12,
    }
    failures = [rule for rule, passed in rules.items() if not passed]
    return {
        "holdings": portfolio.reset_index(),
        "gross_return": gross_return,
        "net_return": net_return,
        "expense_ratio": weighted_expense,
        "trading_cost": trading_cost,
        "volatility": portfolio_vol,
        "equity_weight": equity_weight,
        "fixed_income_weight": fixed_income_weight,
        "largest_weight": largest_weight,
        "rules": rules,
        "verdict": "PASS" if not failures else "FAIL",
        "failures": failures,
    }


def stress_table(inputs: pd.DataFrame, max_position: float) -> pd.DataFrame:
    """Vary estimates, signal window, costs, and constraints against the proposal."""
    rows = []
    cases = [
        ("Base case", 0.00, 10.0, max_position),
        ("Expected returns -150 bps", -0.015, 10.0, max_position, "12-month"),
        ("Signal window shortened to 6 months", 0.00, 10.0, max_position, "6-month"),
        ("Trading cost 50 bps", 0.00, 50.0, max_position),
        ("Position limit tightened to 30%", 0.00, 10.0, 0.30),
    ]
    stressed = inputs.copy()
    for case in cases:
        if len(case) == 4:
            name, return_shift, cost_bps, limit = case
            signal_window = "12-month"
        else:
            name, return_shift, cost_bps, limit, signal_window = case
        stressed["expected_return"] = inputs["expected_return"] + return_shift
        result = evaluate_portfolio(stressed, PROPOSED_WEIGHTS, limit, cost_bps)
        signal_column = "trailing_6m_return" if signal_window == "6-month" else "trailing_12m_return"
        proposed_equities = stressed[stressed["ticker"].isin(["USMV", "QUAL", "ESGU"])]
        eligible_equities = int((proposed_equities[signal_column] > 0).sum())
        rows.append({
            "Scenario": name,
            "Signal-window check": f"{eligible_equities}/3 proposed equity ETFs positive ({signal_window})",
            "Net expected return": result["net_return"],
            "Volatility": result["volatility"],
            "Verdict": result["verdict"],
            "Failed rule(s)": "; ".join(result["failures"]) or "None",
        })
    return pd.DataFrame(rows)
