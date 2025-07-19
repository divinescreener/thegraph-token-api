"""
SVM-specific client for The Graph Token API.

Provides access to Solana blockchain data including SPL tokens, balances, transfers, and DEX swaps.
"""

from typing import Optional, Union
from .base import BaseTokenAPI
from .types import (
    # Enums
    SolanaNetworkId, OrderDirection, OrderBy, SolanaPrograms, SwapPrograms,
    
    # Response types
    SolanaBalancesResponse, SolanaTransfersResponse, SolanaSwapsResponse
)


class SVMTokenAPI(BaseTokenAPI):
    """
    SVM-specific client for The Graph Token API.
    
    Provides access to Solana blockchain data with network-specific configuration.
    
    Example:
        ```python
        import anyio
        from thegraph_client import SVMTokenAPI, SolanaNetworkId, SwapPrograms
        
        async def main():
            # Create SVM client for Solana
            async with SVMTokenAPI(
                api_key="your_bearer_token",
                network=SolanaNetworkId.SOLANA
            ) as svm_api:
                # Get SPL token balances
                balances = await svm_api.get_balances(
                    token_account="4ct7br2vTPzfdmY3S5HLtTxcGSBfn6pnw98hsS6v359A"
                )
                
                # Get swap transactions
                swaps = await svm_api.get_swaps(
                    program_id=SwapPrograms.RAYDIUM,
                    user="9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM"
                )
        
        anyio.run(main)
        ```
    """
    
    def __init__(
        self,
        network: Union[SolanaNetworkId, str] = SolanaNetworkId.SOLANA,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        Initialize SVM Token API client.
        
        Args:
            network: SVM network to use (default: SolanaNetworkId.SOLANA)
            api_key: Bearer token for API authentication
            base_url: API base URL (optional)
        """
        super().__init__(api_key, base_url)
        self.network = str(network)
    
    # ===== Balance Methods =====
    
    async def get_balances(
        self,
        token_account: Optional[str] = None,
        mint: Optional[str] = None,
        program_id: Optional[Union[SolanaPrograms, str]] = None,
        limit: int = 10,
        page: int = 1
    ) -> SolanaBalancesResponse:
        """
        Get Solana SPL token balances.
        
        Args:
            token_account: Filter by token account address
            mint: Filter by mint address
            program_id: Filter by program ID
            limit: Maximum number of results
            page: Page number
            
        Returns:
            SolanaBalancesResponse with validated data
        """
        self._validate_pagination(limit, page)
        params = {
            "network_id": self.network,
            "limit": limit,
            "page": page
        }
        if token_account:
            params["token_account"] = token_account
        if mint:
            params["mint"] = mint
        if program_id:
            params["program_id"] = str(program_id)
        
        response = await self.manager.get(
            f"{self.base_url}/balances/svm",
            headers=self._headers,
            params=params,
            expected_type=SolanaBalancesResponse
        )
        return response
    
    # ===== Transfer Methods =====
    
    async def get_transfers(
        self,
        signature: Optional[str] = None,
        program_id: Optional[Union[SolanaPrograms, str]] = None,
        mint: Optional[str] = None,
        authority: Optional[str] = None,
        source: Optional[str] = None,
        destination: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        order_by: Union[OrderBy, str] = OrderBy.TIMESTAMP,
        order_direction: Union[OrderDirection, str] = OrderDirection.DESC,
        limit: int = 10,
        page: int = 1
    ) -> SolanaTransfersResponse:
        """
        Get Solana SPL token transfer events.
        
        Args:
            signature: Filter by transaction signature
            program_id: Filter by program ID
            mint: Filter by mint address
            authority: Filter by authority address
            source: Filter by source address
            destination: Filter by destination address
            start_time: Start time as UNIX timestamp
            end_time: End time as UNIX timestamp
            order_by: Field to order by
            order_direction: Order direction (asc/desc)
            limit: Maximum number of results
            page: Page number
            
        Returns:
            SolanaTransfersResponse with validated data
        """
        self._validate_pagination(limit, page)
        params = {
            "network_id": self.network,
            "orderBy": str(order_by),
            "orderDirection": str(order_direction),
            "limit": limit,
            "page": page
        }
        
        if signature:
            params["signature"] = signature
        if program_id:
            params["program_id"] = str(program_id)
        if mint:
            params["mint"] = mint
        if authority:
            params["authority"] = authority
        if source:
            params["source"] = source
        if destination:
            params["destination"] = destination
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        
        response = await self.manager.get(
            f"{self.base_url}/transfers/svm",
            headers=self._headers,
            params=params,
            expected_type=SolanaTransfersResponse
        )
        return response
    
    # ===== Swap Methods =====
    
    async def get_swaps(
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
        order_by: Union[OrderBy, str] = OrderBy.TIMESTAMP,
        order_direction: Union[OrderDirection, str] = OrderDirection.DESC,
        limit: int = 10,
        page: int = 1
    ) -> SolanaSwapsResponse:
        """
        Get Solana DEX swap transactions.
        
        Args:
            program_id: Filter by swap program ID (required)
            amm: Filter by AMM address
            amm_pool: Filter by AMM pool address
            user: Filter by user address
            input_mint: Filter by input mint address
            output_mint: Filter by output mint address
            signature: Filter by transaction signature
            start_time: Start time as UNIX timestamp
            end_time: End time as UNIX timestamp
            order_by: Field to order by
            order_direction: Order direction (asc/desc)
            limit: Maximum number of results
            page: Page number
            
        Returns:
            SolanaSwapsResponse with validated data
        """
        self._validate_pagination(limit, page)
        params = {
            "program_id": str(program_id),
            "network_id": self.network,
            "orderBy": str(order_by),
            "orderDirection": str(order_direction),
            "limit": limit,
            "page": page
        }
        
        if amm:
            params["amm"] = amm
        if amm_pool:
            params["amm_pool"] = amm_pool
        if user:
            params["user"] = user
        if input_mint:
            params["input_mint"] = input_mint
        if output_mint:
            params["output_mint"] = output_mint
        if signature:
            params["signature"] = signature
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        
        response = await self.manager.get(
            f"{self.base_url}/swaps/svm",
            headers=self._headers,
            params=params,
            expected_type=SolanaSwapsResponse
        )
        return response