"""Oracle Project 1 finance engine: linked pro forma, FCFF DCF, bridge, and checks.

All currency values are USD millions unless explicitly labeled per share. The input file keeps
reported facts and forecast assumptions distinct. Run from the project root:
    python model/analysis.py
"""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "processed" / "oracle_inputs.json"
OUTPUT_PATH = ROOT / "output" / "visible_output.json"
YEARS = [2027, 2028, 2029, 2030, 2031]


def load_inputs() -> dict[str, Any]:
    return json.loads(INPUT_PATH.read_text(encoding="utf-8"))


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def project(base: dict[str, float], assumptions: dict[str, Any]) -> list[dict[str, float]]:
    """Build a simplified but fully linked IS, BS, and cash-flow statement.

    Debt is the financing plug for a cash floor/sweep; FCFF deliberately excludes it.
    """
    prior = {
        "revenue": base["revenue"], "ppe": base["net_ppe"], "cash": base["cash"],
        "debt": base["debt"], "other_assets": base["other_assets"],
        "other_liabilities": base["other_liabilities"], "equity": base["equity"],
    }
    rows: list[dict[str, float]] = []
    for i, year in enumerate(YEARS):
        revenue = prior["revenue"] * (1 + assumptions["revenue_growth"][i])
        ebit = revenue * assumptions["ebit_margin"][i]
        da = prior["ppe"] * assumptions["da_to_opening_ppe"]
        capex = revenue * assumptions["capex_to_revenue"][i]
        delta_noa = (revenue - prior["revenue"]) * assumptions["incremental_noa_to_revenue_change"]
        interest = prior["debt"] * 0.035  # disclosed separately; not used in FCFF
        pretax = ebit - interest
        tax = max(0.0, pretax) * assumptions["tax_rate"]
        net_income = pretax - tax
        cfo = net_income + da - delta_noa
        fcff = ebit * (1 - assumptions["tax_rate"]) + da - capex - delta_noa
        cash_before_financing = prior["cash"] + cfo - capex
        debt_change = 0.0
        if cash_before_financing < assumptions["minimum_cash"]:
            debt_change = assumptions["minimum_cash"] - cash_before_financing
        elif cash_before_financing > assumptions["cash_sweep_threshold"]:
            debt_change = -min(prior["debt"], cash_before_financing - assumptions["cash_sweep_threshold"])
        debt = prior["debt"] + debt_change
        cash = cash_before_financing + debt_change
        ppe = prior["ppe"] + capex - da
        other_assets = prior["other_assets"] + delta_noa
        other_liabilities = prior["other_liabilities"]
        equity = prior["equity"] + net_income
        assets = cash + ppe + other_assets
        liabilities_equity = debt + other_liabilities + equity
        gap = assets - liabilities_equity
        _assert(abs(gap) < 0.001, f"FY{year} balance-sheet gap is {gap:.3f}")
        _assert(cash >= assumptions["minimum_cash"] - 0.001, f"FY{year} cash floor failed")
        rows.append({"year": year, "revenue": revenue, "ebit": ebit, "da": da, "interest": interest,
                     "tax": tax, "net_income": net_income, "cfo": cfo, "capex": capex, "fcff": fcff,
                     "delta_noa": delta_noa, "cash": cash, "debt": debt, "debt_change": debt_change,
                     "ppe": ppe, "other_assets": other_assets, "other_liabilities": other_liabilities,
                     "equity": equity, "assets": assets, "liabilities_equity": liabilities_equity,
                     "balance_sheet_gap": gap})
        prior = {**prior, **rows[-1]}
    return rows


def dcf(rows: list[dict[str, float]], assumptions: dict[str, Any], bridge: dict[str, float]) -> dict[str, float]:
    wacc, g = assumptions["wacc"], assumptions["terminal_growth"]
    _assert(g < wacc, "Terminal growth must be below WACC")
    explicit_pv = sum(row["fcff"] / (1 + wacc) ** (i + 1) for i, row in enumerate(rows))
    final = rows[-1]
    terminal_fcff = (final["ebit"] * (1 - assumptions["tax_rate"]) + final["da"]
                     - final["revenue"] * assumptions["terminal_capex_to_revenue"]
                     - final["revenue"] * g * assumptions["terminal_incremental_noa_to_revenue_change"])
    _assert(terminal_fcff > 0, "Terminal FCFF must be positive")
    terminal_value = terminal_fcff * (1 + g) / (wacc - g)
    terminal_pv = terminal_value / (1 + wacc) ** len(rows)
    enterprise_value = explicit_pv + terminal_pv
    other_claims = bridge.get("other_claims", 0.0)
    equity_value = enterprise_value + bridge["cash"] - bridge["debt"] - other_claims
    per_share = equity_value / bridge["diluted_shares"]
    return {"explicit_pv": explicit_pv, "terminal_fcff": terminal_fcff, "terminal_value": terminal_value,
            "terminal_pv": terminal_pv, "enterprise_value": enterprise_value, "equity_value": equity_value,
            "per_share": per_share, "terminal_value_share": terminal_pv / enterprise_value}


def run_case(inputs: dict[str, Any], case: str, overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    assumptions = deepcopy(inputs["assumptions"][case])
    if overrides:
        assumptions.update(overrides)
    rows = project(inputs["historical_base_fy2026"], assumptions)
    valuation = dcf(rows, assumptions, inputs["valuation_date_bridge"])
    return {"case": case, "assumptions": assumptions, "rows": rows, "valuation": valuation}


def sensitivity(inputs: dict[str, Any]) -> dict[str, dict[str, float]]:
    base = inputs["assumptions"]["base"]
    grid: dict[str, dict[str, float]] = {}
    for wacc in (base["wacc"] - 0.01, base["wacc"], base["wacc"] + 0.01):
        label = f"{wacc:.1%}"
        grid[label] = {}
        for growth in (0.02, 0.025, 0.03):
            grid[label][f"{growth:.1%}"] = run_case(inputs, "base", {"wacc": wacc, "terminal_growth": growth})["valuation"]["per_share"]
    return grid


def reverse_dcf(inputs: dict[str, Any]) -> dict[str, float | str]:
    """Solve uniform additive growth-path shift with WACC/terminal assumptions fixed."""
    target = inputs["valuation_date_bridge"]["market_price"]
    low, high = -0.10, 0.20
    def price_for(shift: float) -> float:
        base = deepcopy(inputs["assumptions"]["base"])
        path = [max(-0.95, value + shift) for value in base["revenue_growth"]]
        return run_case(inputs, "base", {"revenue_growth": path})["valuation"]["per_share"]

    low_price, high_price = price_for(low), price_for(high)
    if not low_price <= target <= high_price:
        return {"target_price": target, "status": "no solution in predeclared search range",
                "search_range": "uniform additive growth shift from -10.0 to +20.0 percentage points",
                "low_endpoint_price": low_price, "high_endpoint_price": high_price,
                "held_fixed": "EBIT margins, capex path, tax rate, WACC, terminal growth, bridge"}
    for _ in range(80):
        mid = (low + high) / 2
        value = price_for(mid)
        if value < target:
            low = mid
        else:
            high = mid
    shift = (low + high) / 2
    path = [value + shift for value in inputs["assumptions"]["base"]["revenue_growth"]]
    result = run_case(inputs, "base", {"revenue_growth": path})["valuation"]["per_share"]
    return {"target_price": target, "solved_uniform_growth_shift": shift, "solved_price": result,
            "held_fixed": "EBIT margins, capex path, tax rate, WACC, terminal growth, bridge"}


def run_analysis(inputs: dict[str, Any] | None = None) -> dict[str, Any]:
    """Public analysis entry point used by the interface and tests."""
    return build_visible_output(load_inputs() if inputs is None else inputs)


def peer_references(inputs: dict[str, Any]) -> dict[str, Any]:
    bridge = inputs["valuation_date_bridge"]
    orcl_eps = 5.83  # FY2026 GAAP diluted EPS; 10-K EPS note
    orcl_market_ev = (bridge["market_price"] * bridge["diluted_shares"] + bridge["debt"]
                      + bridge.get("other_claims", 0.0) - bridge["cash"])
    references = []
    for peer in inputs["qualified_peer_references"]:
        peer_pe = peer["price"] / peer["annual_gaap_diluted_eps"]
        peer_ev = (peer["price"] * peer["shares_outstanding_millions"] + peer["total_debt"]
                   - peer["cash_and_short_term_investments"])
        references.append({"peer": peer["ticker"], "peer_pe": peer_pe,
                           "pe_implied_orcl_price": peer_pe * orcl_eps,
                           "peer_ev_revenue": peer_ev / peer["annual_revenue"],
                           "basis": peer["basis"]})
    return {"orcl_pe": bridge["market_price"] / orcl_eps,
            "orcl_market_ev": orcl_market_ev,
            "orcl_market_ev_revenue": orcl_market_ev / inputs["historical_base_fy2026"]["revenue"],
            "references": references,
            "limitation": "Microsoft and Salesforce are qualified reference observations, not interchangeable peers or a mechanically averaged valuation range."}


def checks(inputs: dict[str, Any], base_case: dict[str, Any]) -> dict[str, Any]:
    rows = base_case["rows"]
    balance_ok = all(abs(row["balance_sheet_gap"]) < 0.001 for row in rows)
    cash_tie_ok = all(abs((row["cash"] - (inputs["historical_base_fy2026"]["cash"] if i == 0 else rows[i-1]["cash"])) - (row["cfo"] - row["capex"] + row["debt_change"])) < 0.001 for i, row in enumerate(rows))
    base_wacc = inputs["assumptions"]["base"]["wacc"]
    low_wacc = run_case(inputs, "base", {"wacc": base_wacc - 0.01})["valuation"]["per_share"]
    high_wacc = run_case(inputs, "base", {"wacc": base_wacc + 0.01})["valuation"]["per_share"]
    low_g = run_case(inputs, "base", {"terminal_growth": 0.02})["valuation"]["per_share"]
    high_g = run_case(inputs, "base", {"terminal_growth": 0.03})["valuation"]["per_share"]
    return {"base_year_balance_sheet": abs(inputs["historical_base_fy2026"]["assets"] - inputs["historical_base_fy2026"]["debt"] - inputs["historical_base_fy2026"]["other_liabilities"] - inputs["historical_base_fy2026"]["equity"]) < 0.001,
            "forecast_balance_sheets": balance_ok, "cash_flow_ties_to_cash": cash_tie_ok,
            "wacc_monotonic": low_wacc > base_case["valuation"]["per_share"] > high_wacc,
            "terminal_growth_monotonic": low_g < base_case["valuation"]["per_share"] < high_g,
            "bridge_identity": abs(base_case["valuation"]["equity_value"] - (base_case["valuation"]["enterprise_value"] + inputs["valuation_date_bridge"]["cash"] - inputs["valuation_date_bridge"]["debt"] - inputs["valuation_date_bridge"].get("other_claims", 0.0))) < 0.001}


def build_visible_output(inputs: dict[str, Any]) -> dict[str, Any]:
    cases = {name: run_case(inputs, name) for name in ("downside", "base", "upside")}
    base = cases["base"]
    visible = {
        "decision": "Oracle (ORCL) five-year FCFF valuation workbench for a buy-side committee",
        "as_of": inputs["meta"]["valuation_date"], "units": inputs["meta"]["units"],
        "market_price": inputs["valuation_date_bridge"]["market_price"],
        "material_inputs": {
            "base_year_revenue": inputs["historical_base_fy2026"]["revenue"],
            "base_year_ebit": inputs["historical_base_fy2026"]["ebit"],
            "base_year_capex": inputs["historical_base_fy2026"]["capex"],
            "bridge_cash": inputs["valuation_date_bridge"]["cash"],
            "bridge_debt": inputs["valuation_date_bridge"]["debt"],
            "bridge_other_claims": inputs["valuation_date_bridge"].get("other_claims", 0.0),
            "bridge_diluted_shares": inputs["valuation_date_bridge"]["diluted_shares"],
            "base_revenue_growth": inputs["assumptions"]["base"]["revenue_growth"],
            "base_ebit_margin": inputs["assumptions"]["base"]["ebit_margin"],
            "base_capex_to_revenue": inputs["assumptions"]["base"]["capex_to_revenue"],
            "base_wacc": inputs["assumptions"]["base"]["wacc"],
            "base_terminal_growth": inputs["assumptions"]["base"]["terminal_growth"]
        },
        "scenario_per_share": {name: round(value["valuation"]["per_share"], 2) for name, value in cases.items()},
        "valuation_range": [round(cases["downside"]["valuation"]["per_share"], 2), round(cases["upside"]["valuation"]["per_share"], 2)],
        "committee_action": "Watch / defer: do not initiate until cash conversion and funding evidence supports a durable FCFF recovery.",
        "conditions": ["Sustained improvement in FCFF after capacity spending", "Net debt stable or declining without unsupported bridge adjustments", "Evidence that the capex-intensity fade is credible"],
        "base_case": {"enterprise_value": round(base["valuation"]["enterprise_value"], 1), "equity_value": round(base["valuation"]["equity_value"], 1), "per_share": round(base["valuation"]["per_share"], 2), "terminal_value_share": round(base["valuation"]["terminal_value_share"], 4)},
        "base_case_five_year_pro_forma": [
            {key: round(row[key], 1) for key in (
                "year", "revenue", "ebit", "net_income", "cfo", "capex", "fcff",
                "cash", "debt", "ppe", "assets", "liabilities_equity", "balance_sheet_gap"
            )}
            for row in base["rows"]
        ],
        "sensitivity": sensitivity(inputs), "reverse_dcf": reverse_dcf(inputs), "peer_references": peer_references(inputs),
        "checks": checks(inputs, base),
        "limitations": ["Forecast paths are analyst judgments, not company guidance.", "Microsoft and Salesforce are reference observations, not a peer-set valuation or a mechanical average.", "Bridge excludes any unsourced adjustments for leases, preferred, or other claims.", "Terminal-value share makes the long-run capex, WACC, and terminal-growth assumptions load-bearing."]
    }
    return visible


def main() -> None:
    inputs = load_inputs()
    output = run_analysis(inputs)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
