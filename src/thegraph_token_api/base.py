"""
Base client for The Graph Token API.

Provides shared functionality for authentication, networking, and monitoring endpoints.
"""

import os

# Import divine-requests (should be installed as a package)
from requests import NetworkingManager  # type: ignore[attr-defined]

from .types import NetworksResponse, VersionResponse


class BaseTokenAPI:
    """
    Base class for The Graph Token API clients.

    Provides shared functionality for authentication, networking, and monitoring.
    """

    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        """
        Initialize base API client.

        Args:
            api_key: Bearer token for API authentication
            base_url: API base URL (defaults to official endpoint)
        """
        self.api_key = api_key or os.getenv("THEGRAPH_API_KEY")
        self.base_url = base_url or os.getenv("THEGRAPH_API_ENDPOINT", "https://token-api.thegraph.com")

        if not self.api_key:
            raise ValueError(
                "API key is required. Provide it via api_key parameter or THEGRAPH_API_KEY environment variable."
            )

        self.manager = NetworkingManager()
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "TheGraphTokenAPI-Python-Client/0.1.0",
        }

    def _validate_pagination(self, limit: int, page: int) -> None:
        """Validate pagination parameters."""
        if not (1 <= limit <= 1000):
            raise ValueError("limit must be between 1 and 1000")
        if page < 1:
            raise ValueError("page must be 1 or greater")

    async def __aenter__(self):
        """Async context manager entry."""
        await self.manager.startup()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.manager.shutdown()

    # ===== Monitoring Methods =====

    async def get_health(self) -> str:
        """
        Get API health status.

        Returns:
            Health status string (should be "OK")
        """
        response = await self.manager.get(f"{self.base_url}/health", headers=self._headers)
        return str(response.text)

    async def get_version(self) -> VersionResponse:
        """
        Get API version information.

        Returns:
            VersionResponse with version details
        """
        response = await self.manager.get(
            f"{self.base_url}/version", headers=self._headers, expected_type=VersionResponse
        )
        return response.data  # type: ignore[no-any-return]

    async def get_networks(self) -> NetworksResponse:
        """
        Get supported networks.

        Returns:
            NetworksResponse with supported network information
        """
        response = await self.manager.get(
            f"{self.base_url}/networks", headers=self._headers, expected_type=NetworksResponse
        )
        return response.data  # type: ignore[no-any-return]
