# Lab 13 — Portfolio Mandate Defense

## Statement types: S1–S10

| Statement | Type | Reason |
| --- | --- | --- |
| S1 | Objective | The seven-year horizon frames the time available to pursue the reserve's return goal and tolerate risk. |
| S2 | Objective | CPI + 4% net of costs over rolling five years is the stated return objective and measurement period. |
| S3 | Hard constraint | The quarterly payout and the required twelve-month liquidity reserve impose a minimum eligible allocation. |
| S4 | Objective | The 60/40 global-equity/U.S.-investment-grade-bond benchmark is a performance reference, not an explicit allocation limit. |
| S5 | Hard constraint | It expressly prohibits borrowing, shorts, and derivatives. |
| S6 | Hard constraint | It sets an 8% maximum exposure to a single non-exempt company across its securities. |
| S7 | Hard constraint | It caps annual turnover at 25% unless the committee approves more. |
| S8 | Hard constraint | It requires at least 90% to be redeemable within five business days. |
| S9 | Unverifiable promise | A calendar-year loss cap is stated, but no return measure or breach rule defines how to test or enforce it. |
| S10 | Missing | It rules out several preferences but does not say what the pilot should optimize, so the decision criterion is absent. |

## Investment policy statement: what it is and how it works

An investment policy statement (IPS) is the client-approved decision framework for managing a portfolio. It records objectives, constraints, governance, and how success is evaluated, so implementation can be checked against the client's mandate rather than an adviser's assumptions.

For Meridian, S1 and S2 define the horizon and return objective; S4 supplies the benchmark. S3 and S5–S8 are operational and portfolio constraints. S9 is a risk-related statement that needs a measurable definition before it can constrain a portfolio. S10 identifies the missing optimization preference. Together, these are the IPS inputs the portfolio team needs before optimization.

## Known-answer verification and probe

Running `python mandate.py` produces the required 3.0% reserve minimum. Candidates A, B, and C match the given table: A passes every checkable rule, B fails three rules, and C fails one rule. The program groups Acme bonds and stock by issuer, producing B's 9.0% company exposure and C's 8.0% exposure.

For the required probe, I temporarily changed Candidate A's Cash weight to -2 and its global equity index fund weight to 64. The lowest weight became -2.0 and failed long-only; the reserve-eligible total remained 10.0 and every other rule continued to pass. I then restored A's original weights.

## Self-quiz

The line I checked most closely was `issuer_weights[issuer] = issuer_weights.get(issuer, 0) + weight`. It adds each security's weight to the total for that issuer, so Acme's bonds and stock are tested together instead of separately. The `get(..., 0)` supplies zero the first time an issuer occurs.

## Attack portfolio D

Candidate D is 3% Cash and 97% Global equity index fund, with every other holding at 0%. It passes every rule in `mandate.py`: it totals 100%, is long-only, has the 3% reserve minimum, is fully redeemable within five business days, and has no non-exempt single-company exposure.

The objection holds because a 97% equity portfolio is radically different from the 60% global equity / 40% U.S. investment-grade bond benchmark and could expose the reserve to a much larger drawdown than the CIO intended. S4 decides the objection: the CIO must say whether the benchmark is only a reporting comparator or a risk/asset-allocation guide. Against a partner's passing candidate, I would cite S4 whenever it made the portfolio materially unlike the stated 60/40 reference without a stated reason.

## Question for the CIO

Is the 60/40 benchmark merely an evaluation benchmark, or must the portfolio remain within specified risk and allocation ranges around it? If it is a binding risk guide, I would build around a diversified equity-and-investment-grade-bond mix near 60/40; if it is only an evaluation comparator, I would choose the mix that best supports CPI + 4% net of costs subject to the liquidity and other explicit constraints.

## Reflection

A portfolio can pass every checkable rule and still be wrong because a checker only enforces statements that have measurable definitions. It cannot infer the intended risk budget, the role of the benchmark, or an unexpressed optimization goal; Candidate D demonstrates that gap.

I was least sure about S4. A benchmark is crucial to judging performance and risk, but the wording does not say it is an allocation band or a hard limit, so I classified it as an objective/performance reference rather than inventing a constraint.
