# Burry screen — Lab 19 skill

Use the five annual SEC EDGAR 10-K rows printed by `edgar_buffett.py`. Do not estimate missing facts.

- Operating cash flow must be at least net income every year.
- Latest liabilities must be no more than twice equity: `Liabilities / StockholdersEquity <= 2`.

Return `pass`, `fail`, or `not known`; `not known` is required when the needed fact or five-year set is missing. Write the Burry memo only from values printed by the collector.
