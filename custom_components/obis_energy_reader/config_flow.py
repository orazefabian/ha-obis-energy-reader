"""Config flow for OBIS Energy Reader integration."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    OBISEnergyReaderApiClient,
    OBISEnergyReaderApiClientAuthenticationError,
    OBISEnergyReaderApiClientCommunicationError,
    OBISEnergyReaderApiClientError,
)
from .const import DOMAIN

CONF_OBIS_URL = "obis_url"


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for OBIS Energy Reader."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle the initial step of the config flow."""
        errors = {}
        if user_input is not None:
            try:
                await self._test_obis_url(
                    obis_url=user_input[CONF_OBIS_URL],
                )
            except OBISEnergyReaderApiClientAuthenticationError:
                errors["base"] = "auth"
            except OBISEnergyReaderApiClientCommunicationError:
                errors["base"] = "connection"
            except OBISEnergyReaderApiClientError:
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(user_input[CONF_OBIS_URL])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_OBIS_URL],
                    data=user_input,
                )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_OBIS_URL): selector.TextSelector(
                        selector.TextSelectorConfig(type=selector.TextSelectorType.URL),
                    ),
                }
            ),
            errors=errors,
        )

    async def _test_obis_url(
        self,
        obis_url: str,
    ) -> None:
        """Test OBIS endpoint connectivity."""
        client = OBISEnergyReaderApiClient(
            obis_url=obis_url,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()
