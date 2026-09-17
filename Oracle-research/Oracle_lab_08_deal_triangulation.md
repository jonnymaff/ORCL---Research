# Oracle — Lab 08: Deal Evidence and Valuation Triangulation

## Problem, date, and initial peer policy

**Target:** Oracle Corporation (ORCL). **Valuation and comparison date:** September 10,
2026. Oracle earns money by selling enterprise applications and infrastructure through cloud,
on-premise, and hybrid deployments, as well as software licenses, hardware, and related
services. Its FY2026 Form 10-K, Item 1 / Note 1, describes Oracle Cloud Applications and
Oracle Cloud Infrastructure as integrated application and infrastructure services.

My initial policy is to consider only listed operating companies with material enterprise
software *and* public/private/hybrid cloud-infrastructure operations, positive full-year
reported diluted EPS, USD share prices and USD annual EPS on the same quoted-share basis.
I will qualify differences in customer mix, segment mix, scale, capital intensity, and
non-enterprise businesses. I will exclude an otherwise plausible company if a compatible
price/EPS basis cannot be established without an unverified currency conversion.

The remaining research question is whether a company whose cloud platform and enterprise
applications overlap Oracle's, but whose other segments are substantial, can be a useful
single-peer reference rather than a peer-set valuation.

## Candidate decisions and source evidence

| Candidate | Decision | Business evidence opened | Reasoned fit / limitation |
|---|---|---|---|
| Microsoft (MSFT) | **Qualify and use** | [FY2026 Form 10-K, Item 1 and Note 18](https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm) describes the Intelligent Cloud segment as public, private, and hybrid server products and cloud services, including Azure; it also includes Dynamics enterprise applications. | This overlaps Oracle's enterprise cloud infrastructure and applications economics. Microsoft is much larger and has material Productivity, personal-computing, gaming, search/advertising, and LinkedIn businesses. Its P/E is therefore a qualified reference, not a claim of equivalence. |
| SAP SE (SAP) | **Exclude** | [SAP 2025 Form 20-F, Earnings per Share](https://www.sec.gov/Archives/edgar/data/1000184/000110465926020058/R24.htm) reports FY2025 diluted EPS of **€6.10**; [SAP’s annual-report release](https://news.sap.com/2026/02/sap-releases-integrated-report-2025-and-files-annual-report-2025-on-form-20-f-with-the-u-s-securities-and-exchange-commission/) describes SAP as an enterprise-applications and business-AI company. | SAP is a credible enterprise-application candidate, but its ERP/SaaS emphasis is not the same as Oracle’s integrated OCI infrastructure and applications. More importantly, the NYSE SAP ADR price is in USD while the reported EPS is in euros. I did not introduce an unverified EUR/USD conversion, so it is not a compatible price/EPS input under my policy. |

The Microsoft annual filing was filed August 4, 2026, so FY2026 annual GAAP diluted EPS was
public by the September 10 comparison date. SAP's 20-F was filed February 26, 2026. Oracle's
FY2026 10-K was filed June 22, 2026. These filings, not an AI-generated ticker list, provide
the business and earnings evidence.

## Inputs and calculation

All included prices are closing prices on September 10, 2026, and all included EPS figures
are full-year reported GAAP diluted EPS available by that date. They are USD per ordinary
quoted share for ORCL and MSFT; no quarterly or adjusted earnings are used.

| Company | Closing price, September 10, 2026 | Annual diluted EPS and fiscal year | Publication date / source locator |
|---|---:|---:|---|
| Oracle (target) | $152.94 | $5.83, FY ended May 31, 2026 | [Oracle FY2026 10-K, Note 14 — Earnings per Share](https://www.sec.gov/Archives/edgar/data/1341439/000119312526277521/orcl-20260531.htm), filed June 22, 2026; [historical price](https://stockanalysis.com/stocks/orcl/history/). |
| Microsoft (peer) | $492.44 | $17.95, FY ended June 30, 2026 | [Microsoft FY2026 10-K, Note 2 — Earnings per Share](https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm), filed August 4, 2026; [Microsoft investor-relations historic lookup](https://microsoft.gcs-web.com/). |

Run command: `python lab_08_deal_triangulation.py`

Output:

```text
Microsoft P/E: 27.433983x
One valid peer: reference estimate (not a range): $159.94
```

## Validation

I checked Microsoft by hand: **$492.44 / $17.95 = 27.433983x**. Applying that multiple to
Oracle’s $5.83 annual diluted EPS gives **$159.94** ($159.9355 before rounding), a $7.00
premium to Oracle's same-date $152.94 close. This is one qualified-peer reference estimate,
not a range.

I predicted that removing the only usable peer, Microsoft, would leave no P/E estimate. The
calculator confirms: `Remove Microsoft (MSFT): no estimate; no peers remain.` That result is
why I have not disguised this as a diversified peer median or filled the gap with SAP.

## DCF comparison, challenge, and judgment

| Method | Oracle result and date | Main assumption or limitation |
|---|---|---|
| Week 3 DCF | $50.32 per diluted share; FY2026 inputs, compared with the September 10, 2026 $152.94 market close | The modeled five-year FCFF recovery and 10% WACC dominate the result; terminal value was 89.54% of enterprise value. |
| Peer P/E | $159.94 single-peer reference on September 10, 2026 | One qualified peer; Microsoft’s broader business mix and different scale mean its P/E is not a valuation range for Oracle. |

**Provisional call:** **watch / defer; do not initiate yet.** The qualified Microsoft reference
is close to Oracle's market price, but it does not overcome the DCF's large shortfall because
the DCF is explicitly a fragile, capital-intensive FCFF-recovery scenario. The difference
does not justify averaging $50.32 and $159.94: the methods answer different questions and
the peer evidence is only a one-company reference.

**Skeptical-colleague challenge:** The weakest supported assumption is treating Microsoft’s
27.43x consolidated P/E as transferable to Oracle despite Microsoft’s non-Oracle-like
businesses and different cash-flow profile. **Question that could change my decision:** Can
Oracle demonstrate, with reported quarterly cash flow and capital-expenditure evidence, a
durable path to the FCFF recovery embedded in the DCF without further net-debt pressure?

**Judgment of the challenge: accept.** The source evidence confirms the business overlap, but
also confirms Microsoft's three reportable segments and non-cloud activities; that supports a
qualified reference only. What could most easily change my mind is two or more quarters of
credible positive free-cash-flow conversion after cloud-infrastructure capex, with stable or
falling net debt, or a second peer with compatible USD annual GAAP EPS and a clearly similar
cloud/infrastructure mix. Conversely, weaker cash conversion, rising debt, or evidence that
Microsoft's premium reflects segments Oracle does not have would reinforce the deferral.

## Reflection

Oracle’s P/E is usable because its FY2026 reported diluted EPS is positive. Microsoft adds a
market-based cross-check: at its qualified P/E, Oracle’s reported earnings imply a value near
the September 10 market close. The DCF adds a different warning: its value depends on an
assumed recovery from negative FCFF and places unusually high weight on terminal value. The
evidence therefore supports monitoring rather than a mechanical valuation blend. I withhold a
defensible peer range because one admitted peer is a reference, not a peer set.
