"""Config flow for TRMNL Screenshot integration."""
import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class TRMNLScreenshotConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for TRMNL Screenshot."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle user step."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(
                f"trmnl-screenshot-{user_input['trmnl_device_id']}"
            )
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"TRMNL Screenshot {user_input['trmnl_device_id']}",
                data={
                    "addon_host": user_input.get(
                        "addon_host", "http://127.0.0.1:5001"
                    ),
                    "trmnl_device_id": user_input["trmnl_device_id"],
                },
            )

        data_schema = vol.Schema(
            {
                vol.Required("trmnl_device_id"): str,
                vol.Optional(
                    "addon_host", default="http://127.0.0.1:5001"
                ): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        """Get options flow."""
        return TRMNLScreenshotOptionsFlow(config_entry)


class TRMNLScreenshotOptionsFlow(config_entries.OptionsFlow):
    """Handle options for TRMNL Screenshot."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle options flow."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "auto_capture_interval",
                        default=self.config_entry.options.get(
                            "auto_capture_interval", 0
                        ),
                    ): int,
                    vol.Optional(
                        "hash_check_enabled",
                        default=self.config_entry.options.get(
                            "hash_check_enabled", True
                        ),
                    ): bool,
                }
            ),
        )
