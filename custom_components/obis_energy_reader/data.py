"""Custom types for integration_blueprint."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import OBISEnergyReaderApiClient
    from .coordinator import BlueprintDataUpdateCoordinator


type OBISEnergyReaderConfigEntry = ConfigEntry[OBISEnergyReaderData]


@dataclass
class OBISEnergyReaderData:
    """Data for the OBIS Energy Reader."""

    client: OBISEnergyReaderApiClient
    coordinator: BlueprintDataUpdateCoordinator
    integration: Integration
