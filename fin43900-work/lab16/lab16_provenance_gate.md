# Lab 16 — Provenance Gate

## D — Decision question

**On the day I would have traded, what did this data actually say, and how much of what I see now came later?**

The month measured is the period the index describes. The publication date is the day that result became available to an investor. A March value published on 10 April may describe March, but it was not knowable on a 31 March decision date.

## R — Training inputs and rules

The training table is a fictional card-spend index for AAA, BBB, and CCC. The decision date is 31 March 2026. A row is knowable only when its publication date is on or before that date.

The point-in-time rules are applied in order:

1. Quarantine a row with no ticker.
2. Remove an exact duplicate.
3. Remove a row published after the decision date.
4. For each ticker and month with multiple publications, keep the latest publication that was knowable on the decision date.

The signal is the percentage change from each ticker's prior month to its latest month in the selected panel.

## I — Filter design

asof.py uses only the standard library. The editable inputs at the top are the 12 training rows and the decision date.

| Function | Purpose |
| --- | --- |
| publication_date | Converts publication text to a date for comparison. |
| remove_missing_tickers | Quarantines rows with blank tickers. |
| remove_exact_duplicates | Removes a repeated row with the same ticker, month, date, and index. |
| remove_post_decision_publications | Removes information unavailable on the decision date. |
| keep_latest_vintage | Keeps the latest known revision for each ticker/month. |
| as_of_panel | Applies all four rules in the required order and produces the funnel. |
| naive_panel | Uses all available publications while ignoring publication date. |
| signals | Calculates the latest-month percentage change for each ticker. |

Run it with:

    python asof.py

## V — Known-answer proof

Running the file produced this required row funnel:

| Funnel step | Rows removed |
| --- | --- |
| Quarantined: no ticker | 11 |
| Exact duplicate | 7 |
| Published after 31 March | 3, 8, 10 |
| Older vintage replaced by a revision | 2 |

The as-of panel remaining after all four rules is: **1, 4, 5, 6, 9, 12**.

| Ticker | As-of signal | Naive signal |
| --- | --- | --- |
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | -1.02% (February) | -5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

The key revision is AAA February. Row 2 was published on 10 March at 104.0, but row 4 revised the same February observation to 103.0 on 25 March. Because row 4 was known by the decision date, it replaces row 2. Keeping row 2 would incorrectly make AAA's as-of signal +2.97%.

## Code explanation — Rule 4 revisions

keep_latest_vintage groups data by the pair of ticker and month. For each row, it checks whether a value for that pair has already been saved. If not, it saves the row. If a row is published later than the saved row, it records the saved row as replaced and saves the later row instead; otherwise it records the current row as replaced. The function finally sorts the selected panel by original row number for readable output.

**Self-quiz:** Why must rule 3 run before rule 4?  
**Answer:** A revision published after the decision date cannot replace the older known value. Filtering on publication date first ensures the latest vintage is the latest one that was actually available then.

## Swap and break

The required partner test is to set the decision date in asof.py to 2026-04-15, rerun the file, and compare the columns. With that later date, the point-in-time signals match the naive signals ticker by ticker:

| Ticker | Later-date as-of signal = naive signal |
| --- | --- |
| AAA | +5.83% |
| BBB | -5.15% |
| CCC | +1.82% |

The decision date should be restored to 2026-03-31 after the test. This test demonstrates that the difference between the original columns was data not yet published at the original decision date.

## Point-in-time — Learn on my own

### What is look-ahead bias?

Look-ahead bias occurs when a historical analysis uses information that was not available at the time of the supposed decision. It makes a backtest appear to have known the future.

### How do event time, publication time, and revisions create it?

Event time is the month a statistic measures; publication time is when it became public. A revision is a later publication that changes a previously released value for the same month. A point-in-time analysis must use the latest version published by the decision date, not the version visible today.

### AAA example

On 31 March, AAA's latest knowable month was February, revised to 103.0 on 25 March; compared with January's 101.0, that produced +1.98%. The naive +5.83% instead uses March's 109.0, which was published on 10 April, so it could not have informed a 31 March trade.

## Reflection

The rule that removed the most decision-relevant row was the publication-date rule: it removed AAA's March row 3, which creates the overly positive naive signal. A backtest built on the naive column would claim stronger, earlier signal knowledge than an investor had and could falsely make a strategy look profitable or timely.

## Thursday preview

Thursday's version will apply this same four-stage filter to my own monthly ALFRED series. For each observation, I will preserve both the month measured and its vintage/publication date so the decision-date filter can distinguish originally available values from later revisions.
