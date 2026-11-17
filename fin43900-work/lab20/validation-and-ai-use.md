# Validation and AI Use

> **AI use:** OpenAI Codex was used to create the initial app scaffold, calculation functions, documentation outline, and review checklist. The student is responsible for verifying each input, calculation, source, and final decision.
>
> **Education only — not investment advice.** This application is a classroom exercise and must not be used as individualized investment advice.

## Baseline and mandate checks

The app evaluates equal weight, transparent 60/40 SPY/IEF, and the constrained defensive-factor portfolio under the same dated fixture and cost assumption. The decision output documents each portfolio's net expected return, annualized volatility, largest position, pass/fail verdict, and rule failure.

Manual review checkpoints:

1. Portfolio weights sum to 100%.
2. Expense ratios and trading costs are subtracted from gross expected return.
3. The correlation matrix is symmetric; equity pairs use 0.70, equity/fixed-income pairs use 0.15, and IEF/SHY uses 0.55.
4. The maximum-position, equity-floor, fixed-income-floor, and volatility-cap rules are each evaluated independently.
5. Set the app control to a 30% maximum position: the 35% USMV holding must fail the maximum-position rule.

## Stress run

The app reports four scenarios: base case, expected returns reduced by 150 basis points, trading cost raised to 50 basis points, and the single-ETF limit tightened to 30%. The process stops or is rejected if any mandate rule fails or if net expected return is below the compliant equal-weight baseline after costs.

## Locked Changed-Input Record

**Draft status:** AI-generated for final human review under the revised course policy. Add the actual commit SHA and GitHub URL after publishing the repository.

| Required field | Record |
| --- | --- |
| Load-bearing input selected | Maximum single-ETF position limit |
| Old value and units | 35% maximum portfolio weight per ETF |
| New value and units | 30% maximum portfolio weight per ETF |
| Prediction | The proposed portfolio's net expected return (6.75%) and volatility (9.77%) will not change because the holdings and return inputs do not change. Its mandate verdict will change from PASS to FAIL because USMV remains 35%, above the new 30% limit. |
| Expected effect on decision | The pilot recommendation will reverse to pause/reject until the allocation is rebalanced below the tightened limit. |
| Prediction commit SHA and URL | Pending GitHub publication — replace with the commit that contains this prediction before presenting the record. |
| Before-output path/link | `docs/decision-output.md` — constrained portfolio: 6.75% net expected return, 9.77% volatility, PASS at the 35% cap. |
| After-output path/link | App stress table, “Position limit tightened to 30%” — constrained portfolio: 6.75% net expected return, 9.77% volatility, FAIL. |
| Actual result and decision effect | The predicted verdict reversal occurs. The changed constraint does not alter estimated return or risk, but it makes the existing 35% USMV holding non-compliant. The recommendation is therefore paused/rejected until rebalanced. |
| Why actual result matched the prediction | The model evaluates the position limit separately from the return and covariance calculations. Changing only that limit leaves calculated decision numbers unchanged and changes only the mandate-rule result. |

## Test record

| Test | Expected outcome | Status |
| --- | --- | --- |
| Default app run | Three portfolios and stress table render | Review-ready deterministic result |
| Position cap = 30% | Constrained portfolio fails maximum-position rule | Reviewed against `model/portfolio.py` logic |
| Position cap = 35% | Constrained portfolio passes all listed rules | Reviewed against `model/portfolio.py` logic |
| README command | Stranger can start the app using only README | Final reviewer should run once in a clean environment |
