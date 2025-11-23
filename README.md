# TRMNL Screenshot Integration

Home Assistant integration that bridges the TRMNL Screenshot Addon and TRMNL Receiving Integration, enabling automated workflows for capturing and displaying Home Assistant dashboards on TRMNL e-ink devices.

## Features

- **Automated Capture & Send**: Capture dashboards and send to TRMNL devices in one service call
- **Profile Management**: Create multiple capture profiles for different dashboards
- **Direct Integration**: Works seamlessly with TRMNL devices via the TRMNL E-Ink Display integration
- **Flexible Automation**: Easily create automations to update displays on schedules or events
- **Change Detection**: Optional hash checking to avoid unnecessary updates

## Installation

### Via HACS (Recommended)

1. Open Home Assistant and go to **Settings → Devices & Services → Integrations**
2. Click **+ Create Integration**
3. Search for "TRMNL Screenshot"
4. Follow the configuration wizard

### Manual Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ha-trmnl-screenshot-integration.git \
     /home/homeassistant/.homeassistant/custom_components/trmnl_screenshot
   ```

2. Restart Home Assistant

3. Add the integration via **Settings → Devices & Services → Integrations**

## Configuration

When you add the integration, you'll be asked for:

- **TRMNL Device ID**: The MAC address of your TRMNL device (e.g., `XX:XX:XX:XX:XX:XX`)
- **Addon Host**: URL where the TRMNL Screenshot Addon is running (e.g., `http://localhost:5001`)

### Example Configuration

If your addon is running on the same machine as Home Assistant:
```
Addon Host: http://localhost:5001
```

If your addon is running on a different machine:
```
Addon Host: http://192.168.1.100:5001
```

## Services

### `trmnl_screenshot.capture_and_send`

Capture a profile screenshot and send it to your TRMNL device.

```yaml
service: trmnl_screenshot.capture_and_send
data:
  device_id: "XX:XX:XX:XX:XX:XX"
  profile_id: "main-dashboard"
```

**Parameters:**
- `device_id` (required): MAC address of your TRMNL device
- `profile_id` (required): ID of the profile to capture (must exist in the addon)

### `trmnl_screenshot.send_screenshot`

Send an existing screenshot to your TRMNL device.

```yaml
service: trmnl_screenshot.send_screenshot
data:
  device_id: "XX:XX:XX:XX:XX:XX"
  screenshot_path: "screenshot-2025-11-23T23-11-14-224Z-0fdd4984.png"
```

**Parameters:**
- `device_id` (required): MAC address of your TRMNL device
- `screenshot_path` (required): Filename of screenshot from the addon

## Usage Examples

### Simple: Update Display Every 30 Minutes

```yaml
automation:
  - alias: "Update TRMNL Dashboard"
    trigger:
      platform: time_pattern
      minutes: "/30"
    action:
      service: trmnl_screenshot.capture_and_send
      data:
        device_id: "XX:XX:XX:XX:XX:XX"
        profile_id: "main-dashboard"
```

### Intermediate: Update on Specific Events

```yaml
automation:
  - alias: "Update TRMNL on Weather Change"
    trigger:
      platform: state
      entity_id: weather.home
    action:
      service: trmnl_screenshot.capture_and_send
      data:
        device_id: "XX:XX:XX:XX:XX:XX"
        profile_id: "weather-dashboard"
```

### Advanced: Multiple Profiles with Conditions

```yaml
automation:
  - alias: "TRMNL Day/Night Dashboard"
    trigger:
      platform: time_pattern
      minutes: "/30"
    action:
      - service: trmnl_screenshot.capture_and_send
        data:
          device_id: "XX:XX:XX:XX:XX:XX"
          profile_id: "{% if is_state('sun.sun', 'above_horizon') %}day-dashboard{% else %}night-dashboard{% endif %}"
```

### Advanced: Error Handling with Notifications

```yaml
automation:
  - alias: "TRMNL Update with Fallback"
    trigger:
      platform: time_pattern
      minutes: "/30"
    action:
      - service: trmnl_screenshot.capture_and_send
        data:
          device_id: "XX:XX:XX:XX:XX:XX"
          profile_id: "main-dashboard"
      - service: notify.mobile_app
        data:
          message: "TRMNL display updated successfully"
        continue_on_error: true
```

## Architecture

```
Home Assistant
    │
    ├─ TRMNL Screenshot Integration (this)
    │  │
    │  ├─ Calls: TRMNL E-Ink Display Integration
    │  │  └─ Service: trmnl.send_image
    │  │
    │  └─ Calls: TRMNL Screenshot Addon
    │     ├─ POST /api/profiles/{id}/capture
    │     └─ GET /api/screenshot/{filename}
    │
    ├─ TRMNL E-Ink Display Integration
    │  └─ Sends images to TRMNL Cloud/BYOS API
    │
    └─ TRMNL Screenshot Addon
       └─ Captures dashboards via Playwright
```

## Requirements

### Required
- Home Assistant 2024.1.0 or later
- [TRMNL E-Ink Display Integration](https://github.com/yourusername/ha-trmnl-integration)
- [TRMNL Screenshot Addon](https://github.com/yourusername/ha-trmnl-screenshot-addon)
- TRMNL device (Standard or BYOS)

### Optional
- Pillow (for image processing)
- Requests library (for HTTP calls)

## Troubleshooting

### "Cannot connect to addon"
- Verify addon is running: visit `http://addon-host:5001/health` in browser
- Check network connectivity between Home Assistant and addon
- Ensure addon host configuration is correct (IP address or hostname)

### "Profile not found"
- Create the profile in the addon's web UI
- Profile ID must be exactly as created (case-sensitive)
- Reload integration after creating new profiles

### "Failed to send image"
- Verify TRMNL E-Ink Display integration is installed and configured
- Check TRMNL device is online
- Review Home Assistant logs for detailed errors

### Screenshots not showing on device
- Verify image dimensions match device (typically 800x480)
- Check device is connected to internet
- Try testing with a simple image first: `https://via.placeholder.com/800x480`

## API Reference

### Service Call Format

```yaml
service: trmnl_screenshot.capture_and_send
target: {}
data:
  device_id: "XX:XX:XX:XX:XX:XX"
  profile_id: "profile-name"
```

### Response Data

The service returns no data, but success/failure can be checked via:
- Home Assistant logs for error messages
- Integration state/attributes (if available)

## Performance Notes

- **Capture Time**: 1-5 seconds per screenshot
- **Network Latency**: Depends on addon location
- **Rate Limiting**: Subject to TRMNL API rate limits (12-30 requests/hour)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Ask questions on GitHub Discussions
- **TRMNL Support**: Visit [usetrmnl.com](https://usetrmnl.com)

## Related Projects

- [TRMNL E-Ink Display Integration](https://github.com/yourusername/ha-trmnl-integration) - Core TRMNL device integration
- [TRMNL Screenshot Addon](https://github.com/yourusername/ha-trmnl-screenshot-addon) - Screenshot capture addon

## Disclaimer

This integration is not officially affiliated with TRMNL. Use at your own risk.
