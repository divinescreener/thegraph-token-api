"""
Test suite for the Unified Price API system.

Tests the Currency enum, UnifiedPriceAPI class, and all price calculation functionality
across different blockchains with proper mocking and error handling.
"""

import time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from thegraph_token_api.constants import get_currency_config, is_currency_supported
from thegraph_token_api.price_utils import PriceCalculator, create_price_cache
from thegraph_token_api.types import Currency
from thegraph_token_api.unified_price_api import UnifiedPriceAPI


class TestCurrencyEnum:
    """Test Currency enum functionality."""

    def test_currency_enum_values(self):
        """Test that Currency enum has expected values."""
        assert Currency.ETH == "ETH"
        assert Currency.SOL == "SOL"
        assert Currency.POL == "POL"
        assert str(Currency.ETH) == "ETH"
        assert str(Currency.SOL) == "SOL"
        assert str(Currency.POL) == "POL"

    def test_currency_enum_creation(self):
        """Test creating Currency enum from strings."""
        assert Currency("ETH") == Currency.ETH
        assert Currency("SOL") == Currency.SOL
        assert Currency("POL") == Currency.POL
        # Note: Currency enum is case-sensitive as designed

    def test_currency_enum_invalid(self):
        """Test that invalid currency strings raise ValueError."""
        with pytest.raises(ValueError):
            Currency("BTC")
        with pytest.raises(ValueError):
            Currency("INVALID")
        with pytest.raises(ValueError):
            Currency("")


class TestCurrencyConfig:
    """Test currency configuration functions."""

    def test_get_currency_config_enum(self):
        """Test getting config with Currency enum."""
        eth_config = get_currency_config(Currency.ETH)
        assert eth_config is not None
        assert eth_config["blockchain"] == "ethereum"
        assert "token_config" in eth_config
        assert "dex_config" in eth_config

        sol_config = get_currency_config(Currency.SOL)
        assert sol_config is not None
        assert sol_config["blockchain"] == "solana"

        pol_config = get_currency_config(Currency.POL)
        assert pol_config is not None
        assert pol_config["blockchain"] == "ethereum"

    def test_get_currency_config_string(self):
        """Test getting config with string (utility function still supports strings)."""
        eth_config = get_currency_config("ETH")
        assert eth_config is not None
        assert eth_config["blockchain"] == "ethereum"

        sol_config = get_currency_config("sol")  # Case insensitive
        assert sol_config is not None
        assert sol_config["blockchain"] == "solana"

        pol_config = get_currency_config("POL")
        assert pol_config is not None
        assert pol_config["blockchain"] == "ethereum"

    def test_get_currency_config_invalid(self):
        """Test getting config with invalid currency."""
        assert get_currency_config("BTC") is None
        assert get_currency_config("INVALID") is None

    def test_is_currency_supported_enum(self):
        """Test currency support check with enum."""
        assert is_currency_supported(Currency.ETH) is True
        assert is_currency_supported(Currency.SOL) is True
        assert is_currency_supported(Currency.POL) is True

    def test_is_currency_supported_string(self):
        """Test currency support check with string (utility function still supports strings)."""
        assert is_currency_supported("ETH") is True
        assert is_currency_supported("sol") is True  # Case insensitive
        assert is_currency_supported("POL") is True
        assert is_currency_supported("BTC") is False
        assert is_currency_supported("INVALID") is False


class TestPriceCalculator:
    """Test price calculation utilities."""

    def test_price_calculator_statistics(self):
        """Test price statistics calculation."""
        calculator = PriceCalculator()
        prices = [100.0, 102.0, 98.0, 101.0, 99.0]

        stats = calculator.calculate_price_statistics(prices)
        assert stats is not None
        assert stats["price"] == 100.0  # Median
        assert stats["mean_price"] == 100.0
        assert stats["trades_analyzed"] == 5
        assert 0 <= stats["confidence"] <= 1
        assert stats["min_price"] == 98.0
        assert stats["max_price"] == 102.0

    def test_price_calculator_insufficient_data(self):
        """Test price calculator with insufficient data."""
        calculator = PriceCalculator()
        prices = [100.0]  # Less than min_sample_size (3)

        stats = calculator.calculate_price_statistics(prices)
        assert stats is None

    def test_outlier_filtering_basic(self):
        """Test basic outlier filtering."""
        calculator = PriceCalculator()
        prices = [100.0, 101.0, 102.0, 15000.0, 99.0]  # 15000 is outlier (above 10000 max)

        filtered = calculator.filter_outliers_basic(prices)
        assert 15000.0 not in filtered
        assert len(filtered) == 4

    def test_outlier_filtering_iqr(self):
        """Test IQR outlier filtering."""
        calculator = PriceCalculator()
        prices = [100.0, 101.0, 102.0, 103.0, 104.0, 200.0]  # 200 is outlier

        filtered = calculator.filter_outliers_iqr(prices)
        assert 200.0 not in filtered

    def test_progressive_retry_params(self):
        """Test progressive retry parameter generation."""
        calculator = PriceCalculator()

        trades1, minutes1 = calculator.progressive_retry_params(1)
        trades2, minutes2 = calculator.progressive_retry_params(2)

        assert trades2 >= trades1
        assert minutes2 >= minutes1
        assert trades1 >= 100  # Base trades
        assert minutes1 >= 15  # Base minutes


class TestPriceData:
    """Test PriceData cache functionality."""

    def test_price_data_creation(self):
        """Test creating PriceData cache entry."""
        stats = {"price": 100.0, "mean_price": 100.0, "std_deviation": 1.0, "confidence": 0.8, "timestamp": time.time()}

        cache = create_price_cache(100.0, stats)
        assert cache.price == 100.0
        assert cache.stats == stats
        assert isinstance(cache.cached_at, float)

    def test_price_data_freshness_stable(self):
        """Test cache freshness for stable market."""
        stats = {
            "price": 100.0,
            "mean_price": 100.0,
            "std_deviation": 0.1,  # Low volatility
        }

        cache = create_price_cache(100.0, stats)
        assert cache.is_fresh is True  # Should be fresh immediately

    def test_price_data_freshness_volatile(self):
        """Test cache freshness for volatile market."""
        stats = {
            "price": 100.0,
            "mean_price": 100.0,
            "std_deviation": 10.0,  # High volatility
        }

        cache = create_price_cache(100.0, stats)
        assert cache.is_fresh is True  # Should be fresh immediately

        # Mock old timestamp
        cache.cached_at = time.time() - 120  # 2 minutes ago
        # Should be stale due to high volatility (TTL = 60s)
        assert cache.is_fresh is False


class TestUnifiedPriceAPI:
    """Test unified price oracle functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_token_api = MagicMock()
        self.mock_evm_client = AsyncMock()
        self.mock_svm_client = AsyncMock()

        # Configure mock API
        self.mock_token_api.evm.return_value = self.mock_evm_client
        self.mock_token_api.svm.return_value = self.mock_svm_client

        self.oracle = UnifiedPriceAPI(self.mock_token_api)

    @pytest.mark.asyncio
    async def test_unified_price_api_initialization(self):
        """Test Unified Price API initialization."""
        assert self.oracle.token_api == self.mock_token_api
        assert isinstance(self.oracle.calculator, PriceCalculator)
        assert isinstance(self.oracle._price_caches, dict)

    @pytest.mark.asyncio
    async def test_get_price_enum_input(self):
        """Test getting price with Currency enum input."""
        # Mock successful price calculation
        with patch.object(self.oracle, "_fetch_price") as mock_fetch:
            mock_fetch.return_value = {
                "price": 3500.0,
                "confidence": 0.9,
                "trades_analyzed": 10,
                "timestamp": time.time(),
            }

            price = await self.oracle.get(Currency.ETH)
            assert price == 3500.0
            mock_fetch.assert_called_once_with(Currency.ETH)

    @pytest.mark.asyncio
    async def test_get_price_non_enum_input(self):
        """Test getting price with non-enum input raises TypeError."""
        with pytest.raises(TypeError, match="Currency must be Currency enum"):
            await self.oracle.get("SOL")

    @pytest.mark.asyncio
    async def test_get_price_invalid_type(self):
        """Test getting price with invalid type."""
        with pytest.raises(TypeError, match="Currency must be Currency enum"):
            await self.oracle.get(123)

    @pytest.mark.asyncio
    async def test_get_price_with_stats(self):
        """Test getting price with statistics."""
        mock_stats = {
            "price": 3500.0,
            "mean_price": 3505.0,
            "std_deviation": 50.0,
            "confidence": 0.9,
            "trades_analyzed": 15,
            "timestamp": time.time(),
        }

        with patch.object(self.oracle, "_fetch_price") as mock_fetch:
            mock_fetch.return_value = mock_stats

            result = await self.oracle.get(Currency.ETH, include_stats=True)
            assert result == mock_stats
            assert result["price"] == 3500.0
            assert result["confidence"] == 0.9

    @pytest.mark.asyncio
    async def test_get_price_cache_hit(self):
        """Test price cache hit."""
        # First call
        with patch.object(self.oracle, "_fetch_price") as mock_fetch:
            mock_fetch.return_value = {
                "price": 3500.0,
                "confidence": 0.9,
                "trades_analyzed": 10,
                "timestamp": time.time(),
            }

            price1 = await self.oracle.get(Currency.ETH)
            assert price1 == 3500.0
            assert mock_fetch.call_count == 1

            # Second call should use cache
            price2 = await self.oracle.get(Currency.ETH)
            assert price2 == 3500.0
            assert mock_fetch.call_count == 1  # No additional call

    @pytest.mark.asyncio
    async def test_get_price_force_refresh(self):
        """Test force refresh bypasses cache."""
        with patch.object(self.oracle, "_fetch_price") as mock_fetch:
            mock_fetch.return_value = {
                "price": 3500.0,
                "confidence": 0.9,
                "trades_analyzed": 10,
                "timestamp": time.time(),
            }

            # First call
            await self.oracle.get(Currency.ETH)
            assert mock_fetch.call_count == 1

            # Force refresh should bypass cache
            await self.oracle.get(Currency.ETH, force_refresh=True)
            assert mock_fetch.call_count == 2

    @pytest.mark.asyncio
    async def test_get_price_fetch_failure(self):
        """Test price fetch failure returns None."""
        with patch.object(self.oracle, "_fetch_price") as mock_fetch:
            mock_fetch.return_value = None

            price = await self.oracle.get(Currency.ETH)
            assert price is None

    @pytest.mark.asyncio
    async def test_get_supported_currencies(self):
        """Test getting supported currencies."""
        currencies = await self.oracle.get_supported_currencies()
        assert isinstance(currencies, list)
        assert Currency.ETH in currencies
        assert Currency.SOL in currencies
        assert Currency.POL in currencies

    @pytest.mark.asyncio
    async def test_is_supported(self):
        """Test currency support checking."""
        assert await self.oracle.is_supported(Currency.ETH) is True
        assert await self.oracle.is_supported(Currency.SOL) is True
        assert await self.oracle.is_supported(Currency.POL) is True

    @pytest.mark.asyncio
    async def test_is_supported_invalid_type(self):
        """Test is_supported with invalid type."""
        with pytest.raises(TypeError, match="Currency must be Currency enum"):
            await self.oracle.is_supported("BTC")

    @pytest.mark.asyncio
    async def test_clear_cache_specific(self):
        """Test clearing specific currency cache."""
        # Add some cache entries
        self.oracle._price_caches[Currency.ETH] = create_price_cache(
            3500.0, {"price": 3500.0, "timestamp": time.time()}
        )
        self.oracle._price_caches[Currency.SOL] = create_price_cache(150.0, {"price": 150.0, "timestamp": time.time()})

        # Clear ETH cache
        await self.oracle.clear_cache(Currency.ETH)
        assert Currency.ETH not in self.oracle._price_caches
        assert Currency.SOL in self.oracle._price_caches

    @pytest.mark.asyncio
    async def test_clear_cache_all(self):
        """Test clearing all cache."""
        # Add some cache entries
        self.oracle._price_caches[Currency.ETH] = create_price_cache(
            3500.0, {"price": 3500.0, "timestamp": time.time()}
        )
        self.oracle._price_caches[Currency.SOL] = create_price_cache(150.0, {"price": 150.0, "timestamp": time.time()})

        # Clear all cache
        await self.oracle.clear_cache()
        assert len(self.oracle._price_caches) == 0

    @pytest.mark.asyncio
    async def test_fetch_ethereum_price(self):
        """Test fetching Ethereum price."""
        # Mock swap data
        mock_swaps = [
            {
                "token0": {"address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "decimals": 18},
                "token1": {"address": "0xA0b86a33E7c473D00e05A7B8A4bcF1e50e93D1Af", "decimals": 6},
                "amount0": "1000000000000000000",  # 1 ETH
                "amount1": "3500000000",  # 3500 USDC
            }
        ]

        # Mock the _fetch_ethereum_swaps method to return the mock swaps
        with patch.object(self.oracle, "_fetch_ethereum_swaps") as mock_fetch_swaps:
            mock_fetch_swaps.return_value = mock_swaps

            config = get_currency_config(Currency.ETH)
            result = await self.oracle._fetch_ethereum_price(config)

            assert result is not None
            assert "price" in result
            assert "confidence" in result

    @pytest.mark.asyncio
    async def test_fetch_solana_price(self):
        """Test fetching Solana price."""
        # Mock swap data
        mock_swaps = [
            {
                "input_mint": {"address": "So11111111111111111111111111111111111111112"},
                "output_mint": {"address": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"},
                "input_amount": 1000000000,  # 1 SOL (9 decimals)
                "output_amount": 150000000,  # 150 USDC (6 decimals)
            }
        ]

        # Mock the _fetch_solana_swaps method to return the mock swaps
        with patch.object(self.oracle, "_fetch_solana_swaps") as mock_fetch_swaps:
            mock_fetch_swaps.return_value = mock_swaps

            config = get_currency_config(Currency.SOL)
            result = await self.oracle._fetch_solana_price(config)

            assert result is not None
            assert "price" in result
            assert "confidence" in result

    @pytest.mark.asyncio
    async def test_fetch_price_ethereum(self):
        """Test _fetch_price routing to Ethereum."""
        with patch.object(self.oracle, "_fetch_ethereum_price") as mock_fetch:
            mock_fetch.return_value = {"price": 3500.0}

            result = await self.oracle._fetch_price(Currency.ETH)
            assert result == {"price": 3500.0}
            mock_fetch.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_price_solana(self):
        """Test _fetch_price routing to Solana."""
        with patch.object(self.oracle, "_fetch_solana_price") as mock_fetch:
            mock_fetch.return_value = {"price": 150.0}

            result = await self.oracle._fetch_price(Currency.SOL)
            assert result == {"price": 150.0}
            mock_fetch.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_price_pol(self):
        """Test _fetch_price routing to POL (Ethereum)."""
        with patch.object(self.oracle, "_fetch_ethereum_price") as mock_fetch:
            mock_fetch.return_value = {"price": 0.5}

            result = await self.oracle._fetch_price(Currency.POL)
            assert result == {"price": 0.5}
            mock_fetch.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_ethereum_swaps(self):
        """Test fetching Ethereum swaps."""
        mock_swaps = [{"mock": "swap"}]
        self.mock_evm_client.get_swaps.return_value = mock_swaps

        # Need to set up the client properly
        self.mock_token_api.evm.return_value = self.mock_evm_client

        result = await self.oracle._fetch_ethereum_swaps("uniswap_v3", 100, 15)

        assert result == mock_swaps
        self.mock_evm_client.get_swaps.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_solana_swaps(self):
        """Test fetching Solana swaps."""
        mock_swaps = [{"mock": "swap"}]
        self.mock_svm_client.get_swaps.return_value = mock_swaps

        # Need to set up the client properly
        self.mock_token_api.svm.return_value = self.mock_svm_client

        result = await self.oracle._fetch_solana_swaps("jupiter_v6", "token_addr", "base_addr", 100, 15)

        assert len(result) > 0  # Should convert to dicts
        self.mock_svm_client.get_swaps.assert_called()

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling in price fetching."""
        # Mock exception in fetch
        with patch.object(self.oracle, "_fetch_price") as mock_fetch:
            mock_fetch.side_effect = Exception("Network error")

            result = await self.oracle.get(Currency.ETH)
            assert result is None  # Should return None on error

    @pytest.mark.asyncio
    async def test_low_confidence_handling(self):
        """Test handling of low confidence price data."""
        with patch.object(self.oracle, "_fetch_price") as mock_fetch:
            # Mock low confidence data
            mock_fetch.return_value = {
                "price": 3500.0,
                "confidence": 0.05,  # Very low confidence
                "trades_analyzed": 1,  # Insufficient trades
                "timestamp": time.time(),
            }

            result = await self.oracle.get(Currency.ETH)
            assert result is None  # Should reject low confidence data
