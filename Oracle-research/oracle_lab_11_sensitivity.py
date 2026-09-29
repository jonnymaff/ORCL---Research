"""Lab 11: one-at-a-time sensitivity analysis for the Oracle pro-forma.

Run: python oracle_lab_11_sensitivity.py
All dollar outputs are USD millions except value per share.
"""

from __future__ import annotations

from copy import deepcopy

from oracle_lab_10_proforma import ASSUMPTIONS, YEARS, project, value_equity

BASE_INPUTS = deepcopy(ASSUMPTIONS)

# Each range is a labelled judgment based on the FY2024--26 history in the
# Lab 10 memo.  The same percentage-point adjustment applies to each forecast
# year, so each scenario is independently reproducible.
DRIVERS = {
    "Revenue growth": {
        "key": "revenue_growth",
        "unit": "% of prior-year revenue",
        "range_reason": (
            "Judgment: FY2024--26 reported growth was 6.0%, 8.4%, and 17.3%. "
            "A 2.0 percentage-point shift tests slower or faster OCI demand "
            "around the existing decelerating path."
        ),
        "cases": {
            "Lower": [0.13, 0.10, 0.08, 0.06, 0.04],
            "Base": BASE_INPUTS["revenue_growth"],
            "Higher": [0.17, 0.14, 0.12, 0.10, 0.08],
        },
    },
    "Operating margin": {
        "key": "operating_margin",
        "unit": "% of revenue",
        "range_reason": (
            "Judgment: FY2026 GAAP operating margin was 30.6%. A 1.0 "
            "percentage-point shift tests execution around the existing "
            "30.5%--31.5% path."
        ),
        "cases": {
            "Lower": [0.295, 0.295, 0.300, 0.300, 0.305],
            "Base": BASE_INPUTS["operating_margin"],
            "Higher": [0.315, 0.315, 0.320, 0.320, 0.325],
        },
    },
}


def fmt_path(values: list[float]) -> str:
    return ", ".join(f"FY{year} {value:.1%}" for year, value in zip(YEARS, values))


def check_rows(rows: list[dict[str, float]], assumptions: dict[str, object]) -> list[str]:
    """Return visible accounting checks rather than silently assuming validity."""
    checks = []
    for row in rows:
        gap = row["cash"] + row["ppe"] + row["other_assets"] - row["debt"] - row["other_liabilities"] - row["equity"]
        cash_ok = row["cash"] >= assumptions["minimum_cash"] - 1e-7
        checks.append(f"FY{int(row['year'])}: gap {gap:.1f}; cash floor met {cash_ok}")
    return checks


def run_case(driver: dict[str, object], case: str) -> dict[str, object]:
    """Use a fresh base copy, then alter exactly one independent input."""
    inputs = deepcopy(BASE_INPUTS)
    key = driver["key"]
    inputs[key] = deepcopy(driver["cases"][case])
    unchanged = all(inputs[name] == BASE_INPUTS[name] for name in BASE_INPUTS if name != key)
    try:
        rows = project(inputs)
        equity_value, per_share = value_equity(rows, inputs)
        return {
            "case": case, "inputs": inputs, "rows": rows, "valid": True,
            "other_inputs_at_base": unchanged, "operating_income": rows[-1]["operating_income"],
            "fcfe": rows[-1]["fcfe"], "equity_value": equity_value,
            "per_share": per_share, "checks": check_rows(rows, inputs),
        }
    except (ValueError, ZeroDivisionError) as error:
        return {"case": case, "inputs": inputs, "valid": False,
                "other_inputs_at_base": unchanged, "error": str(error)}


def print_driver(name: str, driver: dict[str, object]) -> None:
    print(f"\n{name} ({driver['unit']}; FY2027--FY2031)")
    print(f"Range reason: {driver['range_reason']}")
    results = [run_case(driver, case) for case in ("Lower", "Base", "Higher")]
    base = results[1]
    print("Case     Input path                                      FY2031 operating profit  FY2031 FCFE   Value/share")
    for result in results:
        if not result["valid"]:
            print(f"{result['case']:<9} INVALID: {result['error']}")
            continue
        print(f"{result['case']:<9}{fmt_path(result['inputs'][driver['key']]):<48}"
              f"{result['operating_income']:>18,.1f} {result['fcfe']:>13,.1f} ${result['per_share']:>10.2f}")
        print(f"          Change from base: operating profit {result['operating_income'] - base['operating_income']:+,.1f}; "
              f"FCFE {result['fcfe'] - base['fcfe']:+,.1f}; value/share ${result['per_share'] - base['per_share']:+.2f}; "
              f"only selected input changed = {result['other_inputs_at_base']}")
    valid = [result for result in results if result["valid"]]
    for metric, label in (("operating_income", "operating-profit span"), ("fcfe", "FCFE span"), ("per_share", "value/share span")):
        print(f"{label}: {max(result[metric] for result in valid) - min(result[metric] for result in valid):,.2f}")
    selected = results[2]
    if selected["valid"]:
        print("Selected higher-case trace (FY2031): "
              f"revenue {selected['rows'][-1]['revenue']:,.1f}; operating income {selected['operating_income']:,.1f}; "
              f"capex {selected['rows'][-1]['capex']:,.1f}; debt change {selected['rows'][-1]['debt_change']:,.1f}; "
              f"FCFE {selected['fcfe']:,.1f}")
        print("Accounting checks: " + " | ".join(selected["checks"]))


def main() -> None:
    base_before = run_case({"key": "revenue_growth", "cases": {"Base": BASE_INPUTS["revenue_growth"]}}, "Base")
    print("Lab 11 Oracle one-at-a-time sensitivity (USD millions except per share)")
    print("Base inputs are copied fresh for every case; FCFE is signed and valuation discounts signed FCFE.")
    print(f"Base before: FY2031 operating profit {base_before['operating_income']:,.1f}; "
          f"FY2031 FCFE {base_before['fcfe']:,.1f}; value/share ${base_before['per_share']:.2f}")
    for name, driver in DRIVERS.items():
        print_driver(name, driver)
    base_after = run_case({"key": "revenue_growth", "cases": {"Base": BASE_INPUTS["revenue_growth"]}}, "Base")
    restored = all(abs(base_before[key] - base_after[key]) < 1e-7 for key in ("operating_income", "fcfe", "per_share"))
    print(f"\nRestored base: FY2031 operating profit {base_after['operating_income']:,.1f}; "
          f"FY2031 FCFE {base_after['fcfe']:,.1f}; value/share ${base_after['per_share']:.2f}; matches base before = {restored}")
    print("Restored-base accounting checks: " + " | ".join(base_after["checks"]))


if __name__ == "__main__":
    main()
