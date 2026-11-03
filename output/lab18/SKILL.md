---
name: legend-investor
description: Use when asked to evaluate a public-company business through the Lab 18 Buffett lens using five years of SEC EDGAR 10-K facts, reproducible checks, and a short judgment memo.
---

# Legend Investor

## Purpose

Use this skill to assess the **quality of a business**, not its stock price. The
Python collector performs every numeric task from SEC EDGAR 10-K facts; the
model's role is only to interpret those printed results in a short memo.

## Required workflow

1. From this folder, run the collector for the requested ticker:

   ```powershell
   python edgar_buffett.py TICKER --json TICKER_analysis.json
   ```

2. Read the JSON output. Do not supplement it with web searches, price data,
   FAskills, paid services, estimates, or remembered financial figures.
3. Create `TICKER_buffett_memo.md` using the memo format below.
4. Run the app with `python -m streamlit run app.py` and confirm it displays
   the table, chart, checks, and memo without an unsupported-number warning.

## Non-negotiable data rules

The collector must remain the single source of numbers. It uses only annual
10-K observations, labels results by fiscal-year-end date, and keeps the last
five fiscal years. When the same annual period appears in more than one
filing, the newest filing wins.

| Measure | Required XBRL tag rule |
|---|---|
| Revenue | `RevenueFromContractWithCustomerExcludingAssessedTax`, then `Revenues` |
| Net income | `NetIncomeLoss` |
| Operating cash flow | `NetCashProvidedByUsedInOperatingActivities` |
| Capital spending | `PaymentsToAcquirePropertyPlantAndEquipment`, then `PaymentsToAcquireProductiveAssets` |
| Equity | `StockholdersEquity` |
| ROE | `net income / year-end equity` |
| Owner earnings | `operating cash flow - capital spending` |

Never replace a missing value with an estimate. A missing source fact remains
`not found`; an invalid or incomplete calculation/check remains `not known`.
For zero or negative equity, report ROE as `not known`.

## Memo requirements

Write in a restrained Buffett-like business-analysis voice. Include:

- A title naming the ticker and company.
- One clear verdict: **own the business**, **watch it**, or **pass**.
- A brief evidence-based discussion of the reported revenue, net income,
  ROE, owner earnings, and the three checks where available.
- A direct statement when owner earnings cannot be judged because a required
  input is `not found`.
- A reminder that the verdict considers business quality only, not price or
  valuation.
- A final personal line: `Decision: I [do/do not] trust this verdict because ...`

Every numeric claim must appear exactly in the collector's output. Do not
invent precision, calculate extra ratios in prose, or cite a number the script
did not print.
