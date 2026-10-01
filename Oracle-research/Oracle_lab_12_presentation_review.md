# Lab 12 — Oracle: Presentation Route and Review Record

**Purpose:** Use this as a short route through the existing analysis during the
partner presentation. It is a preparation aid, not a new valuation. AI should
remain closed during the actual presentation and questioning, as the lab directs.

## Preparation check — October 1, 2026

Before class, I reran `python oracle_lab_10_proforma.py` and
`python oracle_lab_11_sensitivity.py`. The base model still returns $8.13 per
common share; every FY2027E–FY2031E balance-sheet gap is $0.0m and the $10,000m
cash floor is met. The sensitivity rerun restores the same base result after
its six cases. These are preparation checks, not partner-review evidence.

## Six-stop presentation route

### 1. Target selection

I selected Oracle because its enterprise applications and OCI cloud-infrastructure
operations make its current investment cycle economically important to analyze.
The original question was whether Oracle can convert heavy OCI data-center spending
into durable free cash flow without sustained net-debt pressure. My initial view
was cautious because FY2026 capital expenditures were $55,663m while the calculated
FY2026 FCFF used in the earlier DCF was negative $19,667m.

### 2. Company and evidence

Oracle earns revenue from cloud applications and infrastructure, on-premise and
hybrid software, hardware, and related services. The key reporting base is the
Oracle FY2026 Form 10-K for the year ended May 31, 2026; all financial-statement
amounts in the pro-forma are USD millions. Useful anchors from the existing files:

| Evidence | FY2026 value | Why it matters |
|---|---:|---|
| Revenue | $67,357m | Starting level for the revenue forecast |
| Revenue growth | 17.3% | High recent growth; forecast decelerates rather than repeats it indefinitely |
| Net PP&E | $99,957m | Existing data-center asset base |
| Capital expenditures | $55,663m | Central OCI-investment / cash-conversion risk |
| Total debt | $129,541m | Makes financing treatment material |
| GAAP operating margin | 30.6% | Starting reference for margin assumptions |

Source: [Oracle FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/1341439/000119312526277521/orcl-20260531.htm), filed June 22, 2026. The model leaves FY2026 inventory unresolved rather than inventing an inventory-days forecast.

### 3. Pro-forma

The forecast uses revenue growth of 15%, 12%, 10%, 8%, and 6% for FY2027–31,
and operating margins of 30.5%, 30.5%, 31.0%, 31.0%, and 31.5%. The company-specific
driver is OCI data-center PP&E and its funding: capex starts at 70% of revenue,
then falls to 25% by FY2031 as the model assumes growing use of the capacity.

The three statements are linked. Revenue drives operating income; capex changes
PP&E and cash; cash below the $10,000m floor triggers debt draws; cash above the
$20,000m threshold is swept to debt repayment. The model calculates cash last,
and its base run reports a zero balance-sheet gap and a met cash floor in every
forecast year. In FY2031E, base revenue is $109,249.9m, operating income is
$34,413.7m, capex is $27,312.5m, debt change is negative $8,217.4m, and signed
FCFE is $4,264.9m.

### 4. Valuation

Keep these methods and their bases separate:

| Method | Result | Date / share basis | What it establishes / limitation |
|---|---:|---|---|
| Earlier FCFF DCF | $50.32 per diluted share | FY2026 inputs; 2,914m diluted weighted-average shares; compared in Lab 06 to a Sep. 10, 2026 $156.72 quote | Uses 10.0% WACC and 3.0% terminal growth. Its terminal value was 89.54% of EV, so the FCFF-recovery path is highly influential. |
| Qualified peer P/E reference | $159.94 per share | Sep. 10, 2026; Oracle FY2026 GAAP diluted EPS of $5.83; Microsoft P/E 27.434x | One peer only; Microsoft's business mix and scale make it a reference, not a peer-set range. |
| Pro-forma signed-FCFE value | $8.13 per common share | FY2026 opening balance sheet; 2,880m common shares; compared in Lab 10 to a Sep. 24, 2026 $138.74 quote | Uses 10.0% cost of equity and 2.5% terminal growth. It is highly dependent on the debt plug / cash sweep and terminal FCFE treatment. |

The methods differ because they use different cash-flow definitions, share bases,
dates, and assumptions. Do not average them. The pro-forma conclusion is conditional:
the model is below the recorded market quote, but that output should not be treated
as a stand-alone recommendation until the terminal FCFE and debt-repayment mechanics
are economically validated.

### 5. Sensitivity and drivers

Lab 11 reruns the full linked model after changing one independent driver at a
time. Every run maintained a zero balance-sheet gap and the minimum cash floor.

| Driver and stated range | FY2031 operating-profit span | FY2031 FCFE span | Value/share span |
|---|---:|---:|---:|
| Revenue growth, base path ±2.0 percentage points | $6,254.8m | $265.7m | $0.78 |
| Operating margin, base path ±1.0 percentage point | $2,185.0m | $1,772.6m | $5.18 |

Revenue growth is the larger operating-profit driver **over these chosen ranges**.
Operating margin is the larger FCFE/value driver **over these chosen ranges**. The
counterintuitive margin result is model mechanics: a higher margin raises operating
income, creates more cash, and triggers more debt repayment; because signed FCFE
includes debt change, the incremental repayment lowers reported FCFE. That does
not mean a higher economic margin is harmful. It identifies the cash-sweep and
terminal-FCFE treatment as the next assumption to research.

### 6. Interpretation

My supported conclusion remains **watch / defer**, not a mechanical buy or sell.
I would become more confident in a positive view if quarterly evidence showed that
OCI revenue growth and utilization convert into durable positive free cash flow
while net debt stabilizes or falls. I would revise the model if capex remains near
FY2026 levels for longer, cash conversion fails to improve, or the current
debt-repayment / terminal-FCFE approach is not economically sustainable.

## In-class review record — complete only after the partner exchange

### As presenter

| Area | Question | Concise answer |
|---|---|---|
| Selection/evidence | Why select Oracle despite high cloud-build-out spending? | OCI capex, PP&E growth, and funding create the cash-conversion question I am testing. FY2026: $67,357m revenue, $55,663m capex, $99,957m net PP&E, and $129,541m debt. |
| Model/valuation | Do negative free cash flow and high debt make the valuation unreliable? | They make it conditional, not a buy. I remain watch / defer: the $8.13 signed-FCFE value depends on capex normalization, the debt plug/cash sweep, and terminal FCFE. |
| Sensitivity | Why does higher margin lower FCFE/value? | Extra cash is swept to debt repayment. Since signed FCFE includes debt change, repayment lowers FCFE mechanically; it does not mean higher margins are harmful. |
- What I will keep, revise, or investigate after feedback — and why:
  - Investigate the durability of OCI cash conversion, the capex-normalization path, and the economic reasonableness of the terminal-FCFE/debt-repayment mechanics. The question about negative cash flow and debt confirms that these are the central limitations rather than a reason to claim a mechanical buy or sell result.
- Does the review change my valuation conclusion or research priority? Why?
  - The conclusion remains watch / defer. The review reinforces the research priority: validate the free-cash-flow recovery and debt path before relying on the model's per-share value.
- The question that made me reconsider something and what I now understand better:
  - The question about negative free cash flow and debt made me reconsider how much weight to place on the signed-FCFE valuation. I now understand more clearly that the cash-sweep/debt-plug mechanics and terminal-FCFE treatment must be validated alongside operating-profit growth.

### As reviewer

- Partner's stated conclusion: long PepsiCo because its beverage and snack portfolio provides diversified revenue, its beverage position is viewed as a duopoly, and existing customer/bottler arrangements may support revenue stability.

| Area | Question | Concise answer |
|---|---|---|
| Selection/evidence | Does the duopoly claim cover all Pepsi revenue? What supports revenue stability? | The duopoly rationale is mainly beverages; snacks diversify revenue. Customer/bottler arrangements are supporting evidence, not a guarantee of sales. |
| Model/valuation | Does the valuation already reflect brand, distribution, and diversification strength? | The long thesis requires that those strengths continue to produce revenue growth and margins; diversification alone does not guarantee upside. |
| Sensitivity | Does the driver ranking depend on the tested ranges? | Yes. Growth reaches net revenue first; margin reaches operating profit first; both flow through cash flow to value. Rankings are range-dependent, not probabilities. |

- Source or calculation opened and checked; result: [PepsiCo Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/77476/000007747626000035/pep-20260613.htm) reports $43,624m net revenue, 7.3% reported growth, and 16.6% operating margin for the first 24 weeks of FY2026. It discusses customer-volume rebates and bottler funding based on annual targets and contract terms, but does not establish guaranteed future revenue or a company-wide duopoly.
- My explanation back of my partner's conclusion, main driver, and biggest limitation:
  - Pepsi's conclusion is long. The main driver is resilient revenue from a diversified beverage-and-snack portfolio, with beverage competitive position and customer/bottler arrangements supporting the thesis. The biggest limitation is whether those strengths are already reflected in the valuation and whether beverage-market logic can be extended to the entire company.
- Evidence-backed strength:
  - Strength: the thesis identifies an economic mechanism—revenue resilience and margin performance—rather than relying only on a brand-name claim. The Form 10-Q check provides current reported revenue growth, operating-margin, and customer/bottler-program evidence that is relevant to testing that mechanism.
- Specific next improvement:
  - Separate the beverage-duopoly rationale from the snack business in the forecast, quantify the contribution of each assumption to value, and explain whether the valuation already prices in the expected resilience. Treat customer/bottler arrangements as support to investigate, not as proof that future sales are guaranteed.

For the three questions, make the wording specific to the partner's company
and displayed evidence. A usable check records the exact source or calculation
opened, what was compared or recomputed, and whether it supported the claim.
