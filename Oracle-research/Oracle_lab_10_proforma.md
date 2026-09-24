# Lab 10 — Oracle Pro-Forma: Draft for Checkout

**Question:** What are five years of Oracle's statements worth, built from assumptions I can defend?

Run: `python oracle_lab_10_proforma.py`

This is a working Lab 10 draft, not investment advice. All dollar figures are USD millions.

## Filing sources and history

| Fiscal year | Filing | Revenue | Gross profit* | SG&A** | Net income | Inventory | PP&E, net | Oracle stockholders' equity |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2024 | [FY2024 10-K](https://www.sec.gov/Archives/edgar/data/1341439/000095017024075605/orcl-20240531.htm) | 52,961 | 37,818 | 9,822 | 10,467 | 334 | 21,536 | 8,704 |
| 2025 | [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1341439/000095017025087926/orcl-20250531.htm) | 57,399 | 40,472 | 10,253 | 12,443 | 303 | 43,522 | 20,451 |
| 2026 | [FY2026 10-K](https://www.sec.gov/Archives/edgar/data/1341439/000119312526277521/orcl-20260531.htm) | 67,357 | 44,336 | 9,949 | 17,087 | unresolved | 99,957 | 42,508 |

*Gross profit is calculated as revenue less the direct cloud/software, hardware, and services expenses that Oracle reports in its business-results table. It is a consistent analytical definition, not a consolidated-statement caption.

**SG&A is sales and marketing plus general and administrative expense. Oracle reports those separately.

History ratios, calculated from the filings:

| Ratio / field | FY2024 | FY2025 | FY2026 | Source / treatment |
|---|---:|---:|---:|---|
| Reported revenue growth | 6.0% | 8.4% | 17.3% | Revenue table above |
| Gross margin | 71.4% | 70.5% | 65.8% | Calculated from defined gross profit |
| SG&A ÷ gross profit | 26.0% | 25.3% | 22.4% | Calculated |
| Depreciation ÷ opening PP&E | 18.3% | 18.0% | 17.5% | FY2024: 3,129 ÷ FY2023 PP&E; FY2025: 3,867 ÷ FY2024 PP&E; FY2026: 7,623 ÷ FY2025 PP&E |
| Capital expenditures | 6,866 | 21,215 | 55,663 | Consolidated cash-flow statement |
| Reported tax rate | 10.9% | 12.1% | 12.6% | Tax provision ÷ pretax income |
| Inventory days | unresolved | unresolved | unresolved | Inventory is not separately reported in FY2026; do not manufacture a ratio. |

Before checkout, manually verify at least two entries in the linked filings (recommended: FY2026 revenue and PP&E) and replace `unresolved` if the FY2026 filing gives a separately reported inventory balance.

## Opening balance sheet (FY2026)

Cash 31,289; PP&E 99,957; other assets 130,513; debt 129,541; other liabilities 89,710; equity 42,508. Other assets and other liabilities are balancing groupings calculated from the FY2026 consolidated balance sheet, not invented operating accounts.

## Assumption set

| Assumption | Value | Label | Reason |
|---|---:|---|---|
| Revenue growth, FY2027–31 | 15%, 12%, 10%, 8%, 6% | judgment | FY2026 reported growth was 17.3%, driven by cloud demand; the path decelerates rather than extending one unusually high year forever. |
| Operating margin, FY2027–31 | 30.5%, 30.5%, 31.0%, 31.0%, 31.5% | judgment | FY2026 GAAP operating margin was 30.6%; the forecast preserves it initially and allows modest scale benefits later. |
| Depreciation ÷ opening PP&E | 7.63% | history | FY2026 depreciation of 7,623 ÷ FY2026 closing PP&E of 99,957. |
| Capex ÷ revenue, FY2027–31 | 70%, 55%, 40%, 30%, 25% | judgment | FY2026 capex was 82.6% of revenue as Oracle built OCI capacity. The forecast assumes investment remains exceptional but normalizes over time. |
| Tax rate | 19.9% | judgment | The FY2026 10-K discusses a 19.9% adjusted rate after excluding discrete items; it is more defensible for a recurring forecast than the 12.6% reported rate. |
| Other-assets change ÷ revenue change | 1.0% | judgment | No separate inventory forecast is appropriate; this small working-capital proxy avoids silently assuming no operating-asset investment. |
| Debt interest rate | 3.55% | history | FY2026 interest expense of 4,599 ÷ FY2026 total debt of 129,541. |
| Minimum cash / cash-sweep threshold | 10,000 / 20,000 | judgment | A conservative liquidity floor and explicit repayment point make the debt plug visible. |
| Cost of equity / terminal growth | 10.0% / 2.5% | judgment | Retains the course discount-rate convention; terminal growth remains below cost of equity. |
| Common shares outstanding | 2,880m | fact | FY2026 consolidated balance sheet. |

## Oracle-specific line

Oracle’s company-specific line is **OCI data-center PP&E and its funding**. The model forecasts capex, PP&E, and the associated automatic debt draw/cash sweep; it does not copy ABG’s floor-plan financing. This matters because FY2026 PP&E grew to $100.0bn and capex reached $55.7bn while Oracle expanded cloud capacity.

## Price comparison

The model returns $14.85 per common share. The current ORCL quote is $138.74, recorded September 24, 2026 at 17:20 UTC. On the same 2,880m common-share count, the model is below the market quote. This is a question, not a recommendation.

The FY2027E FCFE is **negative $21,289m**; FY2028E and FY2029E are effectively zero because new debt holds cash at the stated floor. The valuation discounts only positive FCFE and uses the positive FY2031E FCFE for its terminal value. A terminal value on a negative final cash flow would not be meaningful.

## Model checks

`python oracle_lab_10_proforma.py` prints a zero balance-sheet gap and a met cash floor for FY2027E through FY2031E. The break test—replacing FY2027E cash with opening cash—raises `FY2027E balance-sheet gap: 21289.0`; the valuation cannot continue on a broken balance sheet.

## Required partner review — complete in class

**Partner’s attack:** Your capex assumption falls from 70% of revenue in FY2027 to 25% by FY2031. Why is that decline reasonable when Oracle is still expanding OCI data-center capacity, and what evidence would make you keep capex higher for longer?

**My two-sentence answer:** I used a declining capex ratio because FY2026’s spending was unusually high during a major infrastructure buildout, and I expect revenue to grow into that capacity over time. I would revise the forecast if Oracle continues reporting capex near FY2026’s level without a clear improvement in cloud revenue growth or free-cash-flow conversion.

**My attack on my partner’s Johnson & Johnson model:** Your revenue-growth assumption needs to explain how Johnson & Johnson can sustain growth through patent expirations and biosimilar competition. Which products drive the forecast after those pressures, and what would make you lower the growth or margin assumption?

## Reflection prompts — complete in your own words

- **Label I would defend longest and why:** I would defend the judgment that Oracle’s data-center capex gradually becomes more productive over the long term. I am long Oracle because I believe its heavy investment in OCI capacity can create durable returns as cloud demand grows and the infrastructure is utilized more fully; however, I would revisit that view if capex stays elevated without improving free-cash-flow conversion.
- **One filing number that surprised me:** Oracle’s FY2026 capital expenditures of $55.7 billion surprised me because they were such a large share of revenue. That number makes the near-term cash-flow pressure clear, but it is also the reason long-term data-center ROI is the central question in this model.
