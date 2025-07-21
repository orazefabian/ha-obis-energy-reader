"""Binary sensor platform for obis_energy_reader."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .entity import OBISEnergyReaderEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import OBISEnergyReaderConfigEntry

OBIS_BINARY_SENSORS = [
    ("importing", "Importing Power", "mdi:transmission-tower"),
    ("exporting", "Exporting Power", "mdi:solar-power"),
]

ENTITY_DESCRIPTIONS = tuple(
    BinarySensorEntityDescription(
        key=field[0],
        name=f"OBIS {field[1]}",
        icon=field[2],
    )
    for field in OBIS_BINARY_SENSORS
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: OBISEnergyReaderConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        OBISEnergyReaderBinarySensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class OBISEnergyReaderBinarySensor(OBISEnergyReaderEntity, BinarySensorEntity):
    """obis_energy_reader binary_sensor class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary_sensor is on."""
        data = self.coordinator.data
        if self.entity_description.key == "importing":
            return float(data.get("1.7.0", 0)) > 0
        if self.entity_description.key == "exporting":
            return float(data.get("2.7.0", 0)) > 0
        return None
