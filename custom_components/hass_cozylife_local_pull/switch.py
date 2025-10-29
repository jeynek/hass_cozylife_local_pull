from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN, SWITCH_TYPE_CODE, SWITCH
from .coordinator import CozyLifeCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    if coordinator.device_type_code == SWITCH_TYPE_CODE:
        async_add_entities([CozyLifeSwitch(coordinator)])

class CozyLifeSwitch(SwitchEntity):
    _attr_should_poll = False

    def __init__(self, coordinator: CozyLifeCoordinator) -> None:
        self._attr_unique_id = f"{coordinator.ip}_switch"
        self._attr_name = coordinator.device_model_name or "Switch"
        self._attr_device_info = coordinator.device_info
        self.coordinator = coordinator
        self._state = False

    @callback
    def _handle_coordinator_update(self) -> None:
        self._state = bool(self.coordinator.data.get(SWITCH, 0))
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(self.coordinator.async_add_listener(self._handle_coordinator_update))

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.client.async_control({SWITCH: 255})
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.client.async_control({SWITCH: 0})
        await self.coordinator.async_request_refresh()

    @property
    def is_on(self) -> bool:
        return self._state
