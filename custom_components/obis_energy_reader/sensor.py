"""Sensor platform for OBIS Energy Reader."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import OBISEnergyReaderConfigEntry

OBIS_FIELDS = [
    ("1.8.0", "Total active energy consumed (import)", "kWh"),
    ("2.8.0", "Total active energy exported (export)", "kWh"),
    ("3.8.0", "Total positive reactive energy imported", "kvarh"),
    ("4.8.0", "Total negative reactive energy exported", "kvarh"),
    ("1.7.0", "Instantaneous active power (import)", "W"),
    ("2.7.0", "Instantaneous active power (export)", "W"),
    ("16.7.0", "Instantaneous total active power", "W"),
    ("timestamp", "Timestamp of the reading", None),
    ("uptime", "Uptime of the device", None),
    ("UTC", "Timestamp in UTC", None),
]


async def async_setup_entry(
    hass: HomeAssistant, # noqa: ARG001 Unused function argument: `hass`
    entry: OBISEnergyReaderConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up OBIS sensors from static field list."""
    coordinator = entry.runtime_data.coordinator
    sensors = [
        OBISEnergyReaderStaticSensor(coordinator, key, name, unit)
        for key, name, unit in OBIS_FIELDS
    ]
    async_add_entities(sensors, update_before_add=True)


class OBISEnergyReaderStaticSensor(SensorEntity):
    """Representation of an OBIS Energy Reader sensor."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        key: str,
        name: str,
        unit: str | None,
    ) -> None:
        """Initialize the OBIS sensor."""
        self.coordinator = coordinator
        self._key = key
        self._attr_unique_id = f"obis_{key}"
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self) -> str | None:
        """Return the value of the sensor from coordinator data."""
        return self.coordinator.data.get(self._key)

    async def async_update(self) -> None:
        """Request a refresh from the coordinator."""
        await self.coordinator.async_request_refresh()
