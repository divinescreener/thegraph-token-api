"""
The Graph Token API Client.

A clean, separated Python client for The Graph Token API with EVM and SVM support.
Built with divine-requests for reliable HTTP handling and divine-type-enforcer
for robust runtime type validation.

Usage:
    ```python
    import anyio
    from token_api import TokenAPI, SwapPrograms, Protocol

    async def main():
        api = TokenAPI()  # Auto-loads from .env

        # EVM chains (Ethereum, Polygon, BSC, etc.)
        eth_balances = await api.evm.balances("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
        eth_nfts = await api.evm.nfts.ownerships("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
        nft_collection = await api.evm.nfts.collection("0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb")
        eth_swaps = await api.evm.swaps(protocol=Protocol.UNISWAP_V3, limit=5)

        # SVM (Solana)
        sol_balances = await api.svm.balances(mint="So11111111111111111111111111111111111111112")
        sol_swaps = await api.svm.swaps(program_id=SwapPrograms.RAYDIUM, limit=5)

        # Utility
        health = await api.health()

    anyio.run(main)
    ```
"""

from .simple import TokenAPI  # Main simplified interface
from .types import *

__version__ = "0.1.0"
__all__ = [
    "TokenAPI",  # Main interface
    # Export all types
    "NetworkId",
    "SolanaNetworkId",
    "TokenStandard",
    "ActivityType",
    "OrderDirection",
    "OrderBy",
    "Interval",
    "Protocol",
    "SolanaPrograms",
    "SwapPrograms",
    "Statistics",
    "BaseResponse",
    "ErrorResponse",
    "NFTAttribute",
    "NFTOwnership",
    "NFTOwnershipsResponse",
    "NFTCollection",
    "NFTCollectionsResponse",
    "NFTItem",
    "NFTItemsResponse",
    "NFTActivity",
    "NFTActivitiesResponse",
    "NFTHolder",
    "NFTHoldersResponse",
    "NFTSale",
    "NFTSalesResponse",
    "Balance",
    "BalancesResponse",
    "SolanaBalance",
    "SolanaBalancesResponse",
    "Transfer",
    "TransfersResponse",
    "SolanaTransfer",
    "SolanaTransfersResponse",
    "TokenIcon",
    "Token",
    "TokensResponse",
    "TokenHolder",
    "TokenHoldersResponse",
    "SwapToken",
    "Swap",
    "SwapsResponse",
    "SolanaMint",
    "SolanaSwap",
    "SolanaSwapsResponse",
    "Pool",
    "PoolsResponse",
    "OHLC",
    "OHLCResponse",
    "HistoricalBalance",
    "HistoricalBalancesResponse",
    "VersionResponse",
    "Network",
    "NetworksResponse",
]
