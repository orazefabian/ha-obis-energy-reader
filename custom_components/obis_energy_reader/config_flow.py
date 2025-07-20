"""Adds config flow for OBIS Energy Reader."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from slugify import slugify

from .api import (
    OBISEnergyReaderApiClient,
    OBISEnergyReaderApiClientAuthenticationError,
    OBISEnergyReaderApiClientCommunicationError,
    OBISEnergyReaderApiClientError,
)
from .const import DOMAIN, LOGGER

CONF_OBIS_URL = "obis_url"

class OBISFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for OBIS Energy Reader."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    username=user_input[CONF_USERNAME],
                    password=user_input[CONF_PASSWORD],
                    obis_url=user_input[CONF_OBIS_URL],
                )
            except OBISEnergyReaderApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except OBISEnergyReaderApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except OBISEnergyReaderApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(
                    unique_id=slugify(user_input[CONF_USERNAME])
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_USERNAME,
                        default=(user_input or {}).get(CONF_USERNAME, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                    vol.Required(CONF_PASSWORD): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD,
                        ),
                    ),
                    vol.Required(
                        CONF_OBIS_URL,
                        default=(user_input or {}).get(CONF_OBIS_URL, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.URL,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_credentials(self, username: str, password: str, obis_url: str) -> None:
        """Validate credentials and OBIS endpoint."""
        client = OBISEnergyReaderApiClient(
            username=username,
            password=password,
            obis_url=obis_url,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()
