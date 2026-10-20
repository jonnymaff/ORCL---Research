# Lab 14 — Portfolio Baselines

## Submission files and commands

This lab uses `portfolio.py` for the risk engine and `mandate.py` for the mandate check.

```powershell
python portfolio.py
python mandate.py
python download_prices.py
```

`download_prices.py` creates `prices.csv` for Thursday's fund-universe preview.

## D — The question

**Question:** What does each simple portfolio earn and risk, and does any of them meet the Meridian mandate?

- The **benchmark** is Meridian's 40% investment-grade-bond / 60% global-equity reference.
- **Equal weight** places 25% in each sleeve.
- **Inverse volatility** places more weight in sleeves with lower standalone volatility.

Expected return estimates earnings; volatility measures risk using both each sleeve's volatility and the way sleeves move together. A portfolio must satisfy Meridian's reserve rule as well as its return objective.

### Why two risky assets together can be less risky

When correlation is below +1, two assets do not move perfectly together. Losses in one are not always matched by losses in the other, so the covariance terms lower total portfolio variance compared with a perfect-positive-correlation case. That is why the 40% IG-bond / 60% equity benchmark has 10.46% volatility even though equity alone has 16.0% volatility.

## R — Course-authored inputs

All rates are annual. The 6.5% objective is the labelled 2.5% CPI estimate plus 4.0%.

| Sleeve | Expected return | Volatility | Reserve eligible? |
| --- | ---: | ---: | --- |
| Treasury bills | 3.5% | 0.5% | Yes |
| Treasury 10-year note | 4.3% | 7.0% | Yes |
| Investment-grade bond fund | 5.0% | 6.0% | No |
| Global equity index fund | 8.0% | 16.0% | No |

| Correlation | Bills | 10-year | IG bonds | Equity |
| --- | ---: | ---: | ---: | ---: |
| Bills | 1.00 | 0.10 | 0.05 | 0.00 |
| 10-year | 0.10 | 1.00 | 0.80 | -0.10 |
| IG bonds | 0.05 | 0.80 | 1.00 | 0.25 |
| Equity | 0.00 | -0.10 | 0.25 | 1.00 |

The reserve-eligible sleeves are Treasury bills and the Treasury 10-year note.

## I — Risk-engine design

`portfolio.py` keeps all editable inputs at the top: sleeve expected returns, volatilities, reserve flags, correlation table, and objective. It calculates rather than hard-codes every result.

| Function | What it does |
| --- | --- |
| `validate_correlations` | Refuses a value outside -1 to +1, missing entries, or an asymmetric table. |
| `covariance_matrix` | Calculates covariance as correlation × volatility_i × volatility_j. |
| `expected_return` | Calculates weighted expected return. |
| `portfolio_volatility` | Calculates the square root of the weighted covariance sum. |
| `reserve_eligible_weight` | Adds bills and 10-year-note weights. |
| `benchmark_portfolio`, `equal_weight_portfolio`, `inverse_volatility_portfolio` | Build each required baseline. |
| `print_portfolio` | Prints weights, return, volatility, reserves, and objective decision. |

### Code explanation: portfolio volatility

```python
variance = sum(
    weights[left] * covariances[left][right] * weights[right]
    for left in weights
    for right in weights
)
```

`left` and `right` loop through every pair of sleeves. Each term multiplies the first weight, that pair's covariance, and the second weight. This includes each sleeve's own variance and every between-sleeve covariance. `sqrt(variance)` converts variance to portfolio volatility.

### Self-quiz

**Question:** Why loop through every pair of sleeves instead of adding weighted volatilities?

**Answer:** Portfolio risk depends on how sleeve pairs move together, not just on each sleeve's standalone volatility. The covariance terms measure that diversification effect.

## V — Known-answer proof

I ran `python portfolio.py`. The output matched every given value.

| Portfolio | Weights: bills / 10-year / IG / equity | Return | Volatility | Reserve eligible | Meets 6.5%? |
| --- | --- | ---: | ---: | ---: | --- |
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | Yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | No |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | No |

### Correlation probe

I changed the IG-bond/equity correlation from `0.25` to `0.50` in both symmetric cells. Benchmark volatility rose to **11.00%**, as expected. I then restored both values to `0.25`.

### Invalid-input probe

I set the IG-bond/equity correlation to `1.3` in both cells. The engine refused to calculate:

```text
ValueError: Correlation for Investment-grade bond fund / Global equity index fund is 1.3; it must be between -1 and 1.
```

I restored the valid correlation after testing.

## Explain, swap, and break

The code block to explain is the variance loop in the Risk-engine design section above: it applies the weight-covariance-weight calculation to every sleeve pair, then takes the square root. The critical question is why the off-diagonal pairs are included: those are the correlation-driven covariance terms that measure diversification.

For the required break test, setting the IG-bond/equity correlation to 1.3 causes the engine to refuse the table rather than produce a result. The value must be restored to 0.25 after the test. A partner can run the same command, make this temporary edit, confirm the validation message, and undo it.

## Mandate check — Candidate E

I added Candidate E to `mandate.py`: 40% investment-grade bond fund and 60% global equity index fund. The output was:

| Mandate check | Result |
| --- | --- |
| Weights sum to 100% | Pass |
| Long-only | Pass |
| Reserve minimum: at least 3.0% | **Fail: 0.0%** |
| Redeemable in 5 days: at least 90.0% | Pass: 100.0% |
| Largest single company: at most 8.0% | Pass: 0.0% |

The client's stated benchmark meets the expected-return objective but breaks the reserve rule because it has no allocation to bills or Treasury notes.

## Diversification — Learn on my own

### What is diversification?

Diversification spreads a portfolio across investments whose returns are not identical. It reduces reliance on any one investment or one source of risk.

### How does correlation below +1 lower risk?

At +1 correlation, assets move perfectly together and produce no correlation-based risk reduction. Below +1, they are not perfectly aligned, so the covariance terms in portfolio variance are smaller. Negative correlation creates even stronger partial offsets.

### Benchmark volatility worked by hand

The benchmark is 40% IG bonds and 60% equity:

- `w_IG = 0.40`, `sigma_IG = 0.06`
- `w_equity = 0.60`, `sigma_equity = 0.16`
- `correlation_IG,equity = 0.25`

```text
variance =
(0.40^2 × 0.06^2)
+ (0.60^2 × 0.16^2)
+ (2 × 0.40 × 0.60 × 0.25 × 0.06 × 0.16)

= 0.000576 + 0.009216 + 0.001152
= 0.010944
```

`sqrt(0.010944) = 0.1046`, or **10.46%** volatility. Without the correlation term, the incorrect result is 9.90%.

## Reflection

### Why inverse volatility piles into bills

Inverse-volatility weights are proportional to `1 / volatility`. Bills have 0.5% volatility, far below the other sleeves' 6.0%, 7.0%, and 16.0%, so their inverse-volatility value is largest. After normalization, bills receive 84.3%.

### Baseline I would show the CIO first

I would show the **benchmark** first. It is the only baseline that reaches the 6.5% return objective, at 6.80%. It cannot be adopted unchanged because it fails the 3.0% reserve rule, but it is the best starting point for a CIO discussion of return versus required liquidity. Equal weight and inverse volatility have more reserves but miss the return objective.

## Thursday preview — Fund universe

I selected one fund for each required role. I used Yahoo Finance monthly adjusted-close data because adjusted close includes fund distributions. I did not use money-market funds because their mostly fixed $1.00 price does not provide useful return variation.

| Ticker | Fund name | Role | Source | Download date |
| --- | --- | --- | --- | --- |
| BIL | SPDR Bloomberg 1-3 Month T-Bill ETF | Cash and reserve | Yahoo Finance Historical Data, Monthly Adj Close | 2026-10-20 |
| IEF | iShares 7-10 Year Treasury Bond ETF | Government bonds | Yahoo Finance Historical Data, Monthly Adj Close | 2026-10-20 |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Fixed income | Yahoo Finance Historical Data, Monthly Adj Close | 2026-10-20 |
| VT | Vanguard Total World Stock ETF | Equity | Yahoo Finance Historical Data, Monthly Adj Close | 2026-10-20 |

`prices.csv` has the date first, the oldest month first, and one column for each ticker. It has 60 shared monthly observations from 2021-11-01 through 2026-10-01. `download_prices.py` documents and reproduces the download.

## Checkout

The files to link in the Lab 14 GitHub checkout are:

- `portfolio.py` — risk engine and known-answer calculation.
- `mandate.py` — includes Candidate E.
- `lab14_portfolio_baselines.md` — this written response.
- `prices.csv` — Thursday-preview monthly adjusted-close dataset.

`download_prices.py` is optional supporting code that reproduces `prices.csv`.
