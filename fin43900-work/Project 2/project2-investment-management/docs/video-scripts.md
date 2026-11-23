# Project 2 Video Recording Outlines

Use these as speaking outlines, not as a substitute for the required recordings. Before recording, replace the bracketed fields and open the app locally with `python -m streamlit run app.py`.

## Required opening statement for every video

> AI use: OpenAI Codex assisted with application scaffolding, documentation structure, and calculation-review prompts. The analysis and decision are mine.
>
> Education only -- not investment advice. This is a classroom analysis, not individualized investment advice.

## Video 1 -- system/thinking change and checked AI output

1. Give the required opening statement.
2. State the original idea and how the mandate became more specific: lower-volatility U.S. equity with Treasury ballast, a 60/40 SPY/IEF benchmark, a 12% volatility cap, 60% equity minimum, 20% fixed-income minimum, and a 35% position limit.
3. Show one Codex-produced item you personally checked: the model's base-case outputs. Explain that you reran the model and confirmed the proposed portfolio is 6.75% net expected return, 9.77% volatility, and PASS at the 35% cap.
4. Explain the changed-input prediction: tightening the position limit to 30% should leave return and volatility unchanged but switch the verdict to FAIL because USMV is 35%.
5. Show the result, name the stop/rebalance condition, and point viewers to the GitHub commit that locked your AI-off prediction before this run.

## Video 2 -- code walkthrough

1. Give the required opening statement.
2. Walk through `data/point_in_time_inputs.csv`: dated fixture, expected return, volatility, expenses, 12-month and six-month signal fields.
3. Walk through `model/portfolio.py`: portfolio weights, return after expenses and trading costs, correlation assumptions, volatility calculation, independent mandate rules, and stress scenarios.
4. Walk through `app.py`: committee controls, three portfolios, data card, stress table, and recommendation gate.
5. Demonstrate changing the maximum position to 30% and explain why the proposed portfolio fails.

## Video 3 -- committee presentation

1. Start with the app visibly running live, then give the required opening statement.
2. State the decision: pilot at a 10%-20% sleeve allocation only while all mandate rules pass and net expected return is at least the compliant equal-weight baseline after costs.
3. Compare the proposal, equal-weight baseline, and 60/40 baseline. Explain that the 60/40 baseline fails concentration because SPY is 60%.
4. Show the point-in-time signal, six-month window check, and stress table.
5. State the monitoring triggers: volatility above 12%, fixed income below 20%, a position over its limit, return below equal weight after costs, or loss of positive eligibility at signal review.
6. State the recommendation and its limitations: classroom fixture only; refresh with preserved, checked vendor inputs before any real-world use.

## After recording

Upload each video to YouTube with transcripts enabled (or attach the transcript in the repository), then replace the corresponding rows in `docs/lab-20-evidence.md` and `docs/manifest.md` with the URLs.
