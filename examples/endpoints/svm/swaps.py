#!/usr/bin/env python3
"""Solana DEX Swaps Example - Get swap transactions from Raydium, Jupiter, and Pump.fun."""

import os
import sys
from datetime import datetime

import anyio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))
from token_api import SwapPrograms, TokenAPI


async def main():
    print("Solana DEX Swaps Example")
    print("=" * 24)

    api = TokenAPI()

    try:
        # Get Raydium swaps
        print("\nRaydium Swaps:")
        raydium_swaps = await api.svm.swaps(program_id=SwapPrograms.RAYDIUM, limit=4)

        for i, swap in enumerate(raydium_swaps, 1):
            input_symbol = swap.input_mint.symbol if hasattr(swap.input_mint, "symbol") else str(swap.input_mint)[:8]
            output_symbol = (
                swap.output_mint.symbol if hasattr(swap.output_mint, "symbol") else str(swap.output_mint)[:8]
            )

            user = swap.user[:10] + "..."
            time_str = datetime.fromtimestamp(swap.timestamp).strftime("%H:%M") if swap.timestamp else "?"

            print(f"  {i}. {input_symbol} → {output_symbol} | {user} | {time_str}")

        # Get Jupiter swaps
        print("\nJupiter V6 Swaps:")
        jupiter_swaps = await api.svm.swaps(program_id=SwapPrograms.JUPITER_V6, limit=3)

        for i, swap in enumerate(jupiter_swaps, 1):
            input_symbol = swap.input_mint.symbol if hasattr(swap.input_mint, "symbol") else str(swap.input_mint)[:8]
            output_symbol = (
                swap.output_mint.symbol if hasattr(swap.output_mint, "symbol") else str(swap.output_mint)[:8]
            )

            input_amount = swap.input_amount
            output_amount = swap.output_amount

            print(f"  {i}. {input_symbol} → {output_symbol}")
            print(f"     {input_amount:.2f} → {output_amount:.2f}")

        # Get SOL/USDC swaps
        print("\nSOL/USDC Swaps:")
        sol_usdc = await api.svm.swaps(
            program_id=SwapPrograms.RAYDIUM,
            input_mint="So11111111111111111111111111111111111111112",
            output_mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            limit=2,
        )

        for i, swap in enumerate(sol_usdc, 1):
            input_amount = swap.input_amount
            output_amount = swap.output_amount
            price = output_amount / input_amount if input_amount > 0 else 0

            print(f"  {i}. {input_amount:.2f} SOL → {output_amount:.2f} USDC (${price:.2f}/SOL)")

        print("\n✅ Solana swap data retrieved successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    anyio.run(main)
