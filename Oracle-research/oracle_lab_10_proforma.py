"""Lab 10: Oracle five-year three-statement pro-forma (USD millions)."""

from __future__ import annotations

YEARS = list(range(2027, 2032))

# Sources, labels, and reasons are in Oracle_lab_10_proforma.md.
ASSUMPTIONS = {
    "revenue_growth": [0.15, 0.12, 0.10, 0.08, 0.06],  # judgment
    "operating_margin": [0.305, 0.305, 0.310, 0.310, 0.315],  # judgment
    "depreciation_to_opening_ppe": 7623.0 / 99957.0,  # history
    "capex_to_revenue": [0.70, 0.55, 0.40, 0.30, 0.25],  # judgment
    "tax_rate": 0.199,  # judgment
    "other_assets_to_revenue_change": 0.01,  # judgment
    "debt_rate": 4599.0 / 129541.0,  # history
    "minimum_cash": 10000.0,  # judgment
    "cash_sweep_threshold": 20000.0,  # judgment
    "cost_of_equity": 0.10,  # judgment
    "terminal_growth": 0.025,  # judgment
    "shares_outstanding": 2880.0,  # fact: May 31, 2026 common shares outstanding
}

OPENING = {
    "revenue": 67357.0,
    "cash": 31289.0,
    "ppe": 99957.0,
    "other_assets": 130513.0,
    "debt": 129541.0,
    "other_liabilities": 89710.0,
    "equity": 42508.0,
}


def assert_balanced(year: int, row: dict[str, float]) -> None:
    """Stop valuation if the balance sheet is incorrect or cash is below its floor."""
    assets = row["cash"] + row["ppe"] + row["other_assets"]
    liabilities_equity = row["debt"] + row["other_liabilities"] + row["equity"]
    gap = assets - liabilities_equity
    if abs(gap) > 1e-7:
        raise ValueError(f"FY{year}E balance-sheet gap: {gap:.1f}")
    if row["cash"] < ASSUMPTIONS["minimum_cash"] - 1e-7:
        raise ValueError(f"FY{year}E cash is below the minimum")


def project() -> list[dict[str, float]]:
    """Project Oracle with cash last and debt as the data-center funding plug."""
    prior = OPENING.copy()
    rows: list[dict[str, float]] = []
    a = ASSUMPTIONS

    for index, year in enumerate(YEARS):
        revenue = prior["revenue"] * (1 + a["revenue_growth"][index])
        operating_income = revenue * a["operating_margin"][index]
        depreciation = prior["ppe"] * a["depreciation_to_opening_ppe"]
        interest = prior["debt"] * a["debt_rate"]
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * a["tax_rate"]
        net_income = pretax_income - tax

        capex = revenue * a["capex_to_revenue"][index]
        ppe = prior["ppe"] + capex - depreciation
        other_assets_change = a["other_assets_to_revenue_change"] * (revenue - prior["revenue"])
        other_assets = prior["other_assets"] + other_assets_change
        other_liabilities = prior["other_liabilities"]
        equity = prior["equity"] + net_income

        # Inventory is not separately material in Oracle's FY2026 balance sheet;
        # use the change in other operating assets rather than ABG floor-plan debt.
        fcfe_before_debt = net_income + depreciation - capex - other_assets_change
        cash_before_debt = prior["cash"] + fcfe_before_debt
        debt = prior["debt"]
        if cash_before_debt < a["minimum_cash"]:
            debt += a["minimum_cash"] - cash_before_debt
            cash = a["minimum_cash"]
        else:
            repayment = min(debt, max(0.0, cash_before_debt - a["cash_sweep_threshold"]))
            debt -= repayment
            cash = cash_before_debt - repayment
        debt_change = debt - prior["debt"]
        fcfe = fcfe_before_debt + debt_change

        row = {
            "year": float(year), "revenue": revenue,
            "operating_income": operating_income, "depreciation": depreciation,
            "interest": interest, "pretax_income": pretax_income, "tax": tax,
            "net_income": net_income, "capex": capex, "ppe": ppe,
            "other_assets": other_assets, "other_assets_change": other_assets_change,
            "cash": cash, "debt": debt, "debt_change": debt_change,
            "other_liabilities": other_liabilities, "equity": equity, "fcfe": fcfe,
        }
        assert_balanced(year, row)
        rows.append(row)
        prior = {**prior, **row}
    return rows


def value_equity(rows: list[dict[str, float]]) -> tuple[float, float]:
    """Value only positive FCFE; the final positive FCFE supports terminal value."""
    a = ASSUMPTIONS
    if a["terminal_growth"] >= a["cost_of_equity"]:
        raise ValueError("Terminal growth must be below the cost of equity")
    explicit_pv = sum(
        max(0.0, row["fcfe"]) / (1 + a["cost_of_equity"]) ** (index + 1)
        for index, row in enumerate(rows)
    )
    terminal_value = rows[-1]["fcfe"] * (1 + a["terminal_growth"]) / (
        a["cost_of_equity"] - a["terminal_growth"]
    )
    equity_value = explicit_pv + terminal_value / (1 + a["cost_of_equity"]) ** len(rows)
    return equity_value, equity_value / a["shares_outstanding"]


def print_table(title: str, rows: list[dict[str, float]], lines: list[tuple[str, str]]) -> None:
    print(f"\n{title}")
    print(f"{'Line':<29}" + "".join(f"FY{year}E{'':>8}" for year in YEARS))
    for label, key in lines:
        print(f"{label:<29}" + "".join(f"{row[key]:>13,.1f}" for row in rows))


def main() -> None:
    rows = project()
    print_table("Income Statement (USD millions)", rows, [
        ("Revenue", "revenue"), ("Operating income", "operating_income"),
        ("Depreciation", "depreciation"), ("Interest", "interest"),
        ("Pretax income", "pretax_income"), ("Tax", "tax"), ("Net income", "net_income"),
    ])
    print_table("Balance Sheet (USD millions)", rows, [
        ("Cash", "cash"), ("PP&E - data centers", "ppe"), ("Other assets", "other_assets"),
        ("Debt", "debt"), ("Other liabilities", "other_liabilities"), ("Equity", "equity"),
    ])
    print_table("Cash Flow / Equity (USD millions)", rows, [
        ("Capital expenditures", "capex"), ("Debt change", "debt_change"),
        ("Free cash flow to equity", "fcfe"),
    ])
    print("\nChecks")
    for row in rows:
        assets = row["cash"] + row["ppe"] + row["other_assets"]
        liabilities_equity = row["debt"] + row["other_liabilities"] + row["equity"]
        print(f"FY{int(row['year'])}E: assets - liabilities - equity = "
              f"{assets - liabilities_equity:.1f}; cash floor met = "
              f"{row['cash'] >= ASSUMPTIONS['minimum_cash']}")
    equity_value, per_share = value_equity(rows)
    print(f"\nEquity value: ${equity_value:,.1f} million")
    print(f"Value per share: ${per_share:.2f}")


if __name__ == "__main__":
    main()
