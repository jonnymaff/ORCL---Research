"""Lab 08 peer-P/E valuation for Oracle, using September 10, 2026 inputs."""

from statistics import median

# Prices are USD closing prices on 2026-09-10.  EPS is annual reported GAAP
# diluted EPS available on that date, in USD and on the quoted share basis.
TARGET = {"ticker": "ORCL", "name": "Oracle", "price": 152.94, "eps": 5.83}
PEERS = [
    {"ticker": "MSFT", "name": "Microsoft", "price": 492.44, "eps": 17.95},
]


def pe_multiple(company):
    """Return price / positive annual diluted EPS, or an explanation."""
    price, eps = company.get("price"), company.get("eps")
    if price is None or eps is None:
        return None, "missing price or diluted EPS"
    if price <= 0 or eps <= 0:
        return None, "nonpositive price or diluted EPS"
    return price / eps, None


def money(value):
    return f"${value:,.2f}"


def main():
    target_eps = TARGET["eps"]
    multiples = []
    print(f"Target: {TARGET['name']} ({TARGET['ticker']})")
    print(f"Reference closing price: {money(TARGET['price'])}")
    print(f"Annual GAAP diluted EPS: ${target_eps:.2f}")
    print("\nUsable peer P/E multiples")
    for peer in PEERS:
        multiple, reason = pe_multiple(peer)
        if reason:
            print(f"{peer['name']}: excluded ({reason})")
        else:
            multiples.append((peer, multiple))
            print(f"{peer['name']} ({peer['ticker']}): {multiple:.6f}x")

    if not multiples:
        print("No usable peers; no P/E-implied estimate.")
        return

    peer_median = median(value for _, value in multiples)
    implied = peer_median * target_eps
    print(f"\nPeer median P/E: {peer_median:.6f}x")
    if len(multiples) == 1:
        print(f"One valid peer: reference estimate (not a range): {money(implied)}")
    else:
        implied_values = [multiple * target_eps for _, multiple in multiples]
        print(f"Implied-price range: {money(min(implied_values))} to {money(max(implied_values))}")
        print(f"Implied price at peer median: {money(implied)}")

    print("\nLeave-one-out peer check")
    for removed, _ in multiples:
        remaining = [(peer, value) for peer, value in multiples if peer is not removed]
        if not remaining:
            print(f"Remove {removed['name']} ({removed['ticker']}): no estimate; no peers remain.")
        else:
            value = median(item[1] for item in remaining) * target_eps
            print(f"Remove {removed['name']} ({removed['ticker']}): {money(value)}")


if __name__ == "__main__":
    main()
