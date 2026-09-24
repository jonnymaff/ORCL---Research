"""Lab 09: five-year ABG three-statement pro-forma (USD millions)."""

from __future__ import annotations


YEARS = list(range(2026, 2031))

# Every input below is copied from the Lab 09 ABG instruction.  Ratios derived
# from FY2025 are labelled history; the remaining labels match the handout.
ASSUMPTIONS = {
    "growth": 0.018,  # judgment
    "gross_margin": 0.1705,  # judgment
    "sga_to_gross_profit": [0.665, 0.655, 0.645, 0.645, 0.645],  # judgment
    "depreciation_to_opening_ppe": 82.4 / 3070.4,  # history
    "impairment": 120.0,  # judgment; non-cash
    "capex": 250.0,  # guidance
    "tax_rate": 0.255,  # judgment
    "inventory_days": 2135.8 / (17999.0 - 3071.7) * 365,  # history
    "floor_plan_to_inventory": 2027.0 / 2135.8,  # history
    "other_working_capital_to_revenue_change": 0.008,  # judgment
    "minimum_cash": 25.0,  # history
    "revolver_limit": 850.0,  # judgment
    "revolver_rate": 0.06,  # judgment
    "annual_debt_repayment": 150.0,  # judgment
    "annual_share_buyback": 150.0,  # judgment
    "floor_plan_rate": 0.0467,  # history
    "term_debt_rate": 0.0544,  # history
    "cost_of_equity": 0.10,  # judgment
    "terminal_growth": 0.025,  # judgment
    "shares_outstanding": 17.951349,  # fact; million shares
}

OPENING = {
    "revenue": 17999.0,
    "inventory": 2135.8,
    "ppe": 3070.4,
    "other_assets": 6371.6,
    "cash": 40.4,
    "floor_plan": 2027.0,
    "term_debt": 3572.0,
    "revolver": 0.0,
    "other_liabilities": 2127.5,
    "equity": 3891.7,
}


def assert_balanced(year: int, row: dict[str, float], minimum_cash: float) -> None:
    """Refuse to value a year whose balance sheet or cash floor is invalid."""
    assets = row["cash"] + row["inventory"] + row["ppe"] + row["other_assets"]
    liabilities_and_equity = (
        row["floor_plan"]
        + row["term_debt"]
        + row["revolver"]
        + row["other_liabilities"]
        + row["equity"]
    )
    gap = assets - liabilities_and_equity
    if abs(gap) > 1e-7:
        raise ValueError(f"FY{year}E balance-sheet gap: {gap:.1f}")
    if row["cash"] < minimum_cash - 1e-7:
        raise ValueError(
            f"FY{year}E cash {row['cash']:.1f} is below the minimum {minimum_cash:.1f}"
        )


def project() -> list[dict[str, float]]:
    """Project income statement, balance sheet, and FCFE in the required order."""
    prior = OPENING.copy()
    rows: list[dict[str, float]] = []
    a = ASSUMPTIONS

    for index, year in enumerate(YEARS):
        revenue = prior["revenue"] * (1 + a["growth"])
        gross_profit = revenue * a["gross_margin"]
        sga = gross_profit * a["sga_to_gross_profit"][index]
        depreciation = prior["ppe"] * a["depreciation_to_opening_ppe"]
        impairment = a["impairment"]
        operating_income = gross_profit - sga - depreciation - impairment
        interest = (
            prior["floor_plan"] * a["floor_plan_rate"]
            + prior["term_debt"] * a["term_debt_rate"]
            + prior["revolver"] * a["revolver_rate"]
        )
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * a["tax_rate"]
        net_income = pretax_income - tax

        inventory = (revenue - gross_profit) * a["inventory_days"] / 365
        floor_plan = inventory * a["floor_plan_to_inventory"]
        ppe = prior["ppe"] + a["capex"] - depreciation
        other_working_capital_change = (
            a["other_working_capital_to_revenue_change"] * (revenue - prior["revenue"])
        )
        other_assets = prior["other_assets"] + other_working_capital_change - impairment
        term_debt = prior["term_debt"] - a["annual_debt_repayment"]
        equity = prior["equity"] + net_income - a["annual_share_buyback"]

        fcfe = (
            net_income
            + depreciation
            + impairment
            - a["capex"]
            - (inventory - prior["inventory"])
            - other_working_capital_change
            + (floor_plan - prior["floor_plan"])
            - a["annual_debt_repayment"]
        )
        cash_before_revolver = prior["cash"] + fcfe - a["annual_share_buyback"]
        revolver = prior["revolver"]
        if cash_before_revolver < a["minimum_cash"]:
            draw = a["minimum_cash"] - cash_before_revolver
            if revolver + draw > a["revolver_limit"]:
                raise ValueError(f"FY{year}E revolver limit exceeded")
            revolver += draw
            cash = a["minimum_cash"]
        else:
            repayment = min(revolver, cash_before_revolver - a["minimum_cash"])
            revolver -= repayment
            cash = cash_before_revolver - repayment

        row = {
            "year": float(year), "revenue": revenue, "gross_profit": gross_profit,
            "sga": sga, "depreciation": depreciation, "impairment": impairment,
            "operating_income": operating_income, "interest": interest,
            "pretax_income": pretax_income, "tax": tax, "net_income": net_income,
            "inventory": inventory, "ppe": ppe, "other_assets": other_assets,
            "cash": cash, "floor_plan": floor_plan, "term_debt": term_debt,
            "revolver": revolver, "other_liabilities": prior["other_liabilities"],
            "equity": equity, "fcfe": fcfe,
        }
        assert_balanced(year, row, a["minimum_cash"])
        rows.append(row)
        prior = {**prior, **row}
    return rows


def print_table(title: str, rows: list[dict[str, float]], lines: list[tuple[str, str]]) -> None:
    print(f"\n{title}")
    print(f"{'Line':<28}" + "".join(f"FY{year}E{'':>8}" for year in YEARS))
    for label, key in lines:
        print(f"{label:<28}" + "".join(f"{row[key]:>13,.1f}" for row in rows))


def value_equity(rows: list[dict[str, float]]) -> tuple[float, float, float]:
    a = ASSUMPTIONS
    if a["terminal_growth"] >= a["cost_of_equity"]:
        raise ValueError("Terminal growth must be below the cost of equity")
    explicit_pv = sum(row["fcfe"] / (1 + a["cost_of_equity"]) ** (index + 1)
                      for index, row in enumerate(rows))
    terminal_value = ((rows[-1]["fcfe"] + a["annual_debt_repayment"])
                      * (1 + a["terminal_growth"])
                      / (a["cost_of_equity"] - a["terminal_growth"]))
    terminal_pv = terminal_value / (1 + a["cost_of_equity"]) ** len(rows)
    equity_value = explicit_pv + terminal_pv
    return equity_value, terminal_pv / equity_value, equity_value / a["shares_outstanding"]


def main() -> None:
    rows = project()
    print_table("Income Statement (USD millions)", rows, [
        ("Revenue", "revenue"), ("Gross profit", "gross_profit"), ("SG&A", "sga"),
        ("Depreciation", "depreciation"), ("Impairment", "impairment"),
        ("Operating income", "operating_income"), ("Interest", "interest"),
        ("Pretax income", "pretax_income"), ("Tax", "tax"), ("Net income", "net_income"),
    ])
    print_table("Balance Sheet (USD millions)", rows, [
        ("Inventory", "inventory"), ("PP&E", "ppe"), ("Other assets", "other_assets"),
        ("Cash", "cash"), ("Floor plan", "floor_plan"), ("Term debt", "term_debt"),
        ("Revolver", "revolver"), ("Other liabilities", "other_liabilities"), ("Equity", "equity"),
    ])
    print_table("Cash Flow / Equity (USD millions)", rows, [
        ("Free cash flow to equity", "fcfe"),
    ])
    print("\nChecks")
    for row in rows:
        assets = row["cash"] + row["inventory"] + row["ppe"] + row["other_assets"]
        liabilities_equity = (row["floor_plan"] + row["term_debt"] + row["revolver"]
                              + row["other_liabilities"] + row["equity"])
        print(f"FY{int(row['year'])}E: assets - liabilities - equity = "
              f"{assets - liabilities_equity:.1f}; cash floor met = "
              f"{row['cash'] >= ASSUMPTIONS['minimum_cash']}")
    equity_value, terminal_share, per_share = value_equity(rows)
    print(f"\nEquity value: ${equity_value:,.1f} million")
    print(f"Share of value after 2030: {terminal_share:.1%}")
    print(f"Value per share: ${per_share:.2f}")


if __name__ == "__main__":
    main()
