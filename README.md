# Token API Client (Beta)

A clean, intuitive Python client for The Graph Token API with elegant EVM/SVM separation. Get blockchain data from Ethereum, Polygon, Solana, and more with a simple, unified interface.

*Current Spec version: 4.0*

## Quick Start

### Installation

```bash
pip install divine-thegraph-token-api
```

### Basic Usage

```python
import anyio
from token_api import TokenAPI, SwapPrograms, Protocol

async def main():
    api = TokenAPI()  # Auto-loads from .env
    
    # EVM chains (Ethereum, Polygon, BSC, etc.)
    eth_balances = await api.evm.balances("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
    eth_nfts = await api.evm.nfts.ownerships("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
    eth_swaps = await api.evm.swaps(protocol=Protocol.UNISWAP_V3, limit=10)
    
    # SVM (Solana)
    sol_balances = await api.svm.balances(mint="So11111111111111111111111111111111111111112")
    sol_swaps = await api.svm.swaps(program_id=SwapPrograms.RAYDIUM, limit=10)
    
    # Utility
    health = await api.health()

anyio.run(main)
```

### API Key Setup

Create a `.env` file:
```bash
THEGRAPH_API_KEY=your_api_key_here
```

Get your free API key at: [thegraph.market](https://thegraph.market) (click "Get API Key")

## Features

- 🏗️ **Clean Architecture**: Separated EVM and SVM interfaces
- 🎨 **Nested Organization**: `api.evm.nfts.ownerships()` for better structure  
- ⚡ **Multi-Chain**: Ethereum, Polygon, BSC, Arbitrum, Optimism, Base, Solana
- 🔧 **Time Filtering**: Get trades from specific time ranges
- 📦 **Type Safety**: Full type hints and runtime validation
- 🚀 **Async/Await**: Built for modern Python async patterns
- 🔄 **Auto Environment**: Loads API keys from `.env` automatically

## API Structure

### EVM Chains
```python
# Token Balances
balances = await api.evm.balances(address)

# NFT Operations  
nfts = await api.evm.nfts.ownerships(address)
collection = await api.evm.nfts.collection(contract)
activities = await api.evm.nfts.activities(contract)

# DeFi Trading
swaps = await api.evm.swaps(protocol=Protocol.UNISWAP_V3)
pools = await api.evm.pools(token=token_address)

# Price Data
prices = await api.evm.price_history(token, interval="1d", days=7)
pool_data = await api.evm.pool_history(pool, interval="1h")

# Token Information
token_info = await api.evm.token_info(contract)
holders = await api.evm.token_holders(contract)

# Transfers
transfers = await api.evm.transfers(from_address=address)
```

### SVM (Solana)
```python
# SPL Token Balances
balances = await api.svm.balances(mint=mint_address)

# SPL Transfers
transfers = await api.svm.transfers(mint=mint_address)

# DEX Swaps with Time Filtering
from datetime import datetime, timedelta
end_time = int(datetime.now().timestamp())
start_time = int((datetime.now() - timedelta(minutes=30)).timestamp())

swaps = await api.svm.swaps(
    program_id=SwapPrograms.RAYDIUM,
    start_time=start_time,
    end_time=end_time
)
```

## Supported Networks

**EVM**: Ethereum, Polygon, BSC, Arbitrum, Optimism, Avalanche, Base, Unichain  
**SVM**: Solana

**DEX Protocols**: Uniswap V2/V3, Raydium, Orca, Jupiter, Pump.fun

## Examples

Explore the [`examples/`](examples/) directory for comprehensive usage examples with real blockchain data:

```bash
# EVM examples
python examples/endpoints/evm/health.py      # API connectivity
python examples/endpoints/evm/balances.py    # Token balances
python examples/endpoints/evm/nfts.py        # NFT ownership

# SVM examples  
python examples/endpoints/svm/balances.py    # SPL balances
python examples/endpoints/svm/swaps.py       # Solana DEX swaps
```

## Documentation

📚 **[Complete API Reference](API_REFERENCE.md)** - Detailed documentation for all functions, parameters, and response schemas.

🌐 **[The Graph Token API Docs](https://thegraph.com/docs/en/token-api/quick-start/)** - Official API documentation, endpoints, and specifications.

The API reference includes:
- All function signatures and parameters
- Response schemas and examples  
- Error handling guidelines
- Type definitions and enums
- Advanced usage patterns

## Support

- 📖 **Documentation**: [API Reference](API_REFERENCE.md) | [Official API Docs](https://thegraph.com/docs/en/token-api/quick-start/)
- 💡 **Examples**: Browse the [`examples/`](examples/) directory
- 🐛 **Issues**: Report bugs on [GitHub Issues](https://github.com/your-repo/issues)
- 🔑 **API Key**: Get yours at [thegraph.market](https://thegraph.market) (click "Get API Key")

## License

MIT License - see [LICENSE](LICENSE) for details.