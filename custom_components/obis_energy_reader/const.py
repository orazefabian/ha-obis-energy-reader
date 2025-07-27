"""Constants for integration_blueprint."""

from enum import Enum
from logging import Logger, getLogger
from typing import TypedDict

LOGGER: Logger = getLogger(__package__)

DOMAIN = "obis_energy_reader"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"


class OBISSensorKey(Enum):
    """OBIS Sensor Keys."""

    TOTAL_ACTIVE_ENERGY_CONSUMED_IMPORT = "1.8.0"
    TOTAL_ACTIVE_ENERGY_EXPORTED_EXPORT = "2.8.0"
    TOTAL_POSITIVE_REACTIVE_ENERGY_IMPORTED = "3.8.0"
    TOTAL_NEGATIVE_REACTIVE_ENERGY_EXPORTED = "4.8.0"
    INSTANTANEOUS_ACTIVE_POWER_IMPORT = "1.7.0"
    INSTANTANEOUS_ACTIVE_POWER_EXPORT = "2.7.0"
    INSTANTANEOUS_TOTAL_ACTIVE_POWER = "16.7.0"
    TIMESTAMP = "timestamp"
    UPTIME = "uptime"
    UTC = "UTC"


class OBISBinarySensorKey(Enum):
    """OBIS Binary Sensor Keys."""

    IMPORTING = "importing"
    EXPORTING = "exporting"


class OBISField(TypedDict):
    """OBIS Field definition."""

    key: OBISSensorKey
    name: str
    unit: str | None


OBIS_FIELDS: list[OBISField] = [
    {
        "key": OBISSensorKey.TOTAL_ACTIVE_ENERGY_CONSUMED_IMPORT,
        "name": "Total active energy consumed (import)",
        "unit": "kWh",
    },
    {
        "key": OBISSensorKey.TOTAL_ACTIVE_ENERGY_EXPORTED_EXPORT,
        "name": "Total active energy exported (export)",
        "unit": "kWh",
    },
    {
        "key": OBISSensorKey.TOTAL_POSITIVE_REACTIVE_ENERGY_IMPORTED,
        "name": "Total positive reactive energy imported",
        "unit": "kvarh",
    },
    {
        "key": OBISSensorKey.TOTAL_NEGATIVE_REACTIVE_ENERGY_EXPORTED,
        "name": "Total negative reactive energy exported",
        "unit": "kvarh",
    },
    {
        "key": OBISSensorKey.INSTANTANEOUS_ACTIVE_POWER_IMPORT,
        "name": "Instantaneous active power (import)",
        "unit": "W",
    },
    {
        "key": OBISSensorKey.INSTANTANEOUS_ACTIVE_POWER_EXPORT,
        "name": "Instantaneous active power (export)",
        "unit": "W",
    },
    {
        "key": OBISSensorKey.INSTANTANEOUS_TOTAL_ACTIVE_POWER,
        "name": "Instantaneous total active power",
        "unit": "W",
    },
    {"key": OBISSensorKey.TIMESTAMP, "name": "Timestamp of the reading", "unit": None},
    {"key": OBISSensorKey.UPTIME, "name": "Uptime of the device", "unit": None},
    {"key": OBISSensorKey.UTC, "name": "Timestamp in UTC", "unit": None},
]


class OBISBinarySensor(TypedDict):
    """OBIS Binary Sensor definition."""

    key: OBISBinarySensorKey
    name: str
    icon: str


OBIS_BINARY_SENSORS: list[OBISBinarySensor] = [
    {
        "key": OBISBinarySensorKey.IMPORTING,
        "name": "Importing Power",
        "icon": "mdi:transmission-tower",
    },
    {
        "key": OBISBinarySensorKey.EXPORTING,
        "name": "Exporting Power",
        "icon": "mdi:solar-power",
    },
]
