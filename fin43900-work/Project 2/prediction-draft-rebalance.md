# Changed-Input Prediction Draft: Tighter Position Limit and Rebalance

**Status:** Draft prepared with AI-assisted wording. Do not label this an AI-off Locked Changed-Input Record if the course requires the prediction itself to be written without AI. The student should rewrite and independently commit their final AI-off prediction before performing the official run.

## Input change

Lower the maximum permitted portfolio weight for a single ETF from **35%** to **30%**. Rebalance the portfolio by reducing the ETF currently held at 35% by 5 percentage points and reallocating that amount among other eligible ETFs.

## Prediction

> I predict that lowering the maximum single-ETF weight from 35% to 30% and rebalancing the excess weight will make the portfolio less concentrated because no single ETF will exceed 30% of the portfolio.
>
> I expect the portfolio's estimated return to decrease if the 5 percentage points removed from the previously largest holding are allocated to ETFs with lower expected returns. The exact change in estimated return will depend on the specific ETFs receiving the reallocated weight. If the receiving ETFs have higher expected returns than the reduced holding, the expected return could instead increase.
>
> The portfolio's volatility may also change because the new weights alter both the contribution of each ETF's volatility and the portfolio's correlation exposure. I expect diversification to improve, but I will confirm the resulting volatility and mandate verdict only after running the rebalanced portfolio.

## What this test requires

This prediction requires an actual weight change, not merely changing the maximum-position slider. In the current app, moving the slider from 35% to 30% does **not** automatically reallocate the 5% excess weight; it leaves USMV at 35% and changes the mandate verdict to FAIL. To test this prediction, specify the receiving ETF weights, update the proposed weights in `model/portfolio.py`, and rerun the app.

## Pre-run checklist

1. Choose the recipient ETF(s) and state the exact new weights; all weights must total 100%.
2. Check that the new largest holding is no greater than 30%.
3. Commit and push the student's final AI-off wording before the official run.
4. Run the rebalanced portfolio and record actual net expected return, volatility, concentration, and mandate verdict.
