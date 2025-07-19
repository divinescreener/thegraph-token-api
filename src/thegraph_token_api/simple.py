"""
Simplified Token API Interface

This module provides a clean, separated interface for EVM and SVM chains:
- Auto-loads environment variables
- Returns clean data (no response unwrapping)
- Uses smart defaults (mainnet, reasonable limits)
- Separated EVM and SVM methods

Usage:
    from token_api import TokenAPI
    
    api = TokenAPI()  # Auto-loads from .env
    eth_balances = await api.evm.balances("0x...")  # EVM chains
    sol_balances = await api.svm.balances(mint="...")  # Solana
"""

import os
from typing import List, Optional, Union
from dotenv import load_dotenv

from .client import TheGraphTokenAPI
from .types import NetworkId, SolanaNetworkId, Protocol, TokenStandard, OrderBy, OrderDirection, Interval, SolanaPrograms, SwapPrograms
from .models import (
    Balance, SolanaBalance, Swap, SolanaSwap, Transfer, SolanaTransfer,
    NFTOwnership, NFTCollection, NFTActivity, Token, TokenHolder, Pool, OHLC,
    convert_list_to_models, convert_to_model
)


class NFTWrapper:
    """NFT-specific methods wrapper for EVM chains."""
    
    def __init__(self, api_instance):
        self._api = api_instance
    
    async def ownerships(
        self,
        address: str,
        token_standard: Optional[Union[TokenStandard, str]] = None,
        limit: int = 10,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[NFTOwnership]:
        """Get NFT ownerships for an address."""
        data = await self._api._evm_nfts(address=address, token_standard=token_standard, limit=limit, network=network)
        return convert_list_to_models(data, NFTOwnership)
    
    async def collection(
        self,
        contract: str,
        network: Optional[Union[NetworkId, str]] = None
    ) -> Optional[NFTCollection]:
        """Get NFT collection metadata by contract address."""
        data = await self._api._evm_nft_collection(contract=contract, network=network)
        return convert_to_model(data, NFTCollection) if data else None
    
    async def activities(
        self,
        contract: str,
        from_address: Optional[str] = None,
        to_address: Optional[str] = None,
        limit: int = 10,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[NFTActivity]:
        """Get NFT activities (transfers, mints, burns) for a contract."""
        data = await self._api._evm_nft_activities(contract=contract, from_address=from_address, to_address=to_address, limit=limit, network=network)
        return convert_list_to_models(data, NFTActivity)


class EVMWrapper:
    """EVM-specific methods wrapper."""
    
    def __init__(self, api_instance):
        self._api = api_instance
        
        # Initialize nested NFT wrapper
        self.nfts = NFTWrapper(api_instance)
    
    async def balances(
        self,
        address: str,
        contract: Optional[str] = None,
        limit: int = 10,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[Balance]:
        """Get EVM token balances for an address."""
        data = await self._api._evm_balances(address=address, contract=contract, limit=limit, network=network)
        return convert_list_to_models(data, Balance)
    
    async def token_info(
        self,
        contract: str,
        network: Optional[Union[NetworkId, str]] = None
    ) -> Optional[Token]:
        """Get EVM token contract information."""
        data = await self._api._evm_token_info(contract=contract, network=network)
        return convert_to_model(data, Token) if data else None
    
    async def transfers(
        self,
        from_address: Optional[str] = None,
        to_address: Optional[str] = None,
        contract: Optional[str] = None,
        limit: int = 10,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[Transfer]:
        """Get EVM token transfer events."""
        data = await self._api._evm_transfers(from_address=from_address, to_address=to_address, contract=contract, limit=limit, network=network)
        return convert_list_to_models(data, Transfer)
    
    async def swaps(
        self,
        pool: Optional[str] = None,
        protocol: Optional[Union[Protocol, str]] = None,
        limit: int = 10,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[Swap]:
        """Get EVM DEX swap transactions."""
        data = await self._api._evm_swaps(pool=pool, protocol=protocol, limit=limit, network=network)
        return convert_list_to_models(data, Swap)
    
    async def swaps_advanced(
        self,
        pool: Optional[str] = None,
        caller: Optional[str] = None,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        protocol: Optional[Union[Protocol, str]] = None,
        transaction_id: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        order_by: Union[OrderBy, str] = OrderBy.TIMESTAMP,
        order_direction: Union[OrderDirection, str] = OrderDirection.DESC,
        limit: int = 10,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[Swap]:
        """Get EVM DEX swap transactions with advanced filtering."""
        data = await self._api._evm_swaps_advanced(
            pool=pool, caller=caller, sender=sender, recipient=recipient,
            protocol=protocol, transaction_id=transaction_id,
            start_time=start_time, end_time=end_time,
            order_by=order_by, order_direction=order_direction,
            limit=limit, network=network
        )
        return convert_list_to_models(data, Swap)
    
    async def pools(
        self,
        pool: Optional[str] = None,
        token: Optional[str] = None,
        protocol: Optional[Union[Protocol, str]] = None,
        limit: int = 10,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[Pool]:
        """Get EVM DEX liquidity pools."""
        data = await self._api._evm_pools(pool=pool, token=token, protocol=protocol, limit=limit, network=network)
        return convert_list_to_models(data, Pool)
    
    async def price_history(
        self,
        token: str,
        interval: Union[Interval, str] = Interval.ONE_HOUR,
        days: int = 1,
        limit: int = 24,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[OHLC]:
        """Get EVM OHLC price data for a token."""
        data = await self._api._evm_price_history(token=token, interval=interval, days=days, limit=limit, network=network)
        return convert_list_to_models(data, OHLC)
    
    async def pool_history(
        self,
        pool: str,
        interval: Union[Interval, str] = Interval.ONE_HOUR,
        days: int = 1,
        limit: int = 24,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[OHLC]:
        """Get EVM OHLC data for a DEX pool."""
        data = await self._api._evm_pool_history(pool=pool, interval=interval, days=days, limit=limit, network=network)
        return convert_list_to_models(data, OHLC)
    
    async def token_holders(
        self,
        contract: str,
        limit: int = 10,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[TokenHolder]:
        """Get EVM token holder balances by contract address."""
        data = await self._api._evm_token_holders(contract=contract, limit=limit, network=network)
        return convert_list_to_models(data, TokenHolder)


class SVMWrapper:
    """SVM-specific methods wrapper."""
    
    def __init__(self, api_instance):
        self._api = api_instance
    
    async def swaps(
        self,
        program_id: Union[SwapPrograms, str],
        amm: Optional[str] = None,
        amm_pool: Optional[str] = None,
        user: Optional[str] = None,
        input_mint: Optional[str] = None,
        output_mint: Optional[str] = None,
        signature: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 10,
        network: Union[SolanaNetworkId, str] = SolanaNetworkId.SOLANA
    ) -> List[SolanaSwap]:
        """Get SVM DEX swap transactions."""
        data = await self._api._svm_swaps(
            program_id=program_id, amm=amm, amm_pool=amm_pool,
            user=user, input_mint=input_mint, output_mint=output_mint,
            signature=signature, start_time=start_time, end_time=end_time,
            limit=limit, network=network
        )
        return convert_list_to_models(data, SolanaSwap)
    
    async def balances(
        self,
        token_account: Optional[str] = None,
        mint: Optional[str] = None,
        program_id: Optional[Union[SolanaPrograms, str]] = None,
        limit: int = 10,
        network: Union[SolanaNetworkId, str] = SolanaNetworkId.SOLANA
    ) -> List[SolanaBalance]:
        """Get SVM token balances."""
        data = await self._api._svm_balances(
            token_account=token_account, mint=mint, program_id=program_id,
            limit=limit, network=network
        )
        return convert_list_to_models(data, SolanaBalance)
    
    async def transfers(
        self,
        signature: Optional[str] = None,
        program_id: Optional[Union[SolanaPrograms, str]] = None,
        mint: Optional[str] = None,
        authority: Optional[str] = None,
        source: Optional[str] = None,
        destination: Optional[str] = None,
        limit: int = 10,
        network: Union[SolanaNetworkId, str] = SolanaNetworkId.SOLANA
    ) -> List[SolanaTransfer]:
        """Get SVM token transfers."""
        data = await self._api._svm_transfers(
            signature=signature, program_id=program_id, mint=mint,
            authority=authority, source=source, destination=destination,
            limit=limit, network=network
        )
        return convert_list_to_models(data, SolanaTransfer)


class TokenAPI:
    """
    Simplified Token API client with clean, separated EVM/SVM interface.
    
    This wrapper provides:
    - Auto environment loading
    - Clean data returns (no response unwrapping)
    - Smart defaults
    - Separated EVM/SVM methods
    
    Example:
        ```python
        from token_api import TokenAPI, SwapPrograms, Protocol
        
        api = TokenAPI()  # Auto-loads API key from .env
        
        # EVM (Ethereum, Polygon, BSC, etc.)
        eth_balances = await api.evm.balances("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
        eth_nfts = await api.evm.nfts.ownerships("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
        nft_collection = await api.evm.nfts.collection("0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb")
        nft_activities = await api.evm.nfts.activities("0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb")
        eth_swaps = await api.evm.swaps(protocol=Protocol.UNISWAP_V3, limit=10)
        
        # SVM (Solana)
        sol_balances = await api.svm.balances(mint="So11111111111111111111111111111111111111112")
        sol_swaps = await api.svm.swaps(program_id=SwapPrograms.RAYDIUM, limit=10)
        sol_transfers = await api.svm.transfers(mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")
        
        # Utility
        health = await api.health()
        ```
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        network: Union[NetworkId, str] = NetworkId.MAINNET,
        auto_load_env: bool = True
    ):
        """
        Initialize simplified Token API client.
        
        Args:
            api_key: API key (auto-loads from THEGRAPH_API_KEY if None)
            network: Default network (mainnet by default)
            auto_load_env: Whether to auto-load from .env file
        """
        if auto_load_env:
            load_dotenv()
        
        # Auto-load API key if not provided
        if api_key is None:
            api_key = os.getenv("THEGRAPH_API_KEY")
            if not api_key:
                raise ValueError(
                    "API key not found. Please provide api_key parameter or set THEGRAPH_API_KEY environment variable. "
                    "Get a free API key at: https://thegraph.market (click 'Get API Key')"
                )
        
        self._api = TheGraphTokenAPI(api_key=api_key)
        self._default_network = str(network)
        
        # Initialize nested API wrappers
        self.evm = EVMWrapper(self)
        self.svm = SVMWrapper(self)
    
    def _extract_data(self, response) -> List[dict]:
        """Extract clean data from API response."""
        if hasattr(response, 'data') and isinstance(response.data, dict):
            return response.data.get('data', [])
        return []
    
    # ===== EVM Internal Methods =====
    
    async def _evm_balances(
        self,
        address: str,
        contract: Optional[str] = None,
        limit: int = 10,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[dict]:
        """Internal EVM balances implementation."""
        net = str(network) if network else self._default_network
        async with self._api.evm(net) as client:
            response = await client.get_balances(
                address=address, contract=contract, limit=limit
            )
            return self._extract_data(response)
    
    async def _evm_nfts(
        self,
        address: str,
        token_standard: Optional[Union[TokenStandard, str]] = None,
        limit: int = 10,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[dict]:
        """Internal EVM NFTs implementation."""
        net = str(network) if network else self._default_network
        async with self._api.evm(net) as client:
            response = await client.get_nft_ownerships(
                address=address, token_standard=token_standard, limit=limit
            )
            return self._extract_data(response)
    
    async def _evm_token_info(
        self,
        contract: str,
        network: Optional[Union[NetworkId, str]] = None
    ) -> Optional[dict]:
        """Internal EVM token info implementation."""
        net = str(network) if network else self._default_network
        async with self._api.evm(net) as client:
            response = await client.get_token(contract=contract)
            data = self._extract_data(response)
            return data[0] if data else None
    
    async def _evm_transfers(
        self,
        from_address: Optional[str] = None,
        to_address: Optional[str] = None,
        contract: Optional[str] = None,
        limit: int = 10,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[dict]:
        """Internal EVM transfers implementation."""
        net = str(network) if network else self._default_network
        async with self._api.evm(net) as client:
            response = await client.get_transfers(
                from_address=from_address, to_address=to_address,
                contract=contract, limit=limit
            )
            return self._extract_data(response)
    
    async def _evm_swaps(
        self,
        pool: Optional[str] = None,
        protocol: Optional[Union[Protocol, str]] = None,
        limit: int = 10,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[dict]:
        """Internal EVM swaps implementation."""
        net = str(network) if network else self._default_network
        async with self._api.evm(net) as client:
            response = await client.get_swaps(
                pool=pool, protocol=protocol, limit=limit
            )
            return self._extract_data(response)
    
    async def _evm_swaps_advanced(
        self,
        pool: Optional[str] = None,
        caller: Optional[str] = None,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        protocol: Optional[Union[Protocol, str]] = None,
        transaction_id: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        order_by: Union[OrderBy, str] = OrderBy.TIMESTAMP,
        order_direction: Union[OrderDirection, str] = OrderDirection.DESC,
        limit: int = 10,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[dict]:
        """Internal EVM advanced swaps implementation."""
        net = str(network) if network else self._default_network
        async with self._api.evm(net) as client:
            response = await client.get_swaps(
                pool=pool, caller=caller, sender=sender, recipient=recipient,
                protocol=protocol, transaction_id=transaction_id,
                start_time=start_time, end_time=end_time,
                order_by=order_by, order_direction=order_direction,
                limit=limit
            )
            return self._extract_data(response)
    
    async def _evm_nft_collection(
        self,
        contract: str,
        network: Optional[Union[NetworkId, str]] = None
    ) -> Optional[dict]:
        """Internal EVM NFT collection implementation."""
        net = str(network) if network else self._default_network
        async with self._api.evm(net) as client:
            response = await client.get_nft_collection(contract=contract)
            data = self._extract_data(response)
            return data[0] if data else None
    
    async def _evm_nft_activities(
        self,
        contract: str,
        from_address: Optional[str] = None,
        to_address: Optional[str] = None,
        limit: int = 10,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[dict]:
        """Internal EVM NFT activities implementation."""
        net = str(network) if network else self._default_network
        async with self._api.evm(net) as client:
            response = await client.get_nft_activities(
                contract=contract, from_address=from_address,
                to_address=to_address, limit=limit
            )
            return self._extract_data(response)
    
    async def _evm_pools(
        self,
        pool: Optional[str] = None,
        token: Optional[str] = None,
        protocol: Optional[Union[Protocol, str]] = None,
        limit: int = 10,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[dict]:
        """Internal EVM pools implementation."""
        net = str(network) if network else self._default_network
        async with self._api.evm(net) as client:
            response = await client.get_pools(
                pool=pool, token=token, protocol=protocol, limit=limit
            )
            return self._extract_data(response)
    
    async def _evm_price_history(
        self,
        token: str,
        interval: Union[Interval, str] = Interval.ONE_HOUR,
        days: int = 1,
        limit: int = 24,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[dict]:
        """Internal EVM price history implementation."""
        net = str(network) if network else self._default_network
        from datetime import datetime, timedelta
        start_time = int((datetime.now() - timedelta(days=days)).timestamp())
        
        async with self._api.evm(net) as client:
            response = await client.get_ohlc_prices(
                token=token, interval=interval, start_time=start_time, limit=limit
            )
            return self._extract_data(response)
    
    async def _evm_pool_history(
        self,
        pool: str,
        interval: Union[Interval, str] = Interval.ONE_HOUR,
        days: int = 1,
        limit: int = 24,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[dict]:
        """Internal EVM pool history implementation."""
        net = str(network) if network else self._default_network
        from datetime import datetime, timedelta
        start_time = int((datetime.now() - timedelta(days=days)).timestamp())
        
        async with self._api.evm(net) as client:
            response = await client.get_ohlc_pools(
                pool=pool, interval=interval, start_time=start_time, limit=limit
            )
            return self._extract_data(response)
    
    async def _evm_token_holders(
        self,
        contract: str,
        limit: int = 10,
        network: Optional[Union[NetworkId, str]] = None
    ) -> List[dict]:
        """Internal EVM token holders implementation."""
        net = str(network) if network else self._default_network
        async with self._api.evm(net) as client:
            response = await client.get_token_holders(
                contract=contract, limit=limit
            )
            return self._extract_data(response)
    
    # ===== SVM Internal Methods =====
    
    async def _svm_balances(
        self,
        token_account: Optional[str] = None,
        mint: Optional[str] = None,
        program_id: Optional[Union[SolanaPrograms, str]] = None,
        limit: int = 10,
        network: Union[SolanaNetworkId, str] = SolanaNetworkId.SOLANA
    ) -> List[dict]:
        """Internal SVM balances implementation."""
        async with self._api.svm(str(network)) as client:
            response = await client.get_balances(
                token_account=token_account, mint=mint,
                program_id=program_id, limit=limit
            )
            return self._extract_data(response)
    
    async def _svm_transfers(
        self,
        signature: Optional[str] = None,
        program_id: Optional[Union[SolanaPrograms, str]] = None,
        mint: Optional[str] = None,
        authority: Optional[str] = None,
        source: Optional[str] = None,
        destination: Optional[str] = None,
        limit: int = 10,
        network: Union[SolanaNetworkId, str] = SolanaNetworkId.SOLANA
    ) -> List[dict]:
        """Internal SVM transfers implementation."""
        async with self._api.svm(str(network)) as client:
            response = await client.get_transfers(
                signature=signature, program_id=program_id, mint=mint,
                authority=authority, source=source, destination=destination,
                limit=limit
            )
            return self._extract_data(response)
    
    async def _svm_swaps(
        self,
        program_id: Union[SwapPrograms, str],
        amm: Optional[str] = None,
        amm_pool: Optional[str] = None,
        user: Optional[str] = None,
        input_mint: Optional[str] = None,
        output_mint: Optional[str] = None,
        signature: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 10,
        network: Union[SolanaNetworkId, str] = SolanaNetworkId.SOLANA
    ) -> List[dict]:
        """Internal SVM swaps implementation."""
        async with self._api.svm(str(network)) as client:
            response = await client.get_swaps(
                program_id=program_id, amm=amm, amm_pool=amm_pool,
                user=user, input_mint=input_mint, output_mint=output_mint,
                signature=signature, start_time=start_time, end_time=end_time,
                limit=limit
            )
            return self._extract_data(response)
    
    # ===== Utility Methods =====
    
    async def health(self) -> str:
        """Check API health status."""
        return await self._api.get_health()


# Make TokenAPI available as the main export
__all__ = ['TokenAPI']