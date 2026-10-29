# Lab 17 — Point-in-Time Audit

## Decision question

Was each number in my series knowable on the day I would have traded on it — and may Project 2 use it?

## Known-answer check

On 5 October 2026, the app returned the required last known observations:

| Series | Last date known | Value |
| --- | --- | ---: |
| BAA | September 2026 | 6.47 |
| FEDFUNDS | September 2026 | 3.75 |
| DGS10 | 2 October 2026 | 5.28 |
| MORTGAGE30US | 1 October 2026 | 7.28 |

The PAYEMS probe at 15 January 2025 returned December 2024 at **159,536** as then known. The current download has a lower December 2024 value, and the app reported **59** revised observations on shared dates. This confirms that the as-known download is not mistakenly reading today's data twice.

## My series data card — DGS10

| Field | Evidence |
| --- | --- |
| Series ID and source | [DGS10 — FRED](https://fred.stlouisfed.org/series/DGS10); source: Board of Governors of the Federal Reserve System (US), H.15 Selected Interest Rates. |
| What it measures | The market yield on U.S. Treasury securities with a 10-year constant maturity, quoted on an investment basis. It is relevant to the portfolio because Treasury yields influence the yields and prices of IEF and LQD. |
| Units | Percent; not seasonally adjusted; daily frequency. |
| Publication lag | On 30 September 2026, the app's ALFRED vintage ended at 29 September 2026, 5.26%. Therefore, a 30 September decision cannot assume knowledge of that same day's DGS10 value; use the last value actually present in the vintage. |
| Revisions | In the app comparison from the 30 September 2026 vintage to today's FRED download, 0 shared-date values changed. The FRED page nevertheless says that all data are subject to revision, so the backtest must retain the ALFRED as-of rule. |
| Download date | 29 October 2026. |
| Three values checked by hand | Checked against the FRED page: 27 October 2026 = 4.99%; 26 October 2026 = 5.00%; 23 October 2026 = 5.00%. |

## Fresh-eyes partner attack

**Field my partner trusts least:** Revisions — “I trust the revisions least because the historical interest rate values shown today might not be the same as the values originally reported.”

**Two-sentence answer with evidence:** That concern is supported by the app: in the PAYEMS check, December 2024 was 159,536 as known on 15 January 2025, while today's download is lower, and the comparison reports 59 changed values on shared dates. For DGS10, the app found 0 changed values on shared dates between the 30 September 2026 vintage and today's download, but I will still use the ALFRED vintage on every decision date because the FRED page says that all data are subject to revision.

## Project 2 call

**Admit with an as-of rule:** DGS10 may be used in Project 2 only as the last non-missing observation contained in the ALFRED vintage available on the decision date; a same-day yield that has not yet appeared in that vintage is excluded. I would quarantine it if a later review finds material vintage changes, or if the strategy requires an intraday/same-day signal that the daily H.15 release cannot have supplied.

## Reflection

The app separates the observation date from the data vintage: the ALFRED request fixes the vintage with `vintage_date`, while the FRED request supplies the series as it reads today. For DGS10, the 30 September vintage ending at 29 September makes the publication lag visible; a backtest using today's history could overstate timeliness by assuming the 30 September yield was known on that date, and could overstate stability if later revisions occur.

“Cleaned the data” is not a data card because it does not identify the source, measure, units, observation/publication timing, or revision history. Those fields are what make a potential information leak visible before analysis begins.
