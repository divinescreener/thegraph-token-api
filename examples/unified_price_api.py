#!/usr/bin/env python3
"""
Unified Price API Example

Demonstrates the new Unified Price API that supports multiple cryptocurrencies
across different blockchains using a single, consistent interface.
"""

import os
import sys
import time
import traceback
from pathlib import Path

import anyio
from dotenv import load_dotenv

# Add the parent directory to the path so we can import the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from thegraph_token_api import Currency, TokenAPI

# Load environment variables
load_dotenv()


async def main():
    """Demonstrate Unified Price API functionality."""
    print("🌟 Unified Price API Demo")
    print("=" * 30)

    # Check for API key
    api_key = os.environ.get("THEGRAPH_API_KEY")
    if not api_key:
        print("❌ Error: THEGRAPH_API_KEY not found in environment")
        print("💡 Get a free API key at: https://thegraph.market")
        return

    # Initialize the API
    api = TokenAPI(api_key=api_key)

    try:
        # ===== Simple Price Queries =====
        print("\n📊 Simple Price Queries")
        print("-" * 25)

        print("🔍 Fetching current prices...")

        # Get ETH price
        eth_price = await api.price.get(Currency.ETH)
        if eth_price:
            print(f"💎 ETH: ${eth_price:.2f}")
        else:
            print("❌ ETH price unavailable")

        # Get SOL price
        sol_price = await api.price.get(Currency.SOL)
        if sol_price:
            print(f"☀️  SOL: ${sol_price:.2f}")
        else:
            print("❌ SOL price unavailable")

        # ===== Price with Statistics =====
        print("\n📈 Detailed Price Analysis")
        print("-" * 27)

        # ETH with detailed stats
        print("🔍 Analyzing ETH price data...")
        eth_stats = await api.price.get(Currency.ETH, include_stats=True)

        if eth_stats:
            print("💎 ETH Detailed Analysis:")
            print(f"   💰 Price: ${eth_stats['price']:.2f}")
            print(f"   📊 Confidence: {eth_stats['confidence']:.0%}")
            print(f"   📈 Trades analyzed: {eth_stats['trades_analyzed']}")
            print(f"   📉 Volatility: ${eth_stats['std_deviation']:.2f}")
            print(f"   📋 Range: ${eth_stats['min_price']:.2f} - ${eth_stats['max_price']:.2f}")

            # Confidence interpretation
            conf = eth_stats["confidence"]
            if conf >= 0.8:
                print("   🟢 High confidence - excellent data quality")
            elif conf >= 0.5:
                print("   🟡 Medium confidence - good data quality")
            else:
                print("   🟠 Low confidence - limited data available")
        else:
            print("❌ ETH detailed analysis unavailable")

        # SOL with detailed stats
        print("\n🔍 Analyzing SOL price data...")
        sol_stats = await api.price.get(Currency.SOL, include_stats=True)

        if sol_stats:
            print("☀️  SOL Detailed Analysis:")
            print(f"   💰 Price: ${sol_stats['price']:.2f}")
            print(f"   📊 Confidence: {sol_stats['confidence']:.0%}")
            print(f"   📈 Trades analyzed: {sol_stats['trades_analyzed']}")
            print(f"   📉 Volatility: ${sol_stats['std_deviation']:.2f}")
            print(f"   📋 Range: ${sol_stats['min_price']:.2f} - ${sol_stats['max_price']:.2f}")

            # Confidence interpretation
            conf = sol_stats["confidence"]
            if conf >= 0.8:
                print("   🟢 High confidence - excellent data quality")
            elif conf >= 0.5:
                print("   🟡 Medium confidence - good data quality")
            else:
                print("   🟠 Low confidence - limited data available")
        else:
            print("❌ SOL detailed analysis unavailable")

        # ===== Cache Performance Demo =====
        print("\n⚡ Smart Caching Demo")
        print("-" * 20)

        # First call (fetches from DEX data)
        print("🌐 First call (fetching from DEX)...")
        start = time.time()
        price1 = await api.price.get(Currency.ETH)
        time1 = time.time() - start

        # Second call (uses cache)
        print("⚡ Second call (using cache)...")
        start = time.time()
        price2 = await api.price.get(Currency.ETH)
        time2 = time.time() - start

        if price1 and price2:
            print("📊 Results:")
            print(f"   🌐 API call: ${price1:.2f} - {time1:.2f}s")
            print(f"   ⚡ Cached: ${price2:.2f} - {time2:.3f}s")
            if time1 > time2:
                print(f"   🚀 Speedup: {time1 / time2:.0f}x faster!")

        # ===== Supported Currencies =====
        print("\n🗂️  Supported Currencies")
        print("-" * 21)

        supported = await api.price.get_supported_currencies()
        print("✅ Currently supported:")
        for currency in supported:
            print(f"   • CURRENCY.{currency}")

        # ===== Error Handling Demo =====
        print("\n🛡️  Error Handling")
        print("-" * 17)

        # Demo enum-only interface - no string acceptance
        print("✅ API accepts only Currency enums - no backward compatibility")
        print("   Example: Currency.ETH, Currency.SOL, Currency.POL")

        # Check supported currencies
        print(f"🪙 Currently supported: {', '.join([c.value for c in await api.price.get_supported_currencies()])}")

        print("\n🎉 Unified Price API Demo Complete!")
        print("\n💡 Key Features Demonstrated:")
        print("   • Simple Currency.SYMBOL interface")
        print("   • Multi-blockchain support (Ethereum + Solana)")
        print("   • Smart caching with volatility-based TTL")
        print("   • Detailed statistical analysis")
        print("   • Automatic outlier filtering")
        print("   • Progressive retry with adaptive sampling")
        print("   • Robust error handling")

        print("\n📝 Example usage patterns:")
        print("   price = await api.price.get(Currency.ETH)")
        print("   stats = await api.price.get(Currency.SOL, include_stats=True)")
        print("   supported = await api.price.get_supported_currencies()")

    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    anyio.run(main)
