#!/usr/bin/env python3
"""Token Transfers Example - Track token movements on-chain."""

from datetime import datetime

import anyio

from thegraph_token_api import TokenAPI


def format_time(timestamp):
    """Format timestamp to readable time."""
    try:
        return datetime.fromtimestamp(timestamp).strftime("%H:%M")
    except (ValueError, OSError, OverflowError):
        return "??:??"


async def main():
    print("🔄 Token Transfers")
    print("=" * 18)

    api = TokenAPI()
    wallet = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"  # Vitalik's wallet
    imagine_token = "0x6A1B2AE3a55B5661b40d86c2bF805f7DAdB16978"  # nosec B105

    try:
        # Token-specific transfers
        print("📦 Recent Token Transfers:")
        transfers = await api.evm.transfers(contract=imagine_token, limit=3)

        for i, transfer in enumerate(transfers, 1):
            amount = transfer.value
            from_addr = transfer.from_address[:6] + "..."
            to_addr = transfer.to[:6] + "..."
            time = format_time(transfer.timestamp)

            print(f"  {i}. {amount:.2f} | {from_addr} → {to_addr} | {time}")

        # Wallet outgoing transfers
        print(f"\n📤 Outgoing from {wallet[:8]}...:")
        outgoing = await api.evm.transfers(from_address=wallet, limit=3)

        for i, transfer in enumerate(outgoing, 1):
            amount = transfer.value
            symbol = transfer.symbol or "TOKEN"
            to_addr = transfer.to[:6] + "..."

            print(f"  {i}. {amount:.2f} {symbol} → {to_addr}")

        print("\n✅ Transfer data loaded!")

    except Exception as e:
        print(f"❌ Failed to load transfers: {e}")
        print("💡 Transfer queries cover recent blockchain activity")


if __name__ == "__main__":
    anyio.run(main)
