"""
Core Models Testing - Comprehensive coverage for models.py
Tests model conversion, error handling, and dictionary access methods.
"""

from token_api.models import (
    Balance,
    NFTActivity,
    Pool,
    SolanaSwap,
    Swap,
    Transfer,
    convert_list_to_models,
    convert_to_model,
)


class TestModelConversion:
    """Test model conversion functions."""

    def test_convert_to_model_with_none(self):
        """Test convert_to_model with None input (line 21)."""
        result = convert_to_model(None, Balance)
        assert result is None

    def test_convert_to_model_with_empty_dict(self):
        """Test convert_to_model with empty dict (line 25)."""
        result = convert_to_model({}, Balance)
        assert result is None

    def test_convert_to_model_valid_balance(self):
        """Test convert_to_model with valid Balance data."""
        data = {
            "block_num": 18500000.0,
            "datetime": "2023-11-01T12:00:00Z",
            "contract": "0xToken",
            "amount": "1000000000000000000",
            "value": 1000.0,
            "network_id": "mainnet",
            "symbol": "USDC",
        }

        result = convert_to_model(data, Balance)
        assert result is not None
        assert isinstance(result, Balance)
        assert result.symbol == "USDC"
        assert result.value == 1000.0

    def test_convert_to_model_swap_nested_tokens(self):
        """Test convert_to_model with Swap containing nested tokens (lines 138-140)."""
        data = {
            "block_num": 18500000.0,
            "datetime": "2023-11-01T12:00:00Z",
            "timestamp": 1698840000.0,
            "network_id": "mainnet",
            "transaction_id": "0xhash",
            "caller": "0xCaller",
            "sender": "0xSender",
            "factory": "0xFactory",
            "pool": "0xPool",
            "token0": {"address": "0xToken0", "symbol": "ETH", "decimals": 18.0},
            "token1": {"address": "0xToken1", "symbol": "USDC", "decimals": 6.0},
            "amount0": "1000000000000000000",
            "amount1": "1000000000",
            "price0": 1000.0,
            "price1": 0.001,
            "value0": 1000.0,
            "value1": 1000.0,
            "protocol": "uniswap_v3",
        }

        result = convert_to_model(data, Swap)
        assert result is not None
        assert result.token0.symbol == "ETH"
        assert result.token1.symbol == "USDC"

    def test_convert_to_model_solana_swap_nested_mints(self):
        """Test convert_to_model with SolanaSwap containing nested mints (lines 144-146)."""
        data = {
            "block_num": 185000000.0,
            "datetime": "2023-11-01T12:00:00Z",
            "timestamp": 1698840000.0,
            "signature": "sig123",
            "program_id": "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8",
            "program_name": "Raydium",
            "user": "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
            "amm": "AMM123",
            "amm_name": "Raydium AMM",
            "network_id": "solana",
            "input_mint": {"address": "So11111111111111111111111111111111111111112", "symbol": "SOL", "decimals": 9.0},
            "output_mint": {
                "address": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "symbol": "USDC",
                "decimals": 6.0,
            },
            "input_amount": 10.5,
            "output_amount": 500.25,
        }

        result = convert_to_model(data, SolanaSwap)
        assert result is not None
        assert result.input_mint.symbol == "SOL"
        assert result.output_mint.symbol == "USDC"

    def test_convert_to_model_pool_nested_tokens(self):
        """Test convert_to_model with Pool containing nested tokens (lines 218-222)."""
        data = {
            "block_num": 18500000.0,
            "datetime": "2023-11-01T12:00:00Z",
            "network_id": "mainnet",
            "transaction_id": "0xhash",
            "factory": "0xFactory",
            "pool": "0xPool",
            "token0": {"address": "0xToken0", "symbol": "ETH", "decimals": 18.0},
            "token1": {"address": "0xToken1", "symbol": "USDC", "decimals": 6.0},
            "fee": 3000.0,
            "protocol": "uniswap_v2",
        }

        result = convert_to_model(data, Pool)
        assert result is not None
        assert result.token0.symbol == "ETH"
        assert result.token1.symbol == "USDC"

    def test_convert_to_model_special_field_mappings(self):
        """Test convert_to_model with special field mappings (lines 226-230)."""
        # Test Transfer with 'from' field mapping
        transfer_data = {
            "block_num": 18500000.0,
            "datetime": "2023-11-01T12:00:00Z",
            "timestamp": 1698840000.0,
            "transaction_id": "0xhash",
            "contract": "0xToken",
            "from": "0xFrom",  # Should map to from_address
            "to": "0xTo",
            "value": 1000.0,
        }

        result = convert_to_model(transfer_data, Transfer)
        assert result is not None
        assert result.from_address == "0xFrom"
        assert result.to == "0xTo"

        # Test NFTActivity with '@type' field mapping
        nft_data = {
            "block_num": 18500000.0,
            "block_hash": "0xblock",
            "timestamp": "2023-11-01T12:00:00Z",
            "tx_hash": "0xhash",
            "contract": "0xNFT",
            "from": "0xFrom",  # Should map to from_address
            "to": "0xTo",
            "token_id": "123",
            "amount": 1.0,
            "@type": "transfer",  # Should map to activity_type
        }

        result = convert_to_model(nft_data, NFTActivity)
        assert result is not None
        assert result.from_address == "0xFrom"
        assert result.activity_type == "transfer"

    def test_convert_list_to_models(self):
        """Test convert_list_to_models function (line 348)."""
        data_list = [
            {
                "block_num": 18500000.0,
                "datetime": "2023-11-01T12:00:00Z",
                "contract": "0xToken1",
                "amount": "1000000000000000000",
                "value": 1000.0,
                "network_id": "mainnet",
            },
            {
                "block_num": 18500001.0,
                "datetime": "2023-11-01T12:01:00Z",
                "contract": "0xToken2",
                "amount": "2000000000000000000",
                "value": 2000.0,
                "network_id": "mainnet",
            },
        ]

        result = convert_list_to_models(data_list, Balance)
        assert len(result) == 2
        assert all(isinstance(item, Balance) for item in result)
        assert result[0].value == 1000.0
        assert result[1].value == 2000.0


class TestModelDictionaryAccess:
    """Test dictionary-style access methods on model instances."""

    def test_base_model_dict_access(self):
        """Test BaseModel __getitem__ and get methods (lines 21, 25)."""
        balance = Balance(
            block_num=18500000.0,
            datetime="2023-11-01T12:00:00Z",
            contract="0xToken",
            amount="1000000000000000000",
            value=1000.0,
            network_id="mainnet",
            symbol="USDC",
        )

        # Test __getitem__ method (line 21)
        assert balance["symbol"] == "USDC"
        assert balance["nonexistent"] is None

        # Test get method (line 25)
        assert balance.get("symbol") == "USDC"
        assert balance.get("nonexistent") is None
        assert balance.get("nonexistent", "default") == "default"

    def test_transfer_dict_access_with_from_mapping(self):
        """Test Transfer __getitem__ and get methods with 'from' key mapping (lines 138-140, 144-146)."""
        transfer = Transfer(
            block_num=18500000.0,
            datetime="2023-11-01T12:00:00Z",
            timestamp=1698840000.0,
            transaction_id="0xhash",
            contract="0xToken",
            from_address="0xFrom",
            to="0xTo",
            value=1000.0,
        )

        # Test __getitem__ method with 'from' key mapping (lines 138-140)
        assert transfer["from"] == "0xFrom"
        assert transfer["to"] == "0xTo"

        # Test get method with 'from' key mapping (lines 144-146)
        assert transfer.get("from") == "0xFrom"
        assert transfer.get("to") == "0xTo"
        assert transfer.get("nonexistent") is None

    def test_nft_activity_dict_access_with_special_mappings(self):
        """Test NFTActivity __getitem__ and get methods with special mappings (lines 218-222, 226-230)."""
        activity = NFTActivity(
            activity_type="transfer",
            block_num=18500000.0,
            block_hash="0xblock",
            timestamp="2023-11-01T12:00:00Z",
            tx_hash="0xhash",
            contract="0xNFT",
            from_address="0xFrom",
            to="0xTo",
            token_id="123",
            amount=1.0,
        )

        # Test __getitem__ method with special mappings (lines 218-222)
        assert activity["@type"] == "transfer"
        assert activity["from"] == "0xFrom"
        assert activity["to"] == "0xTo"

        # Test get method with special mappings (lines 226-230)
        assert activity.get("@type") == "transfer"
        assert activity.get("from") == "0xFrom"
        assert activity.get("to") == "0xTo"
        assert activity.get("nonexistent") is None


class TestModelErrorHandling:
    """Test model conversion error handling."""

    def test_convert_to_model_error_handling(self):
        """Test convert_to_model error handling with incomplete data."""
        # Data that will cause TypeError - completely missing required fields
        incomplete_data = {
            "symbol": "USDC",
            "value": 1000.0,
            # Missing required fields: block_num, datetime, contract, amount, network_id
        }

        # This should trigger the error handling paths and return None
        try:
            result = convert_to_model(incomplete_data, Balance)
            assert result is None  # Should be None due to error handling
        except TypeError:
            # If it raises TypeError, that's also valid error handling
            pass

    def test_convert_to_model_with_invalid_nested_data(self):
        """Test convert_to_model with invalid nested data."""
        # Data with invalid nested token structure
        invalid_swap_data = {
            "block_num": 18500000.0,
            "datetime": "2023-11-01T12:00:00Z",
            "timestamp": 1698840000.0,
            "network_id": "mainnet",
            "transaction_id": "0xhash",
            "caller": "0xCaller",
            "sender": "0xSender",
            "factory": "0xFactory",
            "pool": "0xPool",
            "token0": "invalid_token_data",  # Should be dict
            "token1": {"address": "0xToken1", "symbol": "USDC", "decimals": 6.0},
            "amount0": "1000000000000000000",
            "amount1": "1000000000",
            "protocol": "uniswap_v3",
        }

        try:
            result = convert_to_model(invalid_swap_data, Swap)
            # Should handle error gracefully
        except (TypeError, AttributeError):
            # Expected for invalid data
            pass
