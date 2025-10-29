from homeassistant.components.light import ColorMode, LightEntity, LightEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import async_get_current_platform

from .const import DOMAIN, LIGHT_TYPE_CODE, SWITCH, WORK_MODE, COLOR_TEMP, BRIGHT, HUE, SAT
from .coordinator import CozyLifeCoordinator

HUE_SCALE = 65535 / 360
SAT_SCALE = 65535 / 1000  # To 0-1000, then /10 for HA 0-100
BRIGHT_SCALE = 1000 / 255
COLOR_TEMP_MIN = 2000
COLOR_TEMP_MAX = 6500

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    if coordinator.device_type_code != LIGHT_TYPE_CODE:
        return

    async_add_entities([CozyLifeLight(coordinator)])

class CozyLifeLight(LightEntity):
    _attr_supported_features = LightEntityFeature.TRANSITION | LightEntityFeature.EFFECT
    _attr_should_poll = False
    _attr_min_color_temp_kelvin = COLOR_TEMP_MIN
    _attr_max_color_temp_kelvin = COLOR_TEMP_MAX

    def __init__(self, coordinator: CozyLifeCoordinator) -> None:
        self._attr_unique_id = f"{coordinator.ip}_light"
        self._attr_name = coordinator.device_model_name or "Light"
        self._attr_device_info = coordinator.device_info
        self.coordinator = coordinator
        self._attr_supported_color_modes = set()
        dpid = set(coordinator.dpid)
        if HUE in dpid and SAT in dpid:
            self._attr_supported_color_modes.add(ColorMode.HS)
        if COLOR_TEMP in dpid:
            self._attr_supported_color_modes.add(ColorMode.COLOR_TEMP)
        if BRIGHT in dpid and not self._attr_supported_color_modes:
            self._attr_supported_color_modes.add(ColorMode.BRIGHTNESS)
        if not self._attr_supported_color_modes:
            self._attr_supported_color_modes.add(ColorMode.ONOFF)

        self._state = False
        self._brightness = 255
        self._hs_color = (0, 0)
        self._color_temp_kelvin = 3500
        self._color_mode = ColorMode.UNKNOWN

    @callback
    def _handle_coordinator_update(self) -> None:
        data = self.coordinator.data
        self._state = bool(data.get(SWITCH, 0))
        bright = data.get(BRIGHT, 1000)
        self._brightness = int(bright / BRIGHT_SCALE) if bright else None
        work_mode = data.get(WORK_MODE, 0)
        if work_mode == 1:  # Color mode
            self._color_mode = ColorMode.HS
            hue_raw = data.get(HUE, 0)
            sat_raw = data.get(SAT, 0)
            self._hs_color = (hue_raw / HUE_SCALE, (sat_raw / SAT_SCALE) / 10)  # sat 0-1000 to 0-100
            self._color_temp_kelvin = None
        else:  # White mode
            self._color_mode = ColorMode.COLOR_TEMP
            ct_raw = data.get(COLOR_TEMP, 500)
            ct_norm = ct_raw / 1000
            self._color_temp_kelvin = int(COLOR_TEMP_MIN + ct_norm * (COLOR_TEMP_MAX - COLOR_TEMP_MIN))
            self._hs_color = None
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(self.coordinator.async_add_listener(self._handle_coordinator_update))

    async def async_turn_on(self, **kwargs) -> None:
        commands = {SWITCH: 255}
        if 'brightness' in kwargs:
            commands[BRIGHT] = int(kwargs['brightness'] * BRIGHT_SCALE)
        if 'hs_color' in kwargs:
            hs = kwargs['hs_color']
            commands[WORK_MODE] = 1
            commands[HUE] = int(hs[0] * HUE_SCALE)
            commands[SAT] = int(hs[1] * 10 * (65535 / 1000))  # 0-100 to 0-1000 to 0-65535
        if 'color_temp_kelvin' in kwargs:
            commands[WORK_MODE] = 0
            ct_norm = (kwargs['color_temp_kelvin'] - COLOR_TEMP_MIN) / (COLOR_TEMP_MAX - COLOR_TEMP_MIN)
            commands[COLOR_TEMP] = int(ct_norm * 1000)
        await self.coordinator.client.async_control(commands)
        await self.coordinator.async_request_refresh()  # Poll to confirm, but optimistic possible

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.client.async_control({SWITCH: 0})
        await self.coordinator.async_request_refresh()

    @property
    def is_on(self) -> bool:
        return self._state

    @property
    def brightness(self) -> int | None:
        return self._brightness

    @property
    def hs_color(self) -> tuple | None:
        return self._hs_color

    @property
    def color_temp_kelvin(self) -> int | None:
        return self._color_temp_kelvin
