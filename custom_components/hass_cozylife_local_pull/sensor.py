from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN, SENSOR_TYPE_CODE, SENSOR_DPID, SENSOR_TEMP, HUMIDITY, BATTERY
from .coordinator import CozyLifeCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    dpid_set = set(coordinator.dpid)
    if coordinator.device_type_code == SENSOR_TYPE_CODE or dpid_set.intersection(SENSOR_DPID):
        entities = []
        if SENSOR_TEMP in dpid_set:
            entities.append(CozyLifeSensor(coordinator, SENSOR_TEMP, "Temperature", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS, 10))
        if HUMIDITY in dpid_set:
            entities.append(CozyLifeSensor(coordinator, HUMIDITY, "Humidity", SensorDeviceClass.HUMIDITY, PERCENTAGE, 1))  # Adjust factor if scaled
        if BATTERY in dpid_set:
            entities.append(CozyLifeSensor(coordinator, BATTERY, "Battery", SensorDeviceClass.BATTERY, PERCENTAGE, 10))
        async_add_entities(entities)

class CozyLifeSensor(SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_should_poll = False

    def __init__(self, coordinator: CozyLifeCoordinator, dpid: str, name: str, device_class, unit, factor: int) -> None:
        self._attr_unique_id = f"{coordinator.ip}_{dpid}"
        self._attr_name = f"{coordinator.device_model_name} {name}"
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit
        self._attr_device_info = coordinator.device_info
        self.coordinator = coordinator
        self.dpid = dpid
        self.factor = factor

    @callback
    def _handle_coordinator_update(self) -> None:
        value = self.coordinator.data.get(self.dpid)
        if value is not None:
            val_float = float(value)
            if self.dpid == HUMIDITY and val_float > 100 and val_float <= 1000:
                self._attr_native_value = round(val_float / 10, 1)
            else:
                self._attr_native_value = round(val_float / self.factor, 1)
        else:
            self._attr_native_value = None
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(self.coordinator.async_add_listener(self._handle_coordinator_update))
