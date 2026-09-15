# Oracle — Lab 07: Comparable-Company Policy and Implied Range

## Lab 07 Asbury case

Run command: `python lab_07_comps.py`

The calculator uses the frozen Asbury Automotive case required in Lab 07, rather than Oracle. Its editable inputs are the December 31, 2024 closing prices and FY2024 total GAAP diluted EPS supplied in the course case. It calculates peer P/E, the peer median, Asbury's implied range, and each leave-one-out result without using cash or debt.

Expected checked results are AutoNation P/E of 10.037825x, Group 1 P/E of 11.450149x, a median of 10.743987x, an implied Asbury range of $215.81–$246.18, and a median-implied price of $231.00. Removing GPI leaves the AutoNation reference estimate of $215.81, a -$15.18 change from the full-peer estimate.

## P/E explanation

P/E equals a company's price per share divided by its annual diluted earnings per share (EPS). Price is the market value of one share; EPS is profit attributable to each diluted share. The multiple states how many dollars investors pay per dollar of annual earnings. Applying a peer's P/E to the target's EPS converts a comparable earnings valuation into an implied target share price.

P/E normalizes for different company sizes: a $400 share is not necessarily more highly valued than a $100 share when their per-share earnings differ. It complements the Oracle DCF because the DCF reflects my forecast and assumptions, whereas a comparable P/E reflects prices the market assigns to similar companies' earnings. A difference is a prompt to examine assumptions and peer selection, not to average the two values automatically.

P/E is useful only when earnings are positive and the companies have comparable business economics and the same earnings definition. It can mislead with negative EPS, unusual one-time profits or losses, differing growth and risk, capital structure, or accounting choices. Therefore, a lower P/E is a question to investigate, not automatically evidence of a better investment.

## Asbury peer policy

My policy is to use publicly traded franchised vehicle retailers with meaningful new/used vehicle sales plus service and parts, positive annual earnings, and total GAAP diluted EPS on a consistent split basis. I will document material differences in scale, geography, financing, and acquisitions rather than conceal them in an average.

- **AutoNation — use.** It has comparable vehicle-retail operations and relevant service/parts activity. Its AutoNation Finance operation is a business difference to monitor, but its core economics fit Asbury sufficiently for this small teaching comparison.
- **Group 1 — qualify and use.** It has the same core franchised-retail and service/parts model, but its U.K. operations and the 2024 acquisition of 54 Inchcape dealerships create material geographic and acquisition differences. Those differences make it a qualified peer rather than an exact match, which is why the leave-one-out result matters.

Group 1 has the higher P/E. Removing it should reduce the median-implied Asbury value; the calculator confirms this. With AutoNation alone, the output is one reference estimate, not a valuation range. The observed Asbury price being inside the two-peer range does not establish fair value or an investment recommendation.

## Evidence

- [Course worked comparable-company case](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/teach-comps-worked-example.md) — P/E definition, peer-policy evidence, frozen inputs, and check values.
- [Lab 07 directions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/lab-07-comparable-policy.md) — required calculation, validation, and reflection criteria.
