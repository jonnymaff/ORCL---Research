# Oracle — Lab 06: Sensitivity, Reverse DCF, and Conditional Recommendation

## Inputs and price

| Input | Value | Status, as-of date, and exact locator |
|---|---:|---|
| Starting FCFF | ($19,667m) | **Calculated estimate** for fiscal year ended May 31, 2026: operating cash flow $31,977m + after-tax interest $4,019m − capital expenditures $55,663m. [Oracle FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/1341439/000119312526277521/orcl-20260531.htm), Consolidated Statements of Cash Flows and Statements of Operations. |
| FCFF path, Years 1–5 | ($10,000m), $0m, $10,000m, $18,000m, $24,000m | **Forecast assumption.** A direct path is used because a percentage growth rate applied to negative FCFF would compound the loss. |
| WACC | 10.0% | **Estimate / placeholder**, not a copied vendor WACC. A company-specific estimate remains to be completed. |
| Terminal growth | 3.0% | **Assumption** for long-run economic growth; below WACC. |
| Cash | $31,289m | May 31, 2026; FY2026 10-K, Consolidated Balance Sheets. |
| Debt | $129,541m | May 31, 2026; FY2026 10-K, Consolidated Balance Sheets and debt note. |
| Diluted shares | 2,914m | FY2026; 10-K earnings-per-share note, diluted weighted-average shares. |
| ORCL share price | $156.72 | September 10, 2026, 17:30:33 UTC; market quote. [Oracle quote page](https://www.nasdaq.com/market-activity/stocks/orcl). |

## Company DCF result

`python dcf.py` produces a base-case value per diluted share of **$50.32**. This is 0.32× the $156.72 market price, outside the course's 0.5×–2× reasonableness band.

The input I distrust most is the five-year FCFF recovery path, particularly the $24.0bn Year-5 FCFF assumption. Oracle is in a capital-intensive cloud build-out, so the timing and scale of conversion from cloud growth to positive free cash flow are uncertain.

## Sensitivity grid — value per diluted share

| WACC \ terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 9% | $53.51 | $67.40 | $86.85 |
| 10% | $40.28 | $50.32 | $63.72 |
| 11% | $30.05 | $37.59 | $47.27 |

The base case is the center cell. Value falls as WACC rises and rises as terminal growth rises. The corner range is $30.05–$86.85 per share.

## Reverse DCF

The reverse DCF targets **$156.72** per share. Because the model uses a direct FCFF path for a negative-FCFF company, it solves for a **uniform multiplier on every projected FCFF amount**, rather than a uniform growth-rate shift. The solution is **2.2660×** within the 0.0×–5.0× bisection bracket.

Inputs held fixed: starting FCFF, WACC, terminal growth, cash, debt, diluted shares, and the shape of the five-year FCFF path. This is one assumption set consistent with the market price, not proof that the shares are mispriced.

## Conditional call

**Watch / defer. Initiate if** Oracle demonstrates a credible path toward roughly 2.3× the modeled FCFF recovery while net debt stabilizes or declines; **otherwise defer.** Monitor quarterly free-cash-flow conversion after cloud-infrastructure capital expenditures and the net-debt trend.
