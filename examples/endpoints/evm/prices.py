#!/usr/bin/env python3
"""Price History Example - Get OHLC price data."""

import os
import sys
from datetime import datetime

import anyio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))
from token_api import Interval, TokenAPI


async def main():
    print("Price History Example")
    print("=" * 21)

    api = TokenAPI()

    try:
        # Get LINK token price history
        print("\nLINK Price History (7 days):")
        price_data = await api.evm.price_history(
            token="0x514910771AF9Ca656af840dff83E8264EcF986CA", interval=Interval.ONE_DAY, days=7
        )

        for candle in price_data[:5]:
            timestamp = candle.datetime
            open_price = candle.open
            close_price = candle.close

            try:
                dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                date_str = dt.strftime("%m/%d")
            except:
                date_str = "?"

            change = ((close_price - open_price) / open_price * 100) if open_price > 0 else 0
            print(f"  {date_str}: ${open_price:.2f} → ${close_price:.2f} ({change:+.1f}%)")

        # Get pool price history
        print("\nPool Price History (24h):")
        pool_data = await api.evm.pool_history(
            pool="0x3E456E2A71adafb6fe0AF8098334ee41ef53A7C6", interval=Interval.ONE_HOUR, days=1
        )

        for candle in pool_data[:3]:
            timestamp = candle.datetime
            open_price = candle.open
            close_price = candle.close

            try:
                dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                time_str = dt.strftime("%H:%M")
            except:
                time_str = "?"

            print(f"  {time_str}: {open_price:.6f} → {close_price:.6f}")

        print("\n✅ Price data retrieved successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    anyio.run(main)
