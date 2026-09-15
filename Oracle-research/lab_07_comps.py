"""Lab 07 comparable-company P/E calculator (USD per share)."""

from statistics import median

# Editable frozen Lab 07 case inputs.  Use total GAAP diluted EPS on a basis
# consistent with each share price; do not use cash or debt in this P/E method.
TARGET = {"ticker": "ABG", "name": "Asbury Automotive", "price": 243.03, "eps": 21.50}
PEERS = [
    {"ticker": "AN", "name": "AutoNation", "price": 169.84, "eps": 16.92},
    {"ticker": "GPI", "name": "Group 1 Automotive", "price": 421.48, "eps": 36.81},
]


def company_id(company):
    """Return a normalized identifier used to remove duplicates and the target."""
    return str(company.get("ticker", company.get("name", ""))).strip().upper()


def pe_multiple(company):
    """Return price / EPS, or a reason P/E is not meaningful."""
    price = company.get("price")
    eps = company.get("eps")
    if price is None or eps is None:
        return None, "missing price or diluted EPS"
    if price <= 0:
        return None, "nonpositive price"
    if eps <= 0:
        return None, "nonpositive diluted EPS"
    return price / eps, None


def implied_price(multiple, target_eps):
    """Return a P/E-implied target price, or a reason it is not meaningful."""
    if target_eps is None:
        return None, "missing target diluted EPS"
    if target_eps <= 0:
        return None, "nonpositive target diluted EPS"
    return multiple * target_eps, None


def usable_peers(peers, target):
    """Exclude the target, deduplicate peers, and retain peers with meaningful P/E."""
    target_id = company_id(target)
    seen = {target_id}
    usable = []
    excluded = []

    for peer in peers:
        identifier = company_id(peer)
        label = peer.get("name", identifier or "Unnamed peer")
        if not identifier:
            excluded.append((label, "missing ticker/name identifier"))
        elif identifier in seen:
            excluded.append((label, "duplicate peer or target; excluded"))
        else:
            seen.add(identifier)
            multiple, reason = pe_multiple(peer)
            if reason:
                excluded.append((label, f"P/E not meaningful: {reason}"))
            else:
                usable.append((peer, multiple))
    return usable, excluded


def format_price(value):
    return "not meaningful" if value is None else f"${value:,.2f}"


def main():
    target_label = f"{TARGET['name']} ({TARGET['ticker']})"
    target_eps = TARGET.get("eps")
    peers, excluded = usable_peers(PEERS, TARGET)

    print(f"Target: {target_label}")
    target_price = TARGET.get("price")
    if target_price is None or target_price <= 0:
        print("Target price (reference only): not meaningful (missing or nonpositive price)")
    else:
        print(f"Target price (reference only): {format_price(target_price)}")
    if target_eps is None or target_eps <= 0:
        print("Target diluted EPS: not meaningful for a positive P/E comparison")
    else:
        print(f"Target total GAAP diluted EPS: ${target_eps:.6f}")

    print("\nUsable peer P/E multiples")
    if not peers:
        print("No usable peers; no implied price or range.")
    else:
        for peer, multiple in peers:
            print(f"{peer['name']} ({peer['ticker']}): {multiple:.6f}x")

        multiples = [multiple for _, multiple in peers]
        low_multiple, middle_multiple, high_multiple = min(multiples), median(multiples), max(multiples)
        low_price, target_reason = implied_price(low_multiple, target_eps)
        middle_price, _ = implied_price(middle_multiple, target_eps)
        high_price, _ = implied_price(high_multiple, target_eps)

        print(f"\nPeer median P/E: {middle_multiple:.6f}x")
        if target_reason:
            print(f"Implied-price calculations: not meaningful ({target_reason}).")
        elif len(peers) == 1:
            print(f"One valid peer: reference estimate (not a range): {format_price(middle_price)}")
        else:
            print(f"Implied-price range: {format_price(low_price)} to {format_price(high_price)}")
            print(f"Implied price at peer median: {format_price(middle_price)}")

        print("\nLeave-one-out peer check")
        for removed_peer, _ in peers:
            remaining = [(peer, multiple) for peer, multiple in peers if peer is not removed_peer]
            removed_label = f"{removed_peer['name']} ({removed_peer['ticker']})"
            if not remaining:
                print(f"Remove {removed_label}: no estimate; no peers remain.")
                continue
            remaining_median = median([multiple for _, multiple in remaining])
            remaining_price, reason = implied_price(remaining_median, target_eps)
            if reason:
                print(f"Remove {removed_label}: not meaningful ({reason}).")
            else:
                change = remaining_price - middle_price
                note = "reference estimate; one peer remains" if len(remaining) == 1 else "median-implied estimate"
                print(
                    f"Remove {removed_label}: {note} {format_price(remaining_price)}; "
                    f"change from full-peer estimate: {change:+,.2f} dollars"
                )

    if excluded:
        print("\nExcluded inputs")
        for label, reason in excluded:
            print(f"{label}: {reason}")


if __name__ == "__main__":
    main()
