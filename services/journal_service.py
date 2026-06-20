from db import init_db, get_connection
from datetime import date

ASSETS = ["BTC", "ETH", "SOL"]


def yes_no(prompt):
    return 1 if input(prompt + " (y/n): ").lower() == "y" else 0


def collect_asset():
    asset = input("Asset: ")
    timeframe = input("Timeframe (1D/4H/1H): ")
    trend = input("Trend: ")
    hh = yes_no("Higher High?")
    hl = yes_no("Higher Low?")
    lh = yes_no("Lower High?")
    ll = yes_no("Lower Low?")
    support = float(input("Support: "))
    resistance = float(input("Resistance: "))
    volume_level = input("Volume level: ")
    volume_trend = input("Volume trend: ")
    liquidity = input("Liquidity: ")
    spread = input("Spread: ")

    return (
        asset, timeframe, trend, hh, hl, lh, ll,
        support, resistance, volume_level,
        volume_trend, liquidity, spread
    )


def main():
    init_db()

    conn = get_connection()
    cur = conn.cursor()

    today = str(date.today())

    market_context = input("Market Context: ")
    risk_regime = input("Risk Regime: ")
    confidence = int(input("Confidence (0-100): "))
    hypothesis = input("Hypothesis: ")
    probability = int(input("Probability: "))
    invalidation = input("Invalidation: ")
    uncertainty = input("Biggest uncertainty: ")
    bias = input("Possible bias: ")

    cur.execute("""
        INSERT INTO daily_reports (
            date, market_context, risk_regime,
            confidence, hypothesis, probability,
            invalidation, uncertainty, bias
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        today, market_context, risk_regime,
        confidence, hypothesis, probability,
        invalidation, uncertainty, bias
    ))

    report_id = cur.lastrowid

    for asset_name in ASSETS:
        print(f"\n--- {asset_name} ---")
        asset_data = collect_asset()

        cur.execute("""
            INSERT INTO asset_analysis (
                report_id, asset, timeframe, trend,
                hh, hl, lh, ll, support, resistance,
                volume_level, volume_trend, liquidity, spread
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (report_id,) + asset_data)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()