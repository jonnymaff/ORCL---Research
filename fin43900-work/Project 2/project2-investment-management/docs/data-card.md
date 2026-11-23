# Data Card — Defensive-Factor Eligibility Signal

| Field | Description |
| --- | --- |
| Signal | Trailing 12-month total-return direction as of 2025-12-31 |
| Rule | Positive trailing return supports equity-factor eligibility; IEF and SHY serve as defensive Treasury ballast |
| Window stress | A six-month trailing-return check is run in the stress table. If a proposed equity ETF loses positive eligibility at scheduled review, pause the process and review/rebalance before continuing. |
| Decision use | Signal informs the eligible factor sleeve; it does not override the mandate's risk limits |
| Universe | SPY, ESGU, USMV, QUAL, IEF, and SHY |
| Point in time | 2025-12-31; no inputs after that date are used by the fixture |
| Source | Versioned classroom fixture in `data/point_in_time_inputs.csv` |
| Known limitation | Values are illustrative, annualized inputs and six-/twelve-month return fixtures; replace them with checked vendor data and preserve the source export before final submission |
| Refresh policy | Refresh only at the scheduled committee review; rerun validation and retain an input snapshot after every refresh |

The signal intentionally remains simple and auditable. It is not a claim that trailing performance predicts future returns.
