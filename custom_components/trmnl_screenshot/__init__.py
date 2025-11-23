"""TRMNL Screenshot Integration."""
import logging
from typing import Final

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

_LOGGER: logging.Logger = logging.getLogger(__name__)

DOMAIN: Final = "trmnl_screenshot"
PLATFORMS: list[Platform] = []

# Integration version
VERSION: Final = "1.0.0"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up TRMNL Screenshot from a config entry."""
    _LOGGER.debug(f"Setting up TRMNL Screenshot for {entry.title}")

    # Store config entry data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "addon_host": entry.data.get("addon_host", "http://127.0.0.1:5001"),
        "trmnl_device_id": entry.data.get("trmnl_device_id"),
        "auto_capture_interval": entry.options.get("auto_capture_interval", 0),
    }

    # Setup services
    from .services import async_setup_services
    await async_setup_services(hass, entry)

    # Forward setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug(f"Unloading TRMNL Screenshot for {entry.title}")

    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
