"""Check candidate allocations against the Meridian Foundation Reserve mandate.

All monetary inputs are in USD millions; portfolio weights are percentages.
"""

# Editable inputs
HOLDINGS = {
    "Cash": {"issuer": "none", "redeem_days": 0, "reserve_eligible": True},
    "Treasury bills": {
        "issuer": "U.S. Treasury", "redeem_days": 1, "reserve_eligible": True
    },
    "Treasury 10-year note": {
        "issuer": "U.S. Treasury", "redeem_days": 1, "reserve_eligible": True
    },
    "Global equity index fund": {
        "issuer": "diversified fund", "redeem_days": 2, "reserve_eligible": False
    },
    "Investment-grade bond fund": {
        "issuer": "diversified fund", "redeem_days": 3, "reserve_eligible": False
    },
    "Private real estate fund": {
        "issuer": "diversified fund", "redeem_days": 90, "reserve_eligible": False
    },
    "Acme Corp bonds": {"issuer": "Acme Corp", "redeem_days": 4, "reserve_eligible": False},
    "Acme Corp stock": {"issuer": "Acme Corp", "redeem_days": 1, "reserve_eligible": False},
}

CANDIDATES = {
    "A": {
        "Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
        "Global equity index fund": 60, "Investment-grade bond fund": 26,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 55, "Investment-grade bond fund": 20,
        "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
        "Global equity index fund": 70, "Investment-grade bond fund": 20,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8,
    },
    # Attack portfolio: checkable rules pass, but its 97% equity allocation may be
    # unsuitable relative to the stated 60/40 benchmark.
    "D": {
        "Cash": 3, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 97, "Investment-grade bond fund": 0,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    # Meridian's stated 40% investment-grade bond / 60% global equity benchmark.
    "E": {
        "Cash": 0, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 60, "Investment-grade bond fund": 40,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
}

RESERVE_SIZE = 100
QUARTERLY_DISTRIBUTION = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW_DAYS = 5
MINIMUM_LIQUID_SHARE = 90
ISSUER_LIMIT = 8
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def weighted_sum(weights, predicate):
    """Sum candidate weights whose holding metadata meets predicate."""
    return sum(weight for holding, weight in weights.items() if predicate(HOLDINGS[holding]))


def largest_single_company(weights):
    """Aggregate securities by non-exempt issuer, then return the largest exposure."""
    issuer_weights = {}
    for holding, weight in weights.items():
        issuer = HOLDINGS[holding]["issuer"]
        if issuer not in EXEMPT_ISSUERS:
            issuer_weights[issuer] = issuer_weights.get(issuer, 0) + weight
    return max(issuer_weights.values(), default=0)


def show_rule(label, value, passes):
    print(f"  {label}: {value:.1f} {'pass' if passes else 'FAIL'}")
    return not passes


def check_candidate(name, weights, reserve_minimum):
    total_weight = sum(weights.values())
    lowest_weight = min(weights.values())
    reserve_eligible_weight = weighted_sum(weights, lambda data: data["reserve_eligible"])
    liquid_weight = weighted_sum(
        weights, lambda data: data["redeem_days"] <= LIQUIDITY_WINDOW_DAYS
    )
    company_weight = largest_single_company(weights)

    print(f"\nCandidate {name}")
    failures = 0
    failures += show_rule("Weights sum to 100", total_weight, total_weight == 100)
    failures += show_rule("Long-only (lowest weight)", lowest_weight, lowest_weight >= 0)
    failures += show_rule(
        f"Reserve >= {reserve_minimum:.1f}%", reserve_eligible_weight,
        reserve_eligible_weight >= reserve_minimum,
    )
    failures += show_rule(
        f"Redeemable in {LIQUIDITY_WINDOW_DAYS} days >= {MINIMUM_LIQUID_SHARE:.1f}%",
        liquid_weight, liquid_weight >= MINIMUM_LIQUID_SHARE,
    )
    failures += show_rule(
        f"Largest single company <= {ISSUER_LIMIT:.1f}%", company_weight,
        company_weight <= ISSUER_LIMIT,
    )
    print("  Calendar-year loss: requires CIO clarification")
    if failures:
        print(f"  fails {failures} rule(s)")
    else:
        print("  passes every checkable rule")


def main():
    reserve_minimum = QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    print(f"Reserve minimum: {reserve_minimum:.1f}% of the portfolio")
    for name, weights in CANDIDATES.items():
        check_candidate(name, weights, reserve_minimum)


if __name__ == "__main__":
    main()
