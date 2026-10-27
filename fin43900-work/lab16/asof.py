"""Point-in-time data filter for the Lab 16 training card-spend index.

Run with: python asof.py
"""

from collections import defaultdict
from datetime import date
from calendar import month_name


# Editable inputs
DECISION_DATE = date.fromisoformat("2026-03-31")

ROWS = [
    {"row": 1, "ticker": "AAA", "month": "2026-01", "published": "2026-02-10", "index": 101.0},
    {"row": 2, "ticker": "AAA", "month": "2026-02", "published": "2026-03-10", "index": 104.0},
    {"row": 3, "ticker": "AAA", "month": "2026-03", "published": "2026-04-10", "index": 109.0},
    {"row": 4, "ticker": "AAA", "month": "2026-02", "published": "2026-03-25", "index": 103.0},
    {"row": 5, "ticker": "BBB", "month": "2026-01", "published": "2026-02-10", "index": 98.0},
    {"row": 6, "ticker": "BBB", "month": "2026-02", "published": "2026-03-10", "index": 97.0},
    {"row": 7, "ticker": "BBB", "month": "2026-02", "published": "2026-03-10", "index": 97.0},
    {"row": 8, "ticker": "BBB", "month": "2026-03", "published": "2026-04-10", "index": 92.0},
    {"row": 9, "ticker": "CCC", "month": "2026-01", "published": "2026-02-10", "index": 110.0},
    {"row": 10, "ticker": "CCC", "month": "2026-02", "published": "2026-04-05", "index": 112.0},
    {"row": 11, "ticker": "", "month": "2026-02", "published": "2026-03-10", "index": 99.0},
    {"row": 12, "ticker": "CCC", "month": "2026-02", "published": "2026-03-10", "index": 111.0},
]


def publication_date(row):
    """Return a row's publication date as a date object."""
    return date.fromisoformat(row["published"])


def remove_missing_tickers(rows):
    """Quarantine rows with no ticker and return kept rows plus removed row numbers."""
    removed = [row["row"] for row in rows if not row["ticker"]]
    return [row for row in rows if row["ticker"]], removed


def remove_exact_duplicates(rows):
    """Keep the first occurrence of a fully identical data row."""
    kept = []
    seen = set()
    removed = []
    for row in rows:
        identity = (row["ticker"], row["month"], row["published"], row["index"])
        if identity in seen:
            removed.append(row["row"])
        else:
            seen.add(identity)
            kept.append(row)
    return kept, removed


def remove_post_decision_publications(rows, decision_date):
    """Remove rows that were published after the decision date."""
    removed = [row["row"] for row in rows if publication_date(row) > decision_date]
    return [row for row in rows if publication_date(row) <= decision_date], removed


def keep_latest_vintage(rows):
    """Keep the latest publication for each ticker/month and list replaced rows."""
    latest_by_series = {}
    replaced = []
    for row in rows:
        key = (row["ticker"], row["month"])
        if key not in latest_by_series:
            latest_by_series[key] = row
        elif publication_date(row) > publication_date(latest_by_series[key]):
            replaced.append(latest_by_series[key]["row"])
            latest_by_series[key] = row
        else:
            replaced.append(row["row"])
    panel = sorted(latest_by_series.values(), key=lambda row: row["row"])
    return panel, sorted(replaced)


def as_of_panel(rows, decision_date):
    """Apply the four point-in-time rules in order and return panel plus funnel."""
    after_ticker, no_ticker = remove_missing_tickers(rows)
    after_duplicates, duplicates = remove_exact_duplicates(after_ticker)
    after_date, after_decision = remove_post_decision_publications(
        after_duplicates, decision_date
    )
    panel, older_vintages = keep_latest_vintage(after_date)
    funnel = [
        ("Quarantined: no ticker", no_ticker),
        ("Exact duplicate", duplicates),
        (f"Published after {decision_date.isoformat()}", after_decision),
        ("Older vintage replaced by a revision", older_vintages),
    ]
    return panel, funnel


def naive_panel(rows):
    """Use all available publications, ignoring publication date, for comparison."""
    after_ticker, _ = remove_missing_tickers(rows)
    after_duplicates, _ = remove_exact_duplicates(after_ticker)
    panel, _ = keep_latest_vintage(after_duplicates)
    return panel


def signals(panel):
    """Return each ticker's latest month and percent change from its previous month."""
    by_ticker = defaultdict(list)
    for row in panel:
        by_ticker[row["ticker"]].append(row)
    result = {}
    for ticker, ticker_rows in by_ticker.items():
        ordered = sorted(ticker_rows, key=lambda row: row["month"])
        if len(ordered) < 2:
            continue
        previous, latest = ordered[-2:]
        result[ticker] = {
            "month": latest["month"],
            "change": (latest["index"] / previous["index"] - 1) * 100,
        }
    return result


def readable_month(month_text):
    """Convert a YYYY-MM month to the displayed month name."""
    return month_name[int(month_text.split("-")[1])]


def print_funnel(funnel):
    """Print filter rules, count of removals, and row numbers."""
    print("Row funnel")
    for label, row_numbers in funnel:
        row_text = ", ".join(str(number) for number in row_numbers) or "none"
        print(f"  {label}: {len(row_numbers)} removed (row {row_text})")


def print_panel(panel):
    """Print the remaining as-of rows."""
    print("\nAs-of panel")
    print("  Row  Ticker  Month measured  Published on  Index")
    for row in panel:
        print(
            f"  {row['row']:>3}  {row['ticker']:<6}  {row['month']:<14}  "
            f"{row['published']:<12}  {row['index']:.1f}"
        )


def print_signals(label, panel):
    """Print point-in-time or naive signals."""
    print(f"\n{label}")
    for ticker, result in signals(panel).items():
        print(
            f"  {ticker}: {result['change']:+.2f}% "
            f"({readable_month(result['month'])})"
        )


def main():
    panel, funnel = as_of_panel(ROWS, DECISION_DATE)
    print_funnel(funnel)
    print_panel(panel)
    print_signals("As-of signals", panel)
    print_signals("Naive signals (ignores publication date)", naive_panel(ROWS))


if __name__ == "__main__":
    main()
