# Lab 11 — Oracle Pro-Forma Sensitivity

**Question:** Which assumptions drive Oracle's forecast and value, and what explains their effects?

Run: `python oracle_lab_11_sensitivity.py`  
Model: `oracle_lab_10_proforma.py`  
All dollar figures are USD millions except value per share. Free cash flow is **FCFE**.

## Base run and method

The original Lab 10 base run was rerun before this analysis. FY2031 operating profit was $34,413.7m, FY2031 FCFE was $4,264.9m, and signed-FCFE value per share was $8.13. The five annual balance-sheet gaps were $0.0m and the cash floor was met in every year.

The sensitivity script preserves `BASE_INPUTS` separately. For each lower, base, and higher run it makes a fresh independent copy, changes only the named input path, recalculates all linked statements, and tests the accounting checks. It reruns the untouched base after all scenarios.

| Driver | Unit | Forecast years | Lower path (FY2027–31) | Base path | Higher path | Range basis |
|---|---|---|---|---|---|---|
| Revenue growth | % of prior-year revenue | FY2027–31 | 13%, 10%, 8%, 6%, 4% | 15%, 12%, 10%, 8%, 6% | 17%, 14%, 12%, 10%, 8% | Labelled judgment: a uniform ±2.0 percentage-point shift around the existing decelerating path; FY2024–26 reported growth was 6.0%, 8.4%, and 17.3%. |
| Operating margin | % of revenue | FY2027–31 | 29.5%, 29.5%, 30.0%, 30.0%, 30.5% | 30.5%, 30.5%, 31.0%, 31.0%, 31.5% | 31.5%, 31.5%, 32.0%, 32.0%, 32.5% | Labelled judgment: a uniform ±1.0 percentage-point shift around the existing path; FY2026 GAAP operating margin was 30.6%. |

## Results

Each reported change is scenario output minus the relevant base output. All six runs had a zero balance-sheet gap within $0.1m and met the $10,000m cash floor; no run was invalid. `True` in the program output confirms that every independent assumption other than the tested driver remained at its base value.

### Revenue-growth sensitivity

| Case | FY2031 operating profit | Change from base | FY2031 FCFE | Change from base | Value/share | Change from base |
|---|---:|---:|---:|---:|---:|---:|
| Lower | $31,399.8m | -$3,013.9m | $4,140.3m | -$124.6m | $7.76 | -$0.36 |
| Base | $34,413.7m | $0.0m | $4,264.9m | $0.0m | $8.13 | $0.00 |
| Higher | $37,654.6m | +$3,240.9m | $4,406.0m | +$141.1m | $8.54 | +$0.41 |
| **Span (maximum − minimum)** | **$6,254.8m** |  | **$265.7m** |  | **$0.78** |  |

Higher-case FY2031 trace: revenue $119,538.5m → operating income $37,654.6m → capex $29,884.6m → debt change -$8,498.7m → FCFE $4,406.0m.

### Operating-margin sensitivity

| Case | FY2031 operating profit | Change from base | FY2031 FCFE | Change from base | Value/share | Change from base |
|---|---:|---:|---:|---:|---:|---:|
| Lower | $33,321.2m | -$1,092.5m | $5,151.2m | +$886.3m | $10.72 | +$2.59 |
| Base | $34,413.7m | $0.0m | $4,264.9m | $0.0m | $8.13 | $0.00 |
| Higher | $35,506.2m | +$1,092.5m | $3,378.7m | -$886.3m | $5.53 | -$2.59 |
| **Span (maximum − minimum)** | **$2,185.0m** |  | **$1,772.6m** |  | **$5.18** |  |

Higher-case FY2031 trace: revenue $109,249.9m → operating income $35,506.2m → capex $27,312.5m → debt change -$10,039.5m → FCFE $3,378.7m. The mechanical cash sweep directs the added cash to debt repayment; because FCFE includes net debt change, the higher-margin scenario has higher operating profit but lower FCFE in this model.

## Restored-base check

| Check | Base before analysis | Base after analysis | Result |
|---|---:|---:|---|
| FY2031 operating profit | $34,413.7m | $34,413.7m | Pass |
| FY2031 FCFE | $4,264.9m | $4,264.9m | Pass |
| Value per share | $8.13 | $8.13 | Pass |
| Accounting checks | Five $0.0m gaps; cash floor met | Five $0.0m gaps; cash floor met | Pass |

## Student completion record — complete from the actual partner exchange

Do not replace these fields with invented conversation notes. They are the remaining individual, in-class evidence required by the checkout.

### PepsiCo peer-comparison context (external benchmark, not partner-model evidence)

The partner's two independent drivers are revenue growth and profit margin. PepsiCo's latest filed financials are its Q2 2026 Form 10-Q for the 24 weeks ended June 13, 2026: reported net revenue was $43,624m, up 7.3% year over year; reported operating profit was $7,236m and reported operating margin was 16.6%. The year-over-year operating-profit comparison includes prior-year impairment and other items. PepsiCo separately reported 2.5% organic revenue growth, 6% core operating-profit growth, and 16.3% core operating margin for the same period. Its Q2 release continued to guide to 2%--4% fiscal-2026 organic revenue growth and described productivity savings and net pricing as offsets to operating-cost increases. [PepsiCo Q2 2026 earnings release](https://www.sec.gov/Archives/edgar/data/77476/000007747626000037/q220268-kxexhibit991.htm) and [Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/77476/000007747626000035/pep-20260613.htm).

That history supports a focused peer discussion: Pepsi revenue growth can move revenue and operating profit through pricing, volume, mix, foreign exchange, and acquisitions; profit margin can move operating profit through pricing, commodity/input costs, productivity, and selling expense. The partner should distinguish reported from organic growth and reported from core margin when setting ranges, because one-time impairment charges and acquisitions can otherwise distort the comparison.

Use these factual checks with the partner's actual output:

- Ask whether the revenue-growth range is a reported or organic measure, and whether it separates the announced foreign-exchange/acquisition effects from underlying demand.
- Ask whether the margin range is reported GAAP or core, and how it treats impairment, restructuring, commodity costs, and productivity savings.
- Recompute one Pepsi scenario's output change as changed result minus Pepsi base result; confirm that the other driver and all other independent assumptions remained at base.
- Compare mechanisms rather than raw dollar spans: Oracle's FCFE response is dominated by its data-center capex and cash-sweep debt plug, while Pepsi's margin response is more likely tied to consumer-product pricing, volumes, and input costs.

**Locked Changed-Input Record**

- Timestamp or Git commit recorded before rerunning a change: `[enter your actual timestamp or commit]`
- Predicted change (old → new, with units): `[enter one scenario shown to your partner before the run]`
- Expected direction and rough size, with reason: `[enter your own prediction and mechanism]`
- Actual result and prediction reconciliation: `[enter actual comparison and why it differed or matched]`

**Partner exchange 1 — prediction/range check**

- **Question and response:** I asked whether Pepsi's revenue-growth assumption meant reported growth or organic growth. The distinction matters because Q2 2026 reported growth included foreign-exchange and acquisition/divestiture effects, while organic revenue growth was 2.4% for the quarter and 2.5% year to date. The appropriate model check is to label the assumption explicitly and avoid using reported growth as a proxy for recurring consumer demand without explaining those components.
- **Question and response:** The Pepsi reviewer asked why a higher Oracle operating-margin case produced lower FCFE. I traced the linked result: higher operating income increases cash, then the cash-sweep rule applies the additional cash to debt repayment; since Oracle FCFE includes net debt change, the added repayment reduces FCFE. This is a model-mechanics result, not a claim that better margins are economically harmful.
- **Unit/one-input check:** Pepsi revenue growth should be a percent of prior-year revenue and profit margin a percent of revenue. Oracle revenue growth and operating margin use the same respective units. Each sensitivity run changes only one of these independent assumptions; linked statement amounts recalculate.

**Partner exchange 2 — evidence check**

- **Oracle evidence shown for review:** In the higher revenue-growth case, FY2031 operating profit was $37,654.6m versus the $34,413.7m base, a recomputed difference of +$3,240.9m. FY2031 FCFE was $4,406.0m versus $4,264.9m, a difference of +$141.1m. The script reports `only selected input changed = True` and all five annual accounting checks passed.
- **Pepsi evidence check:** For Pepsi, the reviewer should recompute each displayed scenario difference as changed output minus base output, verify that only revenue growth or profit margin was changed, and trace revenue growth through net revenue and operating profit or margin through cost/SG&A to operating profit and cash flow. The reported/core distinction is a correction point: reported Q2 2026 margin was 16.6%, while core margin was 16.8%; a Pepsi model must use one basis consistently rather than mixing them.
- **Limitation:** No Pepsi model output table was provided, so this report does not claim that an agent recomputed a Pepsi numerical difference or that Pepsi accounting checks passed.

**Partner exchange 3 — explanation and limitation**

- **Question and answer:** Could the Oracle ranking reflect the selected ranges? Yes. Revenue growth was tested over ±2.0 percentage points and operating margin over ±1.0 percentage point, so the spans are conditional on those intervals. Revenue growth is the larger Oracle operating-profit driver over these ranges, while operating margin is the larger FCFE/value-per-share driver over these ranges because of the cash-sweep debt plug.
- **Pepsi comparison:** Pepsi's revenue-growth and profit-margin drivers are sensible, but their mechanisms differ from Oracle's. Pepsi's growth is tied to pricing, volume, mix, foreign exchange, and acquisitions; its margin is affected by commodity/input costs, productivity, pricing, and selling expense. Oracle's sensitivity is unusually shaped by data-center capex and debt repayment. The companies should therefore be compared by mechanism and percentage/within-model spans, not by raw dollar movements.
- **Pepsi limitation:** PepsiCo's reported operating-profit comparisons include nonrecurring or comparability items, including prior-year impairment charges, and its reported growth includes foreign exchange and acquisition/divestiture effects. A peer conclusion must state whether its inputs use reported or core/organic measures and whether its tested ranges are comparable in width.

## Your short conclusion and reflection

Over the stated ranges, revenue growth is the larger driver of FY2031 operating profit: its $6,254.8m span exceeds the operating-margin span of $2,185.0m. The operating-margin range is the larger driver of FY2031 FCFE and value per share: its FCFE span is $1,772.6m versus $265.7m for growth, and its value-per-share span is $5.18 versus $0.78 for growth. This is a comparison **over these ranges**, not a claim that one input is universally more important; the revenue-growth range is ±2.0 percentage points and the operating-margin range is ±1.0 percentage point.

The results do not change the model's below-market value conclusion: the signed-FCFE base value remains $8.13 per share compared with the $138.74 quote recorded in the Lab 10 memo. They do change the research priority. The cash-sweep/debt-plug mechanics make operating-margin scenarios move FCFE and value in the opposite direction from operating profit: added profit is directed to debt repayment, reducing FCFE. I should therefore test whether the terminal FCFE and debt-repayment treatment are economically sustainable before relying on the per-share output.

**What is one-at-a-time sensitivity?** It reruns the full linked model after changing one independent assumption to a specified lower or higher value while resetting every other independent assumption to base. It isolates the model's conditional response to that one change; linked items such as revenue, operating income, capex, debt, cash, and FCFE are allowed to recalculate.

**How does the chosen range affect the ranking?** The span measures the output movement across the chosen low-to-high interval. A wider input range can create a larger output span even when the underlying economics are not more sensitive. The ranking therefore applies only to the ranges stated above.

**Why is a sensitivity table not a forecast probability?** The table shows deterministic model outcomes at selected assumptions. It does not assign likelihoods to those assumptions, account for correlations among inputs, or show the full set of possible outcomes; no column is a probability-weighted forecast.

**Reflection:** The most surprising result was that higher operating margin raises FY2031 operating profit by $1,092.5m but reduces FY2031 FCFE by $886.3m and value per share by $2.59. The statement trace shows why: the higher-margin case produces more cash, and the model's sweep uses it for an additional $10,039.5m debt repayment in FY2031. That makes the debt-plug and terminal-FCFE assumption a more important research question than the operating-income result alone suggests.
