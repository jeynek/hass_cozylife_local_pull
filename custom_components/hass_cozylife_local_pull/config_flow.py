"""Config flow for CozyLife Local Pull integration."""
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.const import CONF_IP_ADDRESS

from .const import DOMAIN, CONF_LANG

class CozyLifeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for CozyLife Local Pull."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            # Validate IP (add more validation if needed, e.g., ping or test connection)
            return self.async_create_entry(title=f"CozyLife ({user_input[CONF_IP_ADDRESS]})", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_IP_ADDRESS): str,
                    vol.Optional(CONF_LANG, default="en"): str,
                }
            ),
        )
