"""Sensor platform for OBIS Energy Reader."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import OBISEnergyReaderEntity

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

ENTITY_DESCRIPTIONS = tuple(
    SensorEntityDescription(
        key=field[0],
        name=f"OBIS {field[0]}: {field[1]}",
        icon="mdi:flash" if field[2] in ("kWh", "W", "kvarh") else "mdi:clock-outline",
        native_unit_of_measurement=field[2],
    )
    for field in OBIS_FIELDS
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: OBISEnergyReaderConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        OBISEnergyReaderSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class OBISEnergyReaderSensor(OBISEnergyReaderEntity, SensorEntity):
    """OBIS Energy Reader Sensor class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data.get(self.entity_description.key)
