from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SWITCH_TYPE_CODE, LIGHT_TYPE_CODE, SENSOR_TYPE_CODE
from .tcp_client import TCPClient
from .utils import async_get_pid_list

_LOGGER = logging.getLogger(__name__)

class CozyLifeCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, ip: str, lang: str) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{ip}",
            update_interval=timedelta(seconds=30),
        )
        self.ip = ip
        self.lang = lang
        self.client = TCPClient(self.ip)
        self.device_type_code = None
        self.device_model_name = None
        self.dpid = []
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, ip)},
            name=f"CozyLife ({ip})",
            manufacturer="CozyLife",
            model="Unknown",
        )

    async def async_fetch_device_info(self) -> None:
        info = await self.client.async_send_receive(0, {})
        self.client.device_id = info.get('did')
        self.client.pid = info.get('pid')
        pid_list = await async_get_pid_list(self.lang)
        for category in pid_list:
            for model in category.get('m', []):
                if model['pid'] == self.client.pid:
                    self.device_model_name = model['n']
                    self.dpid = [str(d) for d in model.get('dpid', [])]
                    self.device_type_code = category['c']
                    self.device_info["model"] = self.device_model_name
                    self.device_info["name"] = f"{self.device_model_name} ({self.ip})"
                    break

    async def _async_update_data(self) -> dict:
        try:
            return await self.client.async_query()
        except Exception as err:
            raise UpdateFailed(f"Update failed for {self.ip}: {err}")

    async def async_close(self) -> None:
        await self.client.async_close()
