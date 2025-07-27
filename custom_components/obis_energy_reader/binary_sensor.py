"""Binary sensor platform for OBIS Energy Reader."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
)

from .const import OBIS_BINARY_SENSORS, OBISBinarySensorKey, OBISSensorKey

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
    """Set up the binary sensor platform."""
    coordinator = entry.runtime_data.coordinator
    entities = [
        OBISEnergyReaderBinarySensor(
            coordinator, sensor["key"], sensor["name"], sensor["icon"]
        )
        for sensor in OBIS_BINARY_SENSORS
    ]
    async_add_entities(entities)


class OBISEnergyReaderBinarySensor(BinarySensorEntity):
    """OBIS Energy Reader binary_sensor class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        key: OBISBinarySensorKey,
        name: str,
        icon: str,
    ) -> None:
        """Initialize the binary sensor class."""
        self.coordinator = coordinator
        self._key = key
        self._attr_unique_id = f"obis_binary_{key.value}"
        self._attr_name = name
        self._attr_icon = icon
        self._attr_device_info = {
            "identifiers": {("obis_energy_reader", coordinator.hass.data["obis_energy_reader_entry_id"])},
            "name": "OBIS Energy Reader",
            "manufacturer": "OBIS",
            "model": "OBIS JSON Endpoint",
        }

    @property
    def is_on(self) -> bool | None:
        """Return the state of the binary sensor."""
        data = self.coordinator.data
        if self._key == OBISBinarySensorKey.IMPORTING:
            return (
                float(data.get(OBISSensorKey.INSTANTANEOUS_ACTIVE_POWER_IMPORT, 0)) > 0
            )
        if self._key == OBISBinarySensorKey.EXPORTING:
            return (
                float(data.get(OBISSensorKey.INSTANTANEOUS_ACTIVE_POWER_EXPORT, 0)) > 0
            )
        return None
