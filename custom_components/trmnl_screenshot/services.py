"""Services for TRMNL Screenshot integration."""
import hashlib
import logging
from typing import Any, Dict

import aiohttp
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, SERVICE_CAPTURE_AND_SEND, SERVICE_SEND_SCREENSHOT

_LOGGER = logging.getLogger(__name__)

# Service schemas
CAPTURE_AND_SEND_SCHEMA = vol.Schema(
    {
        vol.Required("device_id"): str,
        vol.Required("profile_id"): str,
    }
)

SEND_SCREENSHOT_SCHEMA = vol.Schema(
    {
        vol.Required("device_id"): str,
        vol.Required("screenshot_path"): str,
    }
)


async def async_setup_services(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Set up services for TRMNL Screenshot."""

    async def handle_capture_and_send(call: ServiceCall) -> None:
        """Capture screenshot from addon and send to TRMNL device."""
        device_id = call.data["device_id"]
        profile_id = call.data["profile_id"]

        config = hass.data[DOMAIN][entry.entry_id]
        addon_host = config["addon_host"]
        trmnl_device_id = config["trmnl_device_id"]

        try:
            # Trigger capture from addon
            async with aiohttp.ClientSession() as session:
                # Capture profile
                capture_url = f"{addon_host}/api/profiles/{profile_id}/capture"
                async with session.post(capture_url, timeout=aiohttp.ClientTimeout(total=60)) as resp:
                    if resp.status != 200:
                        raise HomeAssistantError(
                            f"Failed to capture screenshot: HTTP {resp.status}"
                        )
                    result = await resp.json()
                    filename = result.get("filename")

                if not filename:
                    raise HomeAssistantError("No filename returned from capture")

                # Get screenshot
                screenshot_url = f"{addon_host}/api/screenshot/{filename}"
                async with session.get(screenshot_url) as resp:
                    if resp.status != 200:
                        raise HomeAssistantError("Failed to download screenshot")
                    screenshot_data = await resp.read()

                # Send to TRMNL device using trmnl service
                image_url = f"{addon_host}/api/screenshot/{filename}"
                await hass.services.async_call(
                    "trmnl",
                    "send_image",
                    {
                        "device_id": trmnl_device_id,
                        "image_url": image_url,
                    },
                )

                _LOGGER.debug(
                    f"Screenshot captured and sent to TRMNL device {device_id}"
                )

        except aiohttp.ClientError as err:
            raise HomeAssistantError(f"Communication error with addon: {err}")
        except Exception as err:
            raise HomeAssistantError(f"Failed to capture and send: {err}")

    async def handle_send_screenshot(call: ServiceCall) -> None:
        """Send screenshot file to TRMNL device."""
        device_id = call.data["device_id"]
        screenshot_path = call.data["screenshot_path"]

        config = hass.data[DOMAIN][entry.entry_id]
        trmnl_device_id = config["trmnl_device_id"]
        addon_host = config["addon_host"]

        try:
            # Serve screenshot from addon or local path
            image_url = f"{addon_host}/api/screenshot/{screenshot_path.split('/')[-1]}"

            # Send to TRMNL device
            await hass.services.async_call(
                "trmnl",
                "send_image",
                {
                    "device_id": trmnl_device_id,
                    "image_url": image_url,
                },
            )

            _LOGGER.debug(f"Screenshot sent to TRMNL device {device_id}")

        except Exception as err:
            raise HomeAssistantError(f"Failed to send screenshot: {err}")

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_CAPTURE_AND_SEND,
        handle_capture_and_send,
        schema=CAPTURE_AND_SEND_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_SEND_SCREENSHOT,
        handle_send_screenshot,
        schema=SEND_SCREENSHOT_SCHEMA,
    )

    _LOGGER.debug("TRMNL Screenshot services registered")
