#!/usr/bin/env python3
"""Token Transfers Example - Get token transfer events."""

import os
import sys
from datetime import datetime

import anyio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))
from thegraph_token_api import TokenAPI


async def main():
    print("Token Transfers Example")
    print("=" * 23)

    api = TokenAPI()
    vitalik = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

    try:
        # Get recent transfers for specific token
        print("\nRecent Imagine Token transfers:")
        transfers = await api.evm.transfers(contract="0x6A1B2AE3a55B5661b40d86c2bF805f7DAdB16978", limit=4)

        for i, transfer in enumerate(transfers, 1):
            value = transfer.value
            from_addr = transfer.from_address[:8] + "..."
            to_addr = transfer.to[:8] + "..."

            time_str = datetime.fromtimestamp(transfer.timestamp).strftime("%H:%M") if transfer.timestamp else "?"

            print(f"  {i}. {value:.2f} | {from_addr} → {to_addr} | {time_str}")

        # Get transfers from specific address
        print(f"\nTransfers FROM {vitalik[:10]}...:")
        from_transfers = await api.evm.transfers(from_address=vitalik, limit=3)

        for i, transfer in enumerate(from_transfers, 1):
            value = transfer.value
            symbol = transfer.symbol or "?"
            to_addr = transfer.to[:8] + "..."

            print(f"  {i}. {value:.2f} {symbol} → {to_addr}")

        print("\n✅ Transfer data retrieved successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    anyio.run(main)
