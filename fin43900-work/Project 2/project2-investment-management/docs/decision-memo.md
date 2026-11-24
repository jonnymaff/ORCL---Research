# Decision Memo — Conservative U.S. ETF Mandate

> **AI use:** OpenAI Codex assisted with application scaffolding, documentation structure, and calculation review prompts. The analysis and decision are the student's responsibility.
>
> **Education only — not investment advice.** This is a classroom analysis, not individualized investment advice.

**To:** Investment Committee  
**As of:** 2025-12-31  
**Decision:** **Pilot** the constrained defensive-factor ETF process at a **10%–20% sleeve allocation**.

## Mandate

The objective is a lower-volatility U.S. equity sleeve with Treasury ballast. The universe is SPY, ESGU, USMV, QUAL, IEF, and SHY. The benchmark is 60% SPY / 40% IEF. The risk measure is annualized volatility under the documented correlation assumption. Limits are: equity allocation at least 60%, fixed income allocation at least 20%, no ETF above 35%, and annualized volatility at or below 12%.

## Evidence

The constrained portfolio holds USMV 35%, QUAL 25%, ESGU 15%, IEF 15%, and SHY 10%. Its net expected return is **6.75%** after expense ratios and a 10-basis-point trading-cost assumption on 35% turnover. Its annualized volatility is **9.77%**, and it passes every mandate rule.

The equal-weight baseline returns **6.71%** with **9.56%** volatility and passes. The transparent 60/40 SPY/IEF baseline returns **6.93%** with **11.56%** volatility but fails the single-ETF concentration rule because SPY is 60%.

The data card documents the point-in-time 2025-12-31 trailing-return eligibility signal. The stress run checks estimates, a shorter six-month signal window, trading costs, and constraints. Reducing expected returns by 150 basis points lowers the proposed portfolio's expected return but leaves structural mandate rules intact. The six-month fixture leaves all three proposed equity ETFs eligible; a future loss of positive eligibility triggers a pause and review. Tightening the single-ETF cap to 30% makes the proposed 35% USMV allocation fail; this is a clear stop-and-rebalance condition.

## Conditions and monitoring

Do not advance the pilot if annualized volatility exceeds 12%, fixed income is below 20%, an ETF weight exceeds the applicable limit, or net expected return falls below the compliant equal-weight baseline after stated costs. At review, monitor the mandate verdict, estimated costs, the point-in-time signal, factor concentration, and the documented input source.

## Submission evidence

The three Project 2 videos and transcript PDFs are linked in `docs/manifest.md` and `docs/lab-20-evidence.md`. The changed-input record is documented in `docs/validation-and-ai-use.md` with its GitHub prediction commit.
