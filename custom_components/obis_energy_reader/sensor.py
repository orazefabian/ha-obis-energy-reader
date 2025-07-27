"""Sensor platform for OBIS Energy Reader."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity

from .const import OBIS_FIELDS, OBISSensorKey

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import OBISEnergyReaderConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: OBISEnergyReaderConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up OBIS sensors from static field list."""
    coordinator = entry.runtime_data.coordinator
    sensors = [
        OBISEnergyReaderStaticSensor(
            coordinator, field["key"], field["name"], field["unit"]
        )
        for field in OBIS_FIELDS
    ]
    async_add_entities(sensors, update_before_add=True)


class OBISEnergyReaderStaticSensor(SensorEntity):
    """Representation of an OBIS Energy Reader sensor."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        key: OBISSensorKey,
        name: str,
        unit: str | None,
    ) -> None:
        """Initialize the OBIS sensor."""
        self.coordinator = coordinator
        self._key = key
        self._attr_unique_id = f"obis_{key.value}"
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_device_info = {
            "identifiers": {("obis_energy_reader", coordinator.hass.data["obis_energy_reader_entry_id"])},
            "name": "OBIS Energy Reader",
            "manufacturer": "OBIS",
            "model": "OBIS JSON Endpoint",
        }

    @property
    def native_value(self) -> str | None:
        """Return the value of the sensor from coordinator data."""
        return self.coordinator.data.get(self._key.value)

    async def async_update(self) -> None:
        """Request a refresh from the coordinator."""
        await self.coordinator.async_request_refresh()
