"""Sample API Client for OBIS Energy Reader."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout


class OBISEnergyReaderApiClientError(Exception):
    """Exception to indicate a general API error."""


class OBISEnergyReaderApiClientCommunicationError(
    OBISEnergyReaderApiClientError,
):
    """Exception to indicate a communication error."""


class OBISEnergyReaderApiClientAuthenticationError(
    OBISEnergyReaderApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise OBISEnergyReaderApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class OBISEnergyReaderApiClient:
    """OBIS Energy Reader API Client."""

    def __init__(
        self,
        username: str,
        password: str,
        obis_url: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """OBIS Energy Reader API Client."""
        self._username = username
        self._password = password
        self._obis_url = obis_url
        self._session = session

    async def async_get_data(self) -> Any:
        """Get OBIS data from the configured endpoint."""
        return await self._api_wrapper(
            method="get",
            url=self._obis_url,
        )

    async def async_set_title(self) -> Any:
        """Set tile dummy method for compatibility (not used for OBIS)."""
        return None

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise OBISEnergyReaderApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise OBISEnergyReaderApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise OBISEnergyReaderApiClientError(
                msg,
            ) from exception
