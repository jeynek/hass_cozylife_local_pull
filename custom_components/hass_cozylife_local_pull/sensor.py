"""
CozyLife sensor platform
Creates temperature / humidity / battery sensors for devices that expose those DPIDs.

This implementation uses the DPIDs and scaling used by the homebridge-cozylife-temperature-sensor
project:
 - Temperature (DPID "8") — value is temperature * 10 (e.g. 235 -> 23.5°C)
 - Humidity  (DPID "4") — value is humidity in percent (0..100)
 - Battery   (DPID "9") — value is battery * 10 (e.g. 800 -> 80%)
"""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import TEMP_CELSIUS, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN, SENSOR_TYPE_CODE, SENSOR_DPID, TEMP, HUMIDITY, BATTERY
from .tcp_client import tcp_client

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the CozyLife sensor platform."""
    if discovery_info is None:
        return

    sensors = []
    if DOMAIN in hass.data and 'tcp_client' in hass.data[DOMAIN]:
        for client in hass.data[DOMAIN]['tcp_client']:
            dpids = client.dpid or []
            # Create sensors for devices that either identify as sensor type
            # or expose any of the known sensor DPIDs.
            if client.device_type_code == SENSOR_TYPE_CODE or any(d in dpids for d in SENSOR_DPID):
                for d in SENSOR_DPID:
                    try:
                        if d in dpids:
                            sensors.append(CozyLifeSensor(client, d))
                    except Exception:
                        _LOGGER.exception("Error while creating sensor entity")

    if sensors:
        async_add_entities(sensors, update_before_add=True)


class CozyLifeSensor(SensorEntity):
    """Generic CozyLife sensor for temperature/humidity/battery."""

    _attr_should_poll = True

    def __init__(self, tcp_client_instance: tcp_client, dpid: str) -> None:
        self._tcp_client = tcp_client_instance
        self._dpid = str(dpid)
        self._attr_unique_id = f"{self._tcp_client.device_id}_{self._dpid}"

        # per-dpid configuration
        if self._dpid == TEMP:
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_native_unit_of_measurement = TEMP_CELSIUS
            label = "temperature"
        elif self._dpid == HUMIDITY:
            self._attr_device_class = SensorDeviceClass.HUMIDITY
            self._attr_native_unit_of_measurement = PERCENTAGE
            label = "humidity"
        elif self._dpid == BATTERY:
            self._attr_device_class = SensorDeviceClass.BATTERY
            self._attr_native_unit_of_measurement = PERCENTAGE
            label = "battery"
        else:
            label = f"dpid_{self._dpid}"

        self._attr_name = f"{self._tcp_client.device_model_name} {self._tcp_client.device_id[-4:]} {label}"
        self._state = None

    @property
    def native_value(self) -> Any:
        return self._state

    @property
    def available(self) -> bool:
        # The tcp_client has reconnect logic; consider device available if client exists.
        return True

    async def async_update(self) -> None:
        """Fetch latest data from device (runs in executor to avoid blocking)."""
        try:
            data = await self.hass.async_add_executor_job(self._tcp_client.query)
            if not data or self._dpid not in data:
                self._state = None
                return

            raw = data.get(self._dpid)
            # raw is typically an int or string number. Convert to float safely.
            try:
                value = float(raw)
            except Exception:
                # non-numeric — expose raw
                self._state = raw
                return

            if self._dpid == TEMP:
                # Temperature is reported as integer = temperature * 10
                self._state = round(value / 10.0, 1)
            elif self._dpid == HUMIDITY:
                # Humidity reported as integer percent (0..100)
                # Some devices might send humidity * 10; if value > 100 assume scaled by 10.
                if value > 100 and value <= 1000:
                    self._state = round(value / 10.0, 1)
                else:
                    self._state = round(value, 1)
            elif self._dpid == BATTERY:
                # Battery is reported as integer = battery * 10
                self._state = round(value / 10.0, 1)
            else:
                self._state = value

        except Exception as exc:
            _LOGGER.exception("Error updating sensor %s for %s: %s", self._dpid, self._tcp_client.device_id, exc)
            self._state = None
