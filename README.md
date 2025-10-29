# hass_cozylife_local_pull — CozyLife Local Control for Home Assistant (fork)

A fork of the original hass_cozylife_local_pull integration with fixes and added support for temperature and humidity sensors. This fork focuses on stability, modern Home Assistant APIs, and better local reliability.

NOTE: This is a custom integration for Home Assistant. It is installed into the `custom_components` folder and is not part of core Home Assistant.

Status (2025-10-29)
- Tested against local CozyLife bulbs and temperature/humidity-capable devices.
- Sensors (temperature, humidity, battery) implemented using known DPIDs.
- Works as a manual custom component; a future HACS release may be possible.

Features / Improvements in this fork
- Fixed protocol handling issues present in earlier versions.
- Added temperature and humidity sensors (DPIDs commonly used by CozyLife temperature sensors).
- Modernized async code and added config-entry support for platform setup.
- Device grouping via device_info so entities appear under a single device in Home Assistant.
- Dynamic sensor creation via dispatcher signal when tcp_client objects are created after startup.
- Basic safeguards and logging improvements.

Supported device types
- RGBCW Light
- CW Light
- Switch & Plug
- Temperature / Humidity sensors (devices exposing DPIDs for temp/humidity/battery)

Tested Hardware
- Affordable Wi‑Fi RGB bulbs and CozyLife temperature/humidity sensors (results may vary by model and firmware)

Installation

HACS
- Not currently published to HACS (this fork). If/when published, prefer HACS installation.

Manual (recommended for testing)
1. Copy the `hass_cozylife_local_pull` folder into your Home Assistant `custom_components/` directory:
   /config/custom_components/hass_cozylife_local_pull/

2. Restart Home Assistant.

Configuration

YAML (legacy)
Add basic configuration to `configuration.yaml` (only if the integration expects YAML — check integration manifest and __init__.py for config entry support):
```yaml
hass_cozylife_local_pull:
  lang: en
  ip:
    - "192.168.1.101"
    - "192.168.1.102"
```

Config entries
- This fork includes support for platform setup via `async_setup_entry`. If your integration exposes a config flow or programmatic config entry creation, prefer that over YAML.
- Entities (sensors, lights, etc.) will be created when tcp_client objects are registered in `hass.data[DOMAIN]["tcp_client"]`. If tcp_client objects are created after startup, the integration will dispatch a signal so platforms can add entities dynamically.

Dynamic client / sensor creation (for integrators)
- When the integration creates a new tcp_client at runtime, dispatch:
```py
from homeassistant.helpers.dispatcher import async_dispatcher_send
from custom_components.hass_cozylife_local_pull.sensor import SIGNAL_NEW_TCP_CLIENT

async_dispatcher_send(hass, SIGNAL_NEW_TCP_CLIENT, new_tcp_client)
```
That will instruct the sensor platform to create sensor entities for the new client.

Sensors and DPIDs (info)
- Temperature — DPID "8" — value reported as temperature * 10 (e.g., 235 -> 23.5 °C)
- Humidity — DPID "4" — value reported as percentage (0..100) or occasionally scaled by 10
- Battery — DPID "9" — reported as battery * 10 (e.g., 800 -> 80%)

Notes & recommendations
- The integration exposes synchronous tcp_client.query() calls wrapped in an executor. If your tcp_client provides async methods, converting to native async can reduce thread usage.
- Consider switching to a DataUpdateCoordinator if multiple entities poll the same device; this avoids parallel queries and centralizes error handling and throttling.
- Ensure your devices use static IPs or DHCP reservations for reliability, as described originally.

Troubleshooting
- Device unavailable: check Wi‑Fi connectivity and router client isolation settings.
- Entities not created: verify that `hass.data[DOMAIN]["tcp_client"]` contains clients before platform setup, or that the integration dispatches SIGNAL_NEW_TCP_CLIENT when clients are created later.
- Check Home Assistant logs (Supervisor / Core logs) for integration-specific errors.

Development notes for maintainers
- Keep manifest.json up-to-date with minimum Home Assistant version and requirements.
- Implement `async_unload_entry` in __init__.py to clean up dispatcher listeners stored in hass.data[DOMAIN].
- Provide tests for sensor value conversion, entity creation paths (hass.data vs dispatcher), and query error handling.

License & attribution
- This repository is a fork. Keep license and attribution consistent with the original project as appropriate.
- See the original README preserved below for historical context.

Original README (preserved)
<details>
  <summary>Show Original README</summary>
  (Original README preserved in this repository)
</details>
