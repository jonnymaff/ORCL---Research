"""SEC EDGAR fact collector for Lab 18 (all dollar figures are $ millions)."""
from __future__ import annotations

import argparse
import gzip
import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

USER_AGENT = "Jonat Maffei jonat@example.com"  # Replace with your school email before submitting.
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
NOT_FOUND = "not found"
NOT_KNOWN = "not known"

METRICS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"],
    "net_income": ["NetIncomeLoss"],
    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "capital_spending": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
    "equity": ["StockholdersEquity"],
}
FLOW_METRICS = {"revenue", "net_income", "operating_cash_flow", "capital_spending"}


def get_json(url: str) -> dict:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "gzip, deflate"})
    with urlopen(request, timeout=30) as response:
        body = response.read()
        if response.headers.get("Content-Encoding") == "gzip":
            body = gzip.decompress(body)
        return json.loads(body.decode("utf-8"))


def cik_for_ticker(ticker: str) -> int:
    ticker = ticker.upper().strip()
    tickers = get_json(TICKERS_URL)
    for item in tickers.values():
        if item["ticker"].upper() == ticker:
            return int(item["cik_str"])
    raise ValueError(f"Ticker {ticker!r} was not found in SEC company_tickers.json")


def annual_fact(facts: dict, tags: list[str], end: str, is_flow: bool) -> tuple[float | str, str]:
    """Return the latest-filed 10-K observation for one fiscal-year end, or not found.

    The SEC can expose the same annual period in several 10-Ks; sorting by `filed`
    descending implements the lab rule that the latest filing wins.
    """
    for tag in tags:  # Tag order implements the lab's required fallbacks.
        fact = facts.get("us-gaap", {}).get(tag)
        if not fact:
            continue
        units = fact.get("units", {})
        observations = units.get("USD", [])
        candidates = [
            item for item in observations
            if item.get("form") == "10-K" and item.get("fp") == "FY" and item.get("end") == end
        ]
        if is_flow:
            candidates = [
                item for item in candidates
                if item.get("start") and 300 <= (datetime.fromisoformat(item["end"]) - datetime.fromisoformat(item["start"])).days <= 400
            ]
        if candidates:
            item = max(candidates, key=lambda x: (x.get("filed", ""), x.get("accn", "")))
            return item["val"] / 1_000_000, tag
    return NOT_FOUND, NOT_FOUND


def fiscal_year_ends(facts: dict) -> list[str]:
    """Find the five latest fiscal ends represented by an annual 10-K flow fact."""
    ends: set[str] = set()
    for tag in [tag for metric_tags in METRICS.values() for tag in metric_tags]:
        for item in facts.get("us-gaap", {}).get(tag, {}).get("units", {}).get("USD", []):
            if item.get("form") != "10-K" or item.get("fp") != "FY" or not item.get("start"):
                continue
            try:
                days = (datetime.fromisoformat(item["end"]) - datetime.fromisoformat(item["start"])).days
            except (KeyError, ValueError):
                continue
            if 300 <= days <= 400:
                ends.add(item["end"])
    return sorted(ends)[-5:]


def build_row(facts: dict, fiscal_end: str) -> dict:
    """Turn SEC company facts into one lab row; missing values remain explicit."""
    row: dict = {"fiscal_year_end": fiscal_end, "tags": {}}
    for metric, tags in METRICS.items():
        value, tag = annual_fact(facts, tags, fiscal_end, metric in FLOW_METRICS)
        row[metric] = value
        row["tags"][metric] = tag
    income, equity = row["net_income"], row["equity"]
    if isinstance(income, (int, float)) and isinstance(equity, (int, float)) and equity > 0:
        row["roe"] = income / equity * 100
    else:
        row["roe"] = NOT_KNOWN
    cash, capex = row["operating_cash_flow"], row["capital_spending"]
    row["owner_earnings"] = cash - capex if isinstance(cash, (int, float)) and isinstance(capex, (int, float)) else NOT_FOUND
    row["tags"]["roe"] = "computed: NetIncomeLoss / StockholdersEquity"
    row["tags"]["owner_earnings"] = "computed: operating cash flow - capital spending"
    return row


def checks(rows: list[dict]) -> dict[str, str]:
    roes = [row["roe"] for row in rows]
    owners = [row["owner_earnings"] for row in rows]
    return {
        "ROE of 15% or more every year": "pass" if len(roes) == 5 and all(isinstance(x, (int, float)) and x >= 15 for x in roes) else NOT_KNOWN if any(not isinstance(x, (int, float)) for x in roes) else "fail",
        "Owner earnings positive every year": "pass" if len(owners) == 5 and all(isinstance(x, (int, float)) and x > 0 for x in owners) else NOT_KNOWN if any(not isinstance(x, (int, float)) for x in owners) else "fail",
        "Owner earnings grew, first year to last": "pass" if len(owners) == 5 and isinstance(owners[0], (int, float)) and isinstance(owners[-1], (int, float)) and owners[-1] > owners[0] else NOT_KNOWN if len(owners) != 5 or not isinstance(owners[0], (int, float)) or not isinstance(owners[-1], (int, float)) else "fail",
    }


def analyze(ticker: str) -> dict:
    cik = cik_for_ticker(ticker)
    payload = get_json(FACTS_URL.format(cik=cik))
    rows = [build_row(payload["facts"], end) for end in fiscal_year_ends(payload["facts"])]
    return {"ticker": ticker.upper(), "company": payload.get("entityName", ""), "cik": f"{cik:010d}", "rows": rows, "checks": checks(rows)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Print five 10-K fiscal years from SEC EDGAR.")
    parser.add_argument("ticker")
    parser.add_argument("--json", dest="json_path", help="Also save the analysis JSON to this path.")
    args = parser.parse_args()
    result = analyze(args.ticker)
    rendered = json.dumps(result, indent=2)
    print(rendered)
    if args.json_path:
        Path(args.json_path).write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"EDGAR analysis failed: {error}", file=sys.stderr)
        raise SystemExit(1)
