# Lab 15 — Portfolio Stability Decision

## D — Decision question

**Which mix carries the least risk while meeting the mandate, and does that answer survive a one-point change in one estimate?**

The Streamlit app searches every long-only allocation in 5-point increments. It keeps only allocations that meet the expected-return objective and minimum reserve-eligible weight, then returns the feasible allocation with the lowest volatility. A result is a model output based on estimates, not an investment recommendation.

## R — Inputs, estimates, and sources

Meridian uses the four Lab 14 training sleeves and the course-authored inputs. Its objective is 6.5%; its reserve minimum is 3.0%.

The CSV universe uses monthly adjusted-close prices. Historical average returns are **estimates, not forecasts**.

| Ticker | Fund name | Role | Source | Download date |
| --- | --- | --- | --- | --- |
| BIL | SPDR Bloomberg 1-3 Month T-Bill ETF | Cash and reserve | Yahoo Finance Historical Data, Monthly Adj Close | 2026-10-20 |
| IEF | iShares 7-10 Year Treasury Bond ETF | Government bonds | Yahoo Finance Historical Data, Monthly Adj Close | 2026-10-20 |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Fixed income | Yahoo Finance Historical Data, Monthly Adj Close | 2026-10-20 |
| VT | Vanguard Total World Stock ETF | Equity | Yahoo Finance Historical Data, Monthly Adj Close | 2026-10-20 |

prices.csv puts date first, rows oldest first, and one adjusted-close column per ticker. The engine calculates monthly price returns, arithmetic mean return × 12, sample standard deviation × square root of 12, and pairwise correlations.

## Engine flowchart

~~~mermaid
flowchart TD
    A[prices.csv: date and adjusted closes] --> B[Monthly returns]
    B --> C[Historical estimates: mean x 12 and stdev x sqrt 12]
    C --> D[Correlation table]
    D --> E[Covariance matrix]
    F[Editable expected returns and reserve flags] --> G[All long-only 5-point mixes]
    E --> G
    H[Objective and reserve minimum] --> G
    G --> I{Meets both constraints?}
    I -- No --> G
    I -- Yes --> J[Calculate portfolio volatility]
    J --> K[Keep lowest-volatility feasible mix]
    K --> L[Streamlit answer and stability comparison]
~~~

## I — App and code design

portfolio.py keeps its Lab 14 baseline-printing behavior unchanged. It now also contains:

- long_only_mixes: creates every allocation that sums to 100% in 5-point steps.
- find_lowest_risk_mix: filters for return and reserve feasibility, then keeps the allocation with the lowest volatility.
- estimate_from_prices: estimates annualized return, volatility, and correlation from a price CSV, using all observations or the last 36 monthly returns.

app.py imports those functions and the Meridian inputs from portfolio.py; it does not copy the portfolio math. The page includes sidebar controls for objective, reserve minimum, CSV upload, and a last-36-month switch; editable expected-return boxes; reserve-eligible checkboxes; the current answer beside the answer as loaded; and the largest weight change when both are feasible.

Run the app with:

    python -m streamlit run app.py

## V — Meridian known-answer proof

The app search function reproduced both required training runs.

| Run | Bills / 10-year / IG / equity | Return | Volatility | Largest weight change |
| --- | --- | ---: | ---: | ---: |
| Meridian inputs as loaded | 0 / 20 / 25 / 55 | 6.51% | 9.44% | — |
| Equity return edited from 8.0% to 7.0% | 0 / 10 / 10 / 80 | 6.53% | 12.94% | 25 points |

The one-point lower equity-return estimate changed the selected allocation by 25 percentage points. This is estimation risk: the optimizer searches for a boundary solution that barely meets the return target, so a small expected-return change can select a different 5-point mix.

### Engine-reuse proof

I temporarily changed the IG-bond/equity correlation from 0.25 to 0.50 in both cells of portfolio.py. The search then returned:

| Bills / 10-year / IG / equity | Return | Volatility |
| --- | ---: | ---: |
| 0 / 40 / 0 / 60 | 6.52% | 9.73% |

I restored both correlation cells to 0.25. This proves the app uses the imported engine rather than a second copy of the calculations.

## My CSV universe — provisional app reading

The workspace does not contain a separate Project 2 mandate, so I have **not claimed the following provisional test is my final mandate answer**. To test the uploaded CSV, I used the app's Meridian defaults: 6.5% objective, 3.0% reserve minimum, with BIL and IEF checked as reserve-eligible. The Project 2 objective and hard constraint must replace those defaults before a final personal decision is made.

| Window | BIL / IEF / LQD / VT | Return | Volatility | Reserve eligible |
| --- | --- | ---: | ---: | ---: |
| All monthly returns | 60 / 0 / 0 / 40 | 6.80% | 6.02% | 60.0% |
| Last 36 monthly returns | 85 / 0 / 0 / 15 | 6.80% | 1.78% | 85.0% |

The largest all-months versus last-36-months weight change is **25 points**. These figures will change when the actual Project 2 objective and constraint are entered.

## Explain the search function

The search validates the correlation table and builds a covariance matrix. It then examines every long-only 5-point mix. It skips a mix below the return objective or reserve minimum. For every surviving mix, it calculates volatility; if that volatility is lower than the best feasible volatility seen so far, it saves the mix. After every mix is checked, it returns the saved mix, or None when no mix is feasible.

## Partner attack response

**Partner's stressed input:** Pending an actual partner test in class.

**Two-sentence response template:** “When the [asset] estimate changed from [old] to [new], the lowest-risk feasible mix changed from [old weights] to [new weights]. I would treat that instability as a reason to pilot rather than adopt the mix until I have stronger forward-looking return evidence.”

## My call

**Provisional call: Pilot, not adopt.** A one-point lower equity estimate changed 25 percentage points of the Meridian allocation, and the preliminary CSV analysis also changed 25 points between all-history and last-36-month inputs. I would reconsider after entering the actual Project 2 mandate and reviewing forward-looking return assumptions, the data source, and the minimum liquidity/reserve requirement.

## Estimation risk — Learn on my own

Estimation risk is the possibility that a decision is distorted because estimated returns, volatilities, or correlations differ from future reality. Optimizers amplify small expected-return errors because they often choose a mix at the minimum-return boundary; a small estimate change can make one mix infeasible and another barely feasible. In this lab, a one-point lower equity estimate moved 25 percentage points of the Meridian mix, which is a concrete example of that amplification.

Before adopting an optimizer output, I would need reliable and current data, a justified forward-looking return process, stress tests across multiple time periods, and client approval of the objective and hard constraint.
