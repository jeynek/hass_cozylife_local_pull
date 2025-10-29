# hass_cozylife_local_pull — CozyLife Local Control for Home Assistant (fork)

An AI Slop fork of the original hass_cozylife_local_pull integration with fixes and added support for temperature and humidity sensors. This fork focuses on stability, modern Home Assistant APIs, and better local reliability.

NOTE: This is a custom integration for Home Assistant. It is installed into the `custom_components` folder and is not part of core Home Assistant.

Status (2025-10-29)
- Tested against local CozyLife bulbs, switches/plugs, and temperature/humidity-capable devices.
- Sensors (temperature, humidity, battery) implemented using known DPIDs with automatic scaling.
- Full async implementation for better performance; supports HACS installation (once published).

Features / Improvements in this fork
- Fixed protocol handling issues present in earlier versions, including async TCP connections with on-demand reconnects.
- Added temperature, humidity, and battery sensors for devices exposing relevant DPIDs.
- Modernized to fully async code, including UDP auto-discovery and config flow for easy setup.
- Uses DataUpdateCoordinator for centralized polling, error handling, and throttling to avoid redundant queries.
- Device grouping via device_info so all entities (lights, switches, sensors) appear under a single device in Home Assistant.
- Dynamic entity creation based on device-reported DPIDs and type; supports RGBCW/CW lights with color, temp, and brightness control.
- Config entry support with auto-discovery (UDP broadcast) and manual IP addition via UI.
- Basic safeguards, improved logging, and proper unload cleanup.

Supported device types
- RGBCW Light (with HS color, color temperature, brightness)
- CW Light (color temperature, brightness)
- Switch & Plug
- Temperature / Humidity sensors (devices exposing DPIDs for temp/humidity/battery)

Tested Hardware
- Affordable Wi‑Fi RGB bulbs, switches/plugs, and CozyLife temperature/humidity sensors (results may vary by model and firmware)

Installation

HACS
- Not currently published to HACS (this fork). If/when published, search for "CozyLife Local Pull" in HACS and install.

Manual (recommended for testing)
1. Copy the `hass_cozylife_local_pull` folder into your Home Assistant `custom_components/` directory:  
   `/config/custom_components/hass_cozylife_local_pull/`

2. Restart Home Assistant.

Configuration

This integration uses config entries and does not support legacy YAML configuration. Devices are added via the Home Assistant UI:

- **Auto-discovery**: Devices should be automatically discovered via UDP broadcast (port 6095). Go to Settings > Devices & Services > Add Integration, and select "CozyLife Local Pull" if prompted, or wait for discovery notifications.
- **Manual addition**: If auto-discovery fails (e.g., due to network isolation), add manually: Go to Settings > Devices & Services > Add Integration > Search for "CozyLife Local Pull" > Enter the device's IP address and language (default: en).

Entities (sensors, lights, switches) are created dynamically based on the device's reported type and DPIDs after setup. No further configuration is needed.

Dynamic client / sensor creation (for integrators)
- Entities are added based on device info fetched during setup. For runtime additions (rare), the integration can dispatch a signal, but this is handled internally via the coordinator.

Sensors and DPIDs (info)
- Temperature — DPID "8" — value reported as temperature * 10 (e.g., 235 -> 23.5 °C)
- Humidity — DPID "4" — value reported as percentage (0..100); automatically handles occasional scaling by 10
- Battery — DPID "9" — reported as battery * 10 (e.g., 800 -> 80%)

Lights and DPIDs (info)
- Switch (on/off) — DPID "1"
- Work Mode (white/color) — DPID "2"
- Color Temperature — DPID "3" — value 0-1000 (scaled to Kelvin range 2000-6500)
- Brightness — DPID "4" — value 0-1000 (scaled to 0-255 in HA)
- Hue — DPID "5" — value 0-65535 (scaled to 0-360 in HA)
- Saturation — DPID "6" — value 0-65535 (scaled to 0-100 in HA)

Notes & recommendations
- The integration uses native async TCP methods for queries and controls, reducing thread usage.
- Polling is centralized via DataUpdateCoordinator (every 30 seconds by default; adjustable in code if needed).
- Ensure your devices use static IPs or DHCP reservations for reliability. Auto-discovery requires devices to respond to UDP broadcasts.
- For lights, optimistic updates are used for quick response, with polling to confirm state.

Troubleshooting
- Device unavailable: Check Wi‑Fi connectivity, router client isolation settings, and ensure device is powered on. Verify IP is correct and reachable.
- No auto-discovery: Ensure UDP port 6095 is open; try manual addition with IP. Check logs for discovery errors.
- Entities not created: Verify device reports supported DPIDs (check logs). Restart HA after installation.
- Check Home Assistant logs (Settings > System > Logs) for integration-specific errors (search for "hass_cozylife_local_pull").

Development notes for maintainers
- Keep manifest.json up-to-date with Home Assistant version requirements and dependencies (e.g., aiohttp).
- Tests recommended for sensor scaling, entity creation based on DPIDs, query error handling, and discovery.
- The integration supports async_unload_entry for cleanup.

License & attribution
- This repository is a fork. Keep license and attribution consistent with the original project as appropriate.
- See the original README preserved below for historical context.

Original README (preserved)
<details>
  <summary>Show Original README</summary>
  (Original README preserved in this repository)
</details>
