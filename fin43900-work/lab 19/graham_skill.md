# Graham screen — Lab 19 skill

Use the five annual SEC EDGAR 10-K rows printed by `edgar_buffett.py`. Do not estimate missing facts.

- Latest current ratio must be at least 2.0: `AssetsCurrent / LiabilitiesCurrent`.
- Net income must be positive in every available one of five years.
- Net income must grow from the first year to the last.

Return `pass`, `fail`, or `not known`; `not known` is required when the needed fact or five-year set is missing. Write the Graham memo only from values printed by the collector.

Threshold kept: **2.0**. It is the stated conservative liquidity rule; the 1.0 probe is shown in the app as a design-choice comparison.
