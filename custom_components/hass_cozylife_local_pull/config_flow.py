import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_LANG, LANG
from .tcp_client import TCPClient
from .utils import async_get_pid_list

class CozyLifeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is not None:
            ip = user_input[CONF_IP_ADDRESS]
            lang = user_input.get(CONF_LANG, LANG)

            await self.async_set_unique_id(ip)
            self._abort_if_unique_id_configured()

            client = TCPClient(ip)
            try:
                await client.async_fetch_device_info(lang)
            except Exception as e:
                _LOGGER.error(f"Failed to connect to {ip}: {e}")
                return self.async_abort(reason="cannot_connect")

            return self.async_create_entry(title=client.device_model_name or f"CozyLife ({ip})", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_IP_ADDRESS): str,
                vol.Optional(CONF_LANG, default=LANG): str,
            }),
        )

    async def async_step_discovery(self, discovery_info) -> FlowResult:
        ip = discovery_info[CONF_IP_ADDRESS]
        lang = discovery_info.get(CONF_LANG, LANG)

        await self.async_set_unique_id(ip)
        self._abort_if_unique_id_configured()

        client = TCPClient(ip)
        try:
            await client.async_fetch_device_info(lang)
        except Exception:
            return self.async_abort(reason="cannot_connect")

        return self.async_create_entry(title=client.device_model_name or f"CozyLife ({ip})", data=discovery_info)
