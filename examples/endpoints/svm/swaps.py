#!/usr/bin/env python3
"""Solana DEX Swaps Example - Track Solana trading activity."""

from datetime import datetime

import anyio

from thegraph_token_api import SwapPrograms, TokenAPI


def get_symbol(mint_obj):
    """Get token symbol or shortened mint address."""
    if hasattr(mint_obj, "symbol") and mint_obj.symbol:
        return mint_obj.symbol
    return str(mint_obj)[:6] + "..."


def format_time(timestamp):
    """Format timestamp to readable time."""
    try:
        return datetime.fromtimestamp(timestamp).strftime("%H:%M")
    except (ValueError, OSError, OverflowError):
        return "??:??"


async def main():
    print("⚡ Solana DEX Tracker")
    print("=" * 20)

    api = TokenAPI()

    try:
        # Raydium swaps
        print("🌊 Raydium DEX:")
        raydium = await api.svm.swaps(program_id=SwapPrograms.RAYDIUM, limit=3)

        for i, swap in enumerate(raydium, 1):
            input_sym = get_symbol(swap.input_mint)
            output_sym = get_symbol(swap.output_mint)
            user = swap.user[:8] + "..."
            time = format_time(swap.timestamp)

            print(f"  {i}. {input_sym} → {output_sym} | {user} | {time}")

        # Jupiter swaps
        print("\n🪐 Jupiter DEX:")
        jupiter = await api.svm.swaps(program_id=SwapPrograms.JUPITER_V6, limit=3)

        for i, swap in enumerate(jupiter, 1):
            input_sym = get_symbol(swap.input_mint)
            output_sym = get_symbol(swap.output_mint)
            input_amt = swap.input_amount
            output_amt = swap.output_amount

            print(f"  {i}. {input_sym} → {output_sym}")
            print(f"     {input_amt:.2f} → {output_amt:.2f}")

        # SOL/USDC price discovery
        print("\n💰 SOL/USDC Trading:")
        sol_usdc = await api.svm.swaps(
            program_id=SwapPrograms.RAYDIUM,
            input_mint="So11111111111111111111111111111111111111112",  # SOL
            output_mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC  # pragma: allowlist secret
            limit=2,
        )

        for i, swap in enumerate(sol_usdc, 1):
            sol_amount = swap.input_amount
            usdc_amount = swap.output_amount
            price = usdc_amount / sol_amount if sol_amount > 0 else 0

            print(f"  {i}. {sol_amount:.2f} SOL → {usdc_amount:.2f} USDC")
            print(f"     Rate: ${price:.2f} per SOL")

        print("\n✅ Solana trading data loaded!")

    except Exception as e:
        print(f"❌ Failed to load Solana data: {e}")
        print("💡 Solana queries can take a moment...")


if __name__ == "__main__":
    anyio.run(main)
