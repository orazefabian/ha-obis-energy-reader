"""Switch platform for OBIS Energy Reader (dummy example)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from .entity import OBISEnergyReaderEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import OBISEnergyReaderConfigEntry

OBIS_SWITCHES = [
    ("reset_uptime", "Reset Uptime", "mdi:restart"),
]

ENTITY_DESCRIPTIONS = tuple(
    SwitchEntityDescription(
        key=field[0],
        name=f"OBIS {field[1]}",
        icon=field[2],
    )
    for field in OBIS_SWITCHES
)

async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: OBISEnergyReaderConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    async_add_entities(
        OBISEnergyReaderSwitch(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class OBISEnergyReaderSwitch(OBISEnergyReaderEntity, SwitchEntity):
    """OBIS Energy Reader switch class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: SwitchEntityDescription,
    ) -> None:
        """Initialize the switch class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._is_on = False

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the switch."""
        # Dummy: In real use, would send a command to reset uptime
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch."""
        self._is_on = False
        self.async_write_ha_state()
