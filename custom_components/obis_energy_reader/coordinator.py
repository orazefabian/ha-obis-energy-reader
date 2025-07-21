"""DataUpdateCoordinator for obis_energy_reader."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    OBISEnergyReaderApiClientAuthenticationError,
    OBISEnergyReaderApiClientError,
)

if TYPE_CHECKING:
    from .data import OBISEnergyReaderConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class BlueprintDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass, logger, name, update_interval):
        super().__init__(
            hass,
            logger,
            name=name,
            update_interval=update_interval,
        )
        self.api = None

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        if self.api is None:
            # Try to get the API client from the integration runtime data
            entry = next(iter(self.hass.config_entries.async_entries(DOMAIN)), None)
            if entry and hasattr(entry, "runtime_data"):
                self.api = entry.runtime_data.client
        if self.api:
            return await self.api.async_get_data()
        return {}
