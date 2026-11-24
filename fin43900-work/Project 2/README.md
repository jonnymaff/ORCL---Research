# Project 2 — Conservative U.S. ETF Mandate

> **AI use:** OpenAI Codex was used to scaffold the application structure, calculations, documentation, and reproducibility checks. The analysis, parameter choices, and final decision are the student's responsibility and must be reviewed before submission.
>
> **Education only — not investment advice.** This classroom application is an illustrative portfolio-analysis tool, not a solicitation, recommendation, or individualized investment recommendation.

## Committee decision

**Pilot** the constrained defensive-factor ETF process at a **10%–20% sleeve allocation**, provided the portfolio continues to pass all mandate limits and its net expected return remains at least the compliant equal-weight baseline after stated costs. Pause the process if volatility exceeds 12%, fixed income falls below 20%, a single ETF exceeds the approved position limit, or net expected return falls below the equal-weight baseline.

The GitHub-visible decision numbers and baseline comparison are in [`docs/decision-output.md`](docs/decision-output.md). The data provenance and point-in-time signal are in [`docs/data-card.md`](docs/data-card.md).

## Run the app

```bash
python -m pip install -r requirements.txt && python -m streamlit run app.py
```

Open the local URL Streamlit reports. In the sidebar, change **Maximum single ETF weight** to `30%`: the constrained portfolio changes from a mandate pass to a mandate fail because USMV is 35%.

## Repository map

| Location | Purpose |
| --- | --- |
| `app.py` | Streamlit application and decision dashboard |
| `model/portfolio.py` | Deterministic portfolio, risk, mandate, and stress calculations |
| `data/point_in_time_inputs.csv` | Dated input fixture used by the app |
| `docs/decision-memo.md` | Committee-ready decision memo |
| `docs/validation-and-ai-use.md` | Validation, AI-use disclosure, and changed-input record |
| `docs/video-scripts.md` | Recording-ready outlines for the three required videos |
| `docs/decision-output.md` | GitHub-readable baseline and constrained-portfolio output |
| `docs/data-card.md` | Point-in-time signal and data-card details |
| `docs/lab-20-evidence.md` | Lab 20 evidence checklist; complete partner-only items there |
| `docs/manifest.md` | Submission manifest; replace placeholders with GitHub URLs after push |

## Reproducibility and limits

The input fixture is deliberately versioned and dated **2025-12-31** so the displayed signal is point-in-time. It is a classroom fixture: replace it with checked market data before treating any result as production-quality. Inputs are annualized estimates, not forecasts. The app does not fetch live market data, so reruns are deterministic.

## Recorded videos

- Video 1 - system/thinking change and checked AI output: [YouTube](https://youtu.be/cPcJPLwd_XA) | Transcript: `docs/Project 2 Video 1 Transcript.pdf`
- Video 2 - code walkthrough: [YouTube](https://youtu.be/ihTfunNZO9U) | Transcript: `docs/Project 2 Video 2 Transcript.pdf`
- Video 3 - committee presentation: [YouTube](https://youtu.be/CsO5onXSOtk) | Transcript: `docs/Project 2 Video 3 Transcript.pdf`

See `docs/manifest.md` for the GitHub transcript links.

## Archived video placeholders

- Video 1 — system/thinking change and checked AI output: **pending recording**
- Video 2 — code walkthrough: **pending recording**
- Video 3 — committee presentation opening with the live app: **pending recording**

Add YouTube URLs and transcript links to `docs/lab-20-evidence.md` after recording.
