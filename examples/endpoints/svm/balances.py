#!/usr/bin/env python3
"""Solana SPL Token Balances Example - Get SPL token balances."""

import os
import sys

import anyio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))
from thegraph_token_api import SolanaPrograms, TokenAPI


async def main():
    print("Solana SPL Token Balances")
    print("=" * 25)

    api = TokenAPI()

    try:
        # Get general SPL token balances
        print("\nSPL Token Balances:")
        balances = await api.svm.balances(limit=6)

        for i, balance in enumerate(balances, 1):
            mint = balance.mint[:10] + "..."
            amount = balance.amount
            decimals = balance.decimals

            # Simple decimal formatting
            if decimals > 0:
                formatted = f"{float(amount) / (10 ** decimals):.2f}"
            else:
                formatted = amount

            print(f"  {i}. {mint}: {formatted}")

        # Get USDC balances
        print("\nUSDC Balances:")
        usdc_balances = await api.svm.balances(mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", limit=3)

        for i, balance in enumerate(usdc_balances, 1):
            account = balance.token_account[:12] + "..."
            amount = balance.amount
            usdc_amount = float(amount) / 1_000_000  # USDC has 6 decimals

            print(f"  {i}. {account}: {usdc_amount:,.2f} USDC")

        # Get Token 2022 balances
        print("\nToken 2022 Program:")
        token2022 = await api.svm.balances(program_id=SolanaPrograms.TOKEN_2022, limit=2)

        if token2022:
            for i, balance in enumerate(token2022, 1):
                mint = balance.mint[:12] + "..."
                amount = balance.amount
                print(f"  {i}. {mint}: {amount}")
        else:
            print("  No Token 2022 balances found")

        print("\n✅ Solana balances retrieved successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    anyio.run(main)
