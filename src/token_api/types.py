"""
Type definitions for The Graph Token API.

This module contains all TypedDict and enum definitions based on the OpenAPI 3.1.0 specification.
All types are designed for use with divine-type-enforcer for runtime validation.
"""

from typing import TypedDict, List, Optional, Union, Literal
from enum import Enum


# ===== Common Types =====

class BaseResponse(TypedDict, total=False):
    """Base response structure for all API endpoints."""
    data: List[dict]
    results: Optional[int]  # Number of results returned
    statistics: Optional[dict]
    duration_ms: Optional[float]
    pagination: Optional[dict]
    request_time: Optional[str]
    total_results: Optional[int]

class NetworkId(str, Enum):
    """Supported EVM network IDs."""
    ARBITRUM_ONE = "arbitrum-one"
    AVALANCHE = "avalanche" 
    BASE = "base"
    BSC = "bsc"
    MAINNET = "mainnet"
    MATIC = "matic"
    OPTIMISM = "optimism"
    UNICHAIN = "unichain"
    
    def __str__(self) -> str:
        return self.value


class SolanaNetworkId(str, Enum):
    """Supported SVM network IDs."""
    SOLANA = "solana"
    
    def __str__(self) -> str:
        return self.value


class TokenStandard(str, Enum):
    """NFT token standards."""
    EMPTY = ""
    ERC721 = "ERC721"
    ERC1155 = "ERC1155"
    
    def __str__(self) -> str:
        return self.value


class ActivityType(str, Enum):
    """NFT activity types."""
    TRANSFER = "TRANSFER"
    MINT = "MINT"
    BURN = "BURN"


class OrderDirection(str, Enum):
    """Order direction for sorting."""
    ASC = "asc"
    DESC = "desc"
    
    def __str__(self) -> str:
        return self.value


class OrderBy(str, Enum):
    """Order by field."""
    TIMESTAMP = "timestamp"
    VALUE = "value"
    
    def __str__(self) -> str:
        return self.value


class Interval(str, Enum):
    """Time intervals for OHLC data."""
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    ONE_DAY = "1d"
    ONE_WEEK = "1w"
    
    def __str__(self) -> str:
        return self.value


class Protocol(str, Enum):
    """DEX protocols."""
    UNISWAP_V2 = "uniswap_v2"
    UNISWAP_V3 = "uniswap_v3"
    
    def __str__(self) -> str:
        return self.value


class SolanaPrograms(str, Enum):
    """Solana program IDs."""
    TOKEN_2022 = "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"
    TOKEN = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
    
    def __str__(self) -> str:
        return self.value


class SwapPrograms(str, Enum):
    """Solana swap program IDs."""
    RAYDIUM = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"  # Raydium Liquidity Pool V4
    PUMP_FUN_CORE = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"  # Pump.fun
    PUMP_FUN_AMM = "pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA"  # Pump.fun AMM
    JUPITER_V4 = "JUP4Fb2cqiRUcaTHdrPC8h2gNsA2ETXiPDD33WcGuJB"  # Jupiter Aggregator v4
    JUPITER_V6 = "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4"  # Jupiter Aggregator v6
    
    def __str__(self) -> str:
        return self.value


# ===== Common Response Structure =====

class Statistics(TypedDict, total=False):
    """API response statistics."""
    elapsed: float
    rows_read: float
    bytes_read: float


# Removed duplicate BaseResponse


# ===== NFT Types =====

class NFTAttribute(TypedDict):
    """NFT attribute/trait."""
    trait_type: str
    value: str
    display_type: Optional[str]


class NFTOwnership(TypedDict):
    """NFT ownership record."""
    token_id: str
    token_standard: TokenStandard
    contract: str
    owner: str
    network_id: str  # API returns string format
    symbol: Optional[str]
    uri: Optional[str]
    name: Optional[str]
    image: Optional[str]
    description: Optional[str]


class NFTOwnershipsResponse(BaseResponse):
    """Response for NFT ownerships endpoint."""
    data: List[NFTOwnership]


class NFTCollection(TypedDict, total=False):
    """NFT collection metadata."""
    contract: str
    contract_creation: str
    contract_creator: str
    name: str
    symbol: str
    owners: float
    total_supply: float
    total_unique_supply: float
    total_transfers: float
    network_id: str  # API returns string format
    token_standard: Optional[str]  # API may include this field


class NFTCollectionsResponse(BaseResponse):
    """Response for NFT collections endpoint."""
    data: List[NFTCollection]


class NFTItem(TypedDict):
    """NFT item/token details."""
    token_id: str
    token_standard: TokenStandard
    contract: str
    owner: str
    network_id: str  # API returns string format
    uri: Optional[str]
    name: Optional[str]
    image: Optional[str]
    description: Optional[str]
    attributes: Optional[List[NFTAttribute]]


class NFTItemsResponse(BaseResponse):
    """Response for NFT items endpoint."""
    data: List[NFTItem]


NFTActivity = TypedDict('NFTActivity', {
    '@type': str,  # API uses @type field
    'block_num': float,
    'block_hash': str,
    'timestamp': str,
    'tx_hash': str,
    'contract': str,
    'symbol': Optional[str],
    'name': Optional[str],
    'from': str,  # API uses 'from' field
    'to': str,
    'token_id': str,
    'amount': float,
    'transfer_type': Optional[str],
    'token_standard': Optional[str],
}, total=False)


class NFTActivitiesResponse(BaseResponse):
    """Response for NFT activities endpoint."""
    data: List[NFTActivity]


class NFTHolder(TypedDict):
    """NFT holder information."""
    token_standard: str
    address: str
    quantity: float
    unique_tokens: float
    percentage: float
    network_id: str  # API returns string format


class NFTHoldersResponse(TypedDict):
    """Response for NFT holders endpoint."""
    data: List[NFTHolder]
    statistics: Optional[Statistics]


class NFTSale(TypedDict):
    """NFT sale record."""
    timestamp: str
    block_num: float
    tx_hash: str
    token: str
    token_id: str
    symbol: str
    name: str
    offerer: str
    recipient: str
    sale_amount: float
    sale_currency: str


class NFTSalesResponse(TypedDict):
    """Response for NFT sales endpoint."""
    data: List[NFTSale]
    statistics: Optional[Statistics]


# ===== Balance Types =====

class Balance(TypedDict):
    """Token balance record."""
    block_num: float
    datetime: str
    contract: str
    amount: str
    value: float
    network_id: str  # API returns string format
    symbol: Optional[str]
    decimals: Optional[float]
    price_usd: Optional[float]
    value_usd: Optional[float]
    low_liquidity: Optional[bool]


class BalancesResponse(BaseResponse):
    """Response for balances endpoint."""
    data: List[Balance]


class SolanaBalance(TypedDict):
    """Solana token balance record."""
    block_num: float
    datetime: str
    timestamp: float
    program_id: str
    token_account: str
    mint: str
    amount: str
    value: float
    decimals: float
    network_id: str  # API returns string format


class SolanaBalancesResponse(BaseResponse):
    """Response for Solana balances endpoint."""
    data: List[SolanaBalance]


# ===== Transfer Types =====

Transfer = TypedDict('Transfer', {
    'block_num': float,
    'datetime': str,
    'timestamp': float,
    'transaction_id': str,
    'contract': str,
    'from': str,  # API uses 'from' field
    'to': str,
    'value': float,  # API uses 'value' not 'amount'
    'symbol': Optional[str],
    'decimals': Optional[float],
}, total=False)


class TransfersResponse(BaseResponse):
    """Response for transfers endpoint."""
    data: List[Transfer]


class SolanaTransfer(TypedDict):
    """Solana token transfer record."""
    block_num: float
    datetime: str
    timestamp: float
    signature: str
    program_id: str
    mint: str
    authority: str
    source: str
    destination: str
    amount: str
    value: float
    decimals: Optional[float]
    network_id: str  # API returns string format


class SolanaTransfersResponse(BaseResponse):
    """Response for Solana transfers endpoint."""
    data: List[SolanaTransfer]


# ===== Token Types =====

class TokenIcon(TypedDict):
    """Token icon information."""
    web3icon: str


class Token(TypedDict, total=False):
    """Token metadata."""
    block_num: float
    datetime: str
    contract: str
    circulating_supply: Union[str, float]  # API can return either
    holders: float
    network_id: str  # API returns string format
    icon: Optional[TokenIcon]
    symbol: Optional[str]
    name: Optional[str]
    decimals: Optional[float]
    price_usd: Optional[float]
    market_cap: Optional[float]
    low_liquidity: Optional[bool]


class TokensResponse(BaseResponse):
    """Response for tokens endpoint."""
    data: List[Token]


class TokenHolder(TypedDict):
    """Token holder information."""
    block_num: float
    datetime: str
    address: str
    amount: str
    value: float
    network_id: str  # API returns string format
    symbol: Optional[str]
    decimals: Optional[float]
    price_usd: Optional[float]
    value_usd: Optional[float]
    low_liquidity: Optional[bool]


class TokenHoldersResponse(TypedDict):
    """Response for token holders endpoint."""
    data: List[TokenHolder]
    statistics: Optional[Statistics]


# ===== Swap Types =====

class SwapToken(TypedDict):
    """Token information in swap."""
    address: str
    symbol: str
    decimals: float


class Swap(TypedDict, total=False):
    """DEX swap record."""
    block_num: float
    datetime: str
    timestamp: float
    network_id: str  # API returns different format than we send
    transaction_id: str
    caller: str
    sender: str
    recipient: Optional[str]
    factory: str
    pool: str
    token0: SwapToken
    token1: SwapToken
    amount0: str
    amount1: str
    price0: float
    price1: float
    value0: float
    value1: float
    fee: Optional[str]
    protocol: str


class SwapsResponse(BaseResponse):
    """Response for swaps endpoint."""
    data: List[Swap]


class SolanaMint(TypedDict):
    """Solana mint information."""
    address: str
    symbol: str
    decimals: float


class SolanaSwap(TypedDict, total=False):
    """Solana swap record."""
    block_num: float
    datetime: str
    timestamp: float
    transaction_index: Optional[float]
    instruction_index: Optional[float]
    signature: str
    program_id: str
    program_name: str
    user: str
    amm: str
    amm_name: str
    amm_pool: Optional[str]
    input_mint: Union[SolanaMint, str]  # API can return either dict or string
    input_amount: float
    output_mint: Union[SolanaMint, str]  # API can return either dict or string
    output_amount: float
    network_id: str  # API returns string format


class SolanaSwapsResponse(BaseResponse):
    """Response for Solana swaps endpoint."""
    data: List[SolanaSwap]


# ===== Pool Types =====

class Pool(TypedDict):
    """Liquidity pool information."""
    block_num: float
    datetime: str
    network_id: str  # API returns string format
    transaction_id: str
    factory: str
    pool: str
    token0: SwapToken
    token1: SwapToken
    fee: float
    protocol: str


class PoolsResponse(BaseResponse):
    """Response for pools endpoint."""
    data: List[Pool]


# ===== OHLC Types =====

class OHLC(TypedDict):
    """OHLC price data."""
    datetime: str
    ticker: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    uaw: float
    transactions: float


class OHLCResponse(BaseResponse):
    """Response for OHLC endpoints."""
    data: List[OHLC]


# ===== Historical Types =====

class HistoricalBalance(TypedDict):
    """Historical balance data."""
    datetime: str
    contract: str
    name: str
    symbol: str
    decimals: str
    open: float
    high: float
    low: float
    close: float


class HistoricalBalancesResponse(TypedDict):
    """Response for historical balances endpoint."""
    data: List[HistoricalBalance]
    statistics: Optional[Statistics]


# ===== Monitoring Types =====

class ErrorResponse(TypedDict):
    """Error response structure."""
    status: int
    code: str
    message: str


class VersionResponse(TypedDict):
    """Version information response."""
    version: str
    date: str
    commit: str


class NetworkIcon(TypedDict):
    """Network icon information."""
    web3Icons: dict


class Network(TypedDict):
    """Network information."""
    id: str
    fullName: str
    shortName: str
    caip2Id: str
    networkType: str
    icon: NetworkIcon
    alias: List[str]


class NetworksResponse(TypedDict):
    """Response for networks endpoint."""
    networks: List[Network]


# ===== Export All Types =====

__all__ = [
    # Enums
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
    
    # Common
    "Statistics",
    "BaseResponse",
    "ErrorResponse",
    
    # NFT
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
    
    # Balances
    "Balance",
    "BalancesResponse",
    "SolanaBalance",
    "SolanaBalancesResponse",
    
    # Transfers
    "Transfer",
    "TransfersResponse",
    "SolanaTransfer",
    "SolanaTransfersResponse",
    
    # Tokens
    "TokenIcon",
    "Token",
    "TokensResponse",
    "TokenHolder",
    "TokenHoldersResponse",
    
    # Swaps
    "SwapToken",
    "Swap",
    "SwapsResponse",
    "SolanaMint",
    "SolanaSwap",
    "SolanaSwapsResponse",
    
    # Pools
    "Pool",
    "PoolsResponse",
    
    # OHLC
    "OHLC",
    "OHLCResponse",
    
    # Historical
    "HistoricalBalance",
    "HistoricalBalancesResponse",
    
    # Monitoring
    "VersionResponse",
    "Network",
    "NetworksResponse",
]