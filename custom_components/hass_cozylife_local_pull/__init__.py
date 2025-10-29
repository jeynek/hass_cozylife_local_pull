import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import discovery_flow

from .const import DOMAIN, CONF_IP_ADDRESS, CONF_LANG
from .coordinator import CozyLifeCoordinator
from .discovery import async_discover_ips

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.LIGHT, Platform.SWITCH, Platform.SENSOR]

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    hass.data.setdefault(DOMAIN, {})

    async def _discover():
        ips = await async_discover_ips()
        for ip in ips:
            discovery_flow.async_create_flow(
                hass, DOMAIN,
                context={"source": config_entries.SOURCE_DISCOVERY},
                data={CONF_IP_ADDRESS: ip, CONF_LANG: "en"},
            )

    hass.async_create_task(_discover())
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ip = entry.data[CONF_IP_ADDRESS]
    lang = entry.data.get(CONF_LANG, "en")

    coordinator = CozyLifeCoordinator(hass, ip, lang)
    hass.data[DOMAIN][entry.entry_id] = coordinator

    try:
        await coordinator.async_fetch_device_info()
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        raise ConfigEntryNotReady(f"Setup error for {ip}: {err}")

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        coordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_close()
        return True
    return False
