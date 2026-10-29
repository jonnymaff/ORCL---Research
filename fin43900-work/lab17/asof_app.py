"""FRED/ALFRED point-in-time rate viewer for Lab 17.

Run with: streamlit run asof_app.py
"""

from datetime import date
from io import StringIO

import pandas as pd
import requests
import streamlit as st


FRED_GRAPH_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
ALFRED_GRAPH_URL = (
    "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series_id}"
    "&vintage_date={vintage_date}"
)
DEFAULT_SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}


@st.cache_data(show_spinner=False, ttl=60 * 60)
def download_today(series_id):
    """Download a series as FRED displays it today."""
    url = FRED_GRAPH_URL.format(series_id=series_id)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return tidy_csv(response.text, series_id)


@st.cache_data(show_spinner=False, ttl=60 * 60)
def download_as_known_on(series_id, vintage_date):
    """Download the latest ALFRED vintage available on vintage_date."""
    url = ALFRED_GRAPH_URL.format(series_id=series_id, vintage_date=vintage_date)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return tidy_csv(response.text, series_id)


def tidy_csv(csv_text, series_id):
    """Return DATE and numeric value columns, treating FRED's '.' as missing."""
    frame = pd.read_csv(StringIO(csv_text), na_values=".")
    if frame.empty or len(frame.columns) < 2:
        raise ValueError("FRED returned no observations for this series ID.")
    date_column = frame.columns[0]
    value_column = series_id if series_id in frame.columns else frame.columns[-1]
    frame = frame[[date_column, value_column]].copy()
    frame.columns = ["DATE", "value"]
    frame["DATE"] = pd.to_datetime(frame["DATE"], errors="coerce")
    frame["value"] = pd.to_numeric(frame["value"], errors="coerce")
    return frame.dropna(subset=["DATE"]).sort_values("DATE").reset_index(drop=True)


def last_observation(frame, start_date):
    """Return the latest non-missing row from start_date onward, if available."""
    visible = frame[(frame["DATE"].dt.date >= start_date) & frame["value"].notna()]
    return None if visible.empty else visible.iloc[-1]


def point_in_time_counts(asof_frame, today_frame, start_date, last_asof_date):
    """Count later observations and changed values for shared available dates."""
    today_visible = today_frame[
        (today_frame["DATE"].dt.date >= start_date) & today_frame["value"].notna()
    ]
    late_count = int((today_visible["DATE"].dt.date > last_asof_date).sum())
    comparison = asof_frame.merge(today_frame, on="DATE", how="inner", suffixes=("_asof", "_today"))
    comparison = comparison[
        (comparison["DATE"].dt.date >= start_date)
        & comparison["value_asof"].notna()
        & comparison["value_today"].notna()
    ]
    revised_count = int((comparison["value_asof"] != comparison["value_today"]).sum())
    return late_count, revised_count


def fmt_observation(row):
    """Format a date/value pair for the summary table."""
    if row is None:
        return "No non-missing observation"
    return f"{row['DATE']:%-d %b %Y}: {row['value']:,.3f}"


def selected_ids(extra_id):
    """Return sidebar selections plus a cleaned typed FRED ID, without duplicates."""
    chosen = st.sidebar.multiselect(
        "Rate series",
        options=list(DEFAULT_SERIES),
        default=list(DEFAULT_SERIES),
        format_func=lambda series_id: f"{series_id} — {DEFAULT_SERIES[series_id]}",
    )
    typed = extra_id.strip().upper()
    if typed and typed not in chosen:
        chosen.append(typed)
    return chosen


def main():
    st.set_page_config(page_title="Point-in-Time Rates", layout="wide")
    st.title("Point-in-Time Rates")
    st.caption(
        "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, "
        f"downloaded {date.today():%-d %B %Y}; built with AI help, a learning "
        "demonstration, not investment advice."
    )

    st.sidebar.header("Controls")
    extra_id = st.sidebar.text_input("Add another FRED series ID", placeholder="e.g., PAYEMS")
    series_ids = selected_ids(extra_id)
    start_date = st.sidebar.date_input("Start date", value=date(2020, 1, 1))
    as_known_on = st.sidebar.date_input("As known on", value=date.today())
    if not series_ids:
        st.info("Choose at least one series in the sidebar.")
        return

    summary_rows = []
    for series_id in series_ids:
        try:
            today_frame = download_today(series_id)
            asof_frame = download_as_known_on(series_id, as_known_on.isoformat())
            chart_frame = today_frame[
                (today_frame["DATE"].dt.date >= start_date) & today_frame["value"].notna()
            ].set_index("DATE")[["value"]]
            st.subheader(f"{series_id} — {DEFAULT_SERIES.get(series_id, 'FRED series')}")
            if chart_frame.empty:
                st.warning(f"No non-missing {series_id} observations from {start_date:%-d %B %Y}.")
            else:
                st.line_chart(chart_frame, y="value")

            asof_last = last_observation(asof_frame, start_date)
            today_last = last_observation(today_frame, start_date)
            st.caption(f"Last date in the data known on {as_known_on:%-d %B %Y}: {fmt_observation(asof_last)}")
            if asof_last is None:
                late_count, revised_count = 0, 0
            else:
                late_count, revised_count = point_in_time_counts(
                    asof_frame, today_frame, start_date, asof_last["DATE"].date()
                )
            summary_rows.append({
                "Series": series_id,
                "Last measured / value as known then": fmt_observation(asof_last),
                "Last measured / value today": fmt_observation(today_last),
                "Today's values after then": late_count,
                "Values revised since": revised_count,
            })
        except (requests.RequestException, ValueError, pd.errors.ParserError) as error:
            st.error(f"{series_id}: could not download this series ({error}).")

    st.subheader("As-known comparison")
    if summary_rows:
        table = pd.DataFrame(summary_rows)
        table["Series"] = table["Series"].map(
            lambda series_id: f"https://fred.stlouisfed.org/series/{series_id}"
        )
        st.dataframe(
            table,
            column_config={"Series": st.column_config.LinkColumn("Series ID", display_text=r".*/series/(.*)$")},
            hide_index=True,
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
