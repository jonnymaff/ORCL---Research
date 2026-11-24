# Validation and AI Use

> **Official-run update (2026-11-23):** The 30% maximum-position test was completed locally after the student reported publishing the prediction to GitHub. The official observed result is recorded below. Before submission, paste the actual pre-run prediction commit SHA and GitHub URL into the Locked Changed-Input Record; this local environment does not have Git available to verify it.

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

The app reports five scenarios: base case, expected returns reduced by 150 basis points, a six-month signal-window check, trading cost raised to 50 basis points, and the single-ETF limit tightened to 30%. The process stops or is rejected if any mandate rule fails, net expected return is below the compliant equal-weight baseline after costs, or a proposed equity ETF loses positive eligibility at a scheduled signal-window review.

## Locked Changed-Input Record (historical draft; superseded below)

The following draft table is retained as a record of the initial setup. For grading, use the **Superseding post-repush locked-record run** below, which cites the pre-run GitHub commit and records the official rerun result.

**Draft status:** This is a calculation-checked draft, not yet a locked course record. To create the required locked record, the student must turn AI off, write and commit their own prediction to GitHub, then perform and document the official changed-input run. Add that pre-run commit SHA and URL below. Do not represent the dry-run result currently listed as a pre-committed record.

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
| Actual result and decision effect | **Dry-run calculation only:** the predicted verdict reversal occurs. For the official record, replace this with the result observed after the pre-run prediction commit. The changed constraint does not alter estimated return or risk, but it makes the existing 35% USMV holding non-compliant. The recommendation is therefore paused/rejected until rebalanced. |
| Why actual result matched the prediction | In the dry run, the model evaluates the position limit separately from the return and covariance calculations. Changing only that limit leaves calculated decision numbers unchanged and changes only the mandate-rule result. Confirm this wording against the official post-commit run. |

## Official changed-input run result

**Changed input:** Maximum single-ETF position limit, reduced from 35% to 30%.

**Prediction commit:** [`aacaa0372fb610f369e3fa5e896c14cb9f393f33`](https://github.com/jonnymaff/ORCL---Research/commit/aacaa0372fb610f369e3fa5e896c14cb9f393f33)

| Observed output | Result |
| --- | --- |
| Net expected return | 6.75% |
| Annualized volatility | 9.77% |
| Largest ETF position | USMV, 35% |
| Mandate verdict | FAIL |
| Failed rule | Single ETF maximum position: USMV at 35% exceeds the 30% limit |
| Decision effect | Pause/reject the pilot until the portfolio is rebalanced below the applicable position limit. |

The observed result matched the prediction: changing only the maximum-position constraint did not change holdings, expected-return inputs, costs, or correlation assumptions, so return and volatility remained unchanged. It changed the compliance verdict because the existing 35% USMV holding exceeds the new 30% limit.

## Superseding post-repush locked-record run

**Run date:** 2026-11-23  
**Changed input:** Maximum single-ETF position limit, 35% to 30%  
**Prediction commit:** [`aacaa0372fb610f369e3fa5e896c14cb9f393f33`](https://github.com/jonnymaff/ORCL---Research/commit/aacaa0372fb610f369e3fa5e896c14cb9f393f33). This rerun, not any earlier run, is the official run for the Locked Changed-Input Record.

| Observed output | Post-repush rerun result |
| --- | --- |
| Net expected return | 6.75% |
| Annualized volatility | 9.77% |
| Largest ETF position | USMV, 35% |
| Mandate verdict | FAIL |
| Failed rule | Single ETF maximum position: USMV at 35% exceeds the 30% limit |
| Decision effect | Pause/reject the pilot until the portfolio is rebalanced below the 30% position limit. |

**Result check:** The rerun matched the prediction. Only the constraint changed, so the return and volatility calculations remained unchanged; the compliance verdict changed because the 35% USMV weight exceeds the new 30% maximum.

## Test record

| Test | Expected outcome | Status |
| --- | --- | --- |
| Default app run | Three portfolios and stress table render | Review-ready deterministic result |
| Position cap = 30% | Constrained portfolio fails maximum-position rule | Reviewed against `model/portfolio.py` logic |
| Position cap = 35% | Constrained portfolio passes all listed rules | Reviewed against `model/portfolio.py` logic |
| README command | Stranger can start the app using only README | Final reviewer should run once in a clean environment |
