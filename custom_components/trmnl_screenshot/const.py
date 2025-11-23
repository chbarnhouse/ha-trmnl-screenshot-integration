"""Constants for TRMNL Screenshot integration."""
from typing import Final

DOMAIN: Final = "trmnl_screenshot"
VERSION: Final = "1.0.0"

# Service names
SERVICE_CAPTURE_AND_SEND: Final = "capture_and_send"
SERVICE_SEND_SCREENSHOT: Final = "send_screenshot"

# Default values
DEFAULT_ADDON_HOST: Final = "http://127.0.0.1:5001"
DEFAULT_AUTO_CAPTURE_INTERVAL: Final = 0  # 0 = disabled
