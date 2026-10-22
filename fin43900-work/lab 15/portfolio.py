"""Risk and return calculations for Meridian's simple portfolio baselines.

All rates below are annual decimals: 0.035 represents 3.5%.
Run with: python portfolio.py
"""

import csv
from math import sqrt
from statistics import mean, stdev

# Editable inputs
SLEEVES = {
    "Treasury bills": {"return": 0.035, "volatility": 0.005, "reserve_eligible": True},
    "Treasury 10-year note": {"return": 0.043, "volatility": 0.070, "reserve_eligible": True},
    "Investment-grade bond fund": {"return": 0.050, "volatility": 0.060, "reserve_eligible": False},
    "Global equity index fund": {"return": 0.080, "volatility": 0.160, "reserve_eligible": False},
}

CORRELATIONS = {
    "Treasury bills": {"Treasury bills": 1.00, "Treasury 10-year note": 0.10, "Investment-grade bond fund": 0.05, "Global equity index fund": 0.00},
    "Treasury 10-year note": {"Treasury bills": 0.10, "Treasury 10-year note": 1.00, "Investment-grade bond fund": 0.80, "Global equity index fund": -0.10},
    "Investment-grade bond fund": {"Treasury bills": 0.05, "Treasury 10-year note": 0.80, "Investment-grade bond fund": 1.00, "Global equity index fund": 0.25},
    "Global equity index fund": {"Treasury bills": 0.00, "Treasury 10-year note": -0.10, "Investment-grade bond fund": 0.25, "Global equity index fund": 1.00},
}

OBJECTIVE_RETURN = 0.065  # CPI estimate of 2.5% + 4.0%


def validate_correlations(sleeves, correlations):
    """Raise ValueError if the correlation table is incomplete, invalid, or asymmetric."""
    names = set(sleeves)
    if set(correlations) != names:
        raise ValueError("Correlation table must have exactly one row for every sleeve.")
    for left in sleeves:
        if set(correlations[left]) != names:
            raise ValueError(f"Correlation row for {left} must include every sleeve.")
        for right in sleeves:
            value = correlations[left][right]
            if not -1 <= value <= 1:
                raise ValueError(f"Correlation for {left} / {right} is {value}; it must be between -1 and 1.")
            if value != correlations[right][left]:
                raise ValueError(f"Correlation table is not symmetric at {left} / {right}.")


def covariance_matrix(sleeves, correlations):
    """Return covariance[i][j] = correlation[i][j] * volatility[i] * volatility[j]."""
    return {
        left: {
            right: correlations[left][right] * sleeves[left]["volatility"] * sleeves[right]["volatility"]
            for right in sleeves
        }
        for left in sleeves
    }


def expected_return(weights, sleeves):
    """Calculate the weighted expected return."""
    return sum(weights[name] * sleeves[name]["return"] for name in sleeves)


def portfolio_volatility(weights, covariances):
    """Calculate sqrt(sum_i(sum_j(w_i * covariance_ij * w_j)))."""
    variance = sum(
        weights[left] * covariances[left][right] * weights[right]
        for left in weights
        for right in weights
    )
    return sqrt(variance)


def reserve_eligible_weight(weights, sleeves):
    """Return the total weight in reserve-eligible sleeves."""
    return sum(weights[name] for name in sleeves if sleeves[name]["reserve_eligible"])


def long_only_mixes(asset_names, step=0.05):
    """Yield every long-only allocation whose weights sum to 100% at the given step."""
    units = round(1 / step)
    if units <= 0 or abs(units * step - 1) > 1e-9:
        raise ValueError("Step must divide evenly into 100%; for example, use 0.05.")

    def build(index, remaining, partial):
        if index == len(asset_names) - 1:
            yield {**partial, asset_names[index]: remaining / units}
            return
        for allocation in range(remaining + 1):
            yield from build(
                index + 1,
                remaining - allocation,
                {**partial, asset_names[index]: allocation / units},
            )

    yield from build(0, units, {})


def find_lowest_risk_mix(
    sleeves, correlations, objective_return, minimum_reserve_weight, step=0.05
):
    """Return the feasible long-only mix with the lowest volatility, or None."""
    validate_correlations(sleeves, correlations)
    covariances = covariance_matrix(sleeves, correlations)
    best_weights = None
    best_volatility = None
    for weights in long_only_mixes(list(sleeves), step):
        if expected_return(weights, sleeves) < objective_return:
            continue
        if reserve_eligible_weight(weights, sleeves) < minimum_reserve_weight:
            continue
        volatility = portfolio_volatility(weights, covariances)
        if best_volatility is None or volatility < best_volatility:
            best_weights = weights
            best_volatility = volatility
    return best_weights


def estimate_from_prices(csv_file, last_36_months=False):
    """Estimate annualized returns, volatility, and correlations from monthly prices.

    The CSV must put the date first, use oldest-first rows, and use one price
    column per asset. Returns are historical estimates, not forecasts.
    """
    should_close = False
    if isinstance(csv_file, (str, bytes)):
        csv_file = open(csv_file, newline="", encoding="utf-8")
        should_close = True
    try:
        rows = list(csv.DictReader(csv_file))
    finally:
        if should_close:
            csv_file.close()
    if not rows or not rows[0]:
        raise ValueError("Price CSV must contain a header and at least two rows.")
    columns = list(rows[0])
    if len(columns) < 4 or columns[0].lower() != "date":
        raise ValueError("Price CSV needs date first and at least three asset columns.")
    names = columns[1:]
    prices = {name: [float(row[name]) for row in rows] for name in names}
    if any(len(values) < 2 for values in prices.values()):
        raise ValueError("Each asset needs at least two monthly prices.")
    returns = {
        name: [
            current / previous - 1
            for previous, current in zip(values, values[1:])
        ]
        for name, values in prices.items()
    }
    if last_36_months:
        returns = {name: values[-36:] for name, values in returns.items()}
    if any(len(values) < 2 for values in returns.values()):
        raise ValueError("At least three price rows are needed to estimate volatility.")
    sleeves = {
        name: {
            "return": mean(values) * 12,
            "volatility": stdev(values) * sqrt(12),
            "reserve_eligible": False,
        }
        for name, values in returns.items()
    }
    correlations = {
        left: {
            right: 1.0 if left == right else _correlation(returns[left], returns[right])
            for right in names
        }
        for left in names
    }
    return sleeves, correlations


def _correlation(left_values, right_values):
    """Return the sample correlation of two equal-length numeric sequences."""
    left_mean = mean(left_values)
    right_mean = mean(right_values)
    numerator = sum(
        (left - left_mean) * (right - right_mean)
        for left, right in zip(left_values, right_values)
    )
    denominator = sqrt(
        sum((left - left_mean) ** 2 for left in left_values)
        * sum((right - right_mean) ** 2 for right in right_values)
    )
    if denominator == 0:
        raise ValueError("Correlation cannot be estimated for a zero-variation return series.")
    return numerator / denominator


def equal_weight_portfolio(sleeves):
    """Allocate equally across all sleeves."""
    return {name: 1 / len(sleeves) for name in sleeves}


def inverse_volatility_portfolio(sleeves):
    """Allocate in proportion to one divided by each sleeve's volatility."""
    inverse_volatilities = {name: 1 / data["volatility"] for name, data in sleeves.items()}
    total = sum(inverse_volatilities.values())
    return {name: value / total for name, value in inverse_volatilities.items()}


def benchmark_portfolio(sleeves):
    """Return Meridian's 40% IG bond / 60% global equity benchmark."""
    return {
        name: 0.40 if name == "Investment-grade bond fund" else 0.60 if name == "Global equity index fund" else 0.0
        for name in sleeves
    }


def print_portfolio(name, weights, sleeves, covariances, objective_return):
    """Print one portfolio's weights and calculated metrics."""
    weight_text = " / ".join(f"{weights[sleeve] * 100:.1f}" for sleeve in sleeves)
    result_return = expected_return(weights, sleeves)
    result_volatility = portfolio_volatility(weights, covariances)
    reserves = reserve_eligible_weight(weights, sleeves)
    print(f"{name}\n  Weights (bills / 10-year / IG / equity): {weight_text}\n"
          f"  Expected return: {result_return * 100:.2f}%\n"
          f"  Volatility: {result_volatility * 100:.2f}%\n"
          f"  Reserve-eligible: {reserves * 100:.1f}%\n"
          f"  Meets {objective_return * 100:.1f}% objective: {'yes' if result_return >= objective_return else 'no'}")


def main():
    validate_correlations(SLEEVES, CORRELATIONS)
    covariances = covariance_matrix(SLEEVES, CORRELATIONS)
    portfolios = {
        "Benchmark": benchmark_portfolio(SLEEVES),
        "Equal weight": equal_weight_portfolio(SLEEVES),
        "Inverse volatility": inverse_volatility_portfolio(SLEEVES),
    }
    for name, weights in portfolios.items():
        print_portfolio(name, weights, SLEEVES, covariances, OBJECTIVE_RETURN)
        print()


if __name__ == "__main__":
    main()
