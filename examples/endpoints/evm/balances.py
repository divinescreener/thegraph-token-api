#!/usr/bin/env python3
"""Token Balances Example - Get ERC-20 token balances."""

import os
import sys

import anyio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))
from thegraph_token_api import TokenAPI


async def main():
    print("Token Balances Example")
    print("=" * 22)

    api = TokenAPI()
    vitalik = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

    try:
        # Get top token balances
        print(f"\nTop balances for {vitalik[:10]}...:")
        balances = await api.evm.balances(vitalik, limit=7)

        for i, balance in enumerate(balances, 1):
            symbol = balance.symbol or "?"
            value = balance.value

            # Simple number formatting
            if value > 1_000_000:
                formatted = f"{value/1_000_000:.1f}M"
            elif value > 1_000:
                formatted = f"{value/1_000:.1f}K"
            else:
                formatted = f"{value:.2f}"

            print(f"  {i}. {symbol}: {formatted}")

        # Get specific token balance
        print("\nSpecific token balance:")
        specific = await api.evm.balances(vitalik, contract="0x6A1B2AE3a55B5661b40d86c2bF805f7DAdB16978", limit=1)

        if specific:
            symbol = specific[0].symbol or "?"
            value = specific[0].value
            print(f"  {symbol}: {value}")
        else:
            print("  No balance found")

        print("\n✅ Balances retrieved successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    anyio.run(main)
