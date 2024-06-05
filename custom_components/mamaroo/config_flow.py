import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

class MamarooConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return MamarooOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="MamaRoo", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("broker"): str,
                vol.Required("username"): str,
                vol.Required("password"): str,
                vol.Required("prefix"): str,
                vol.Required("MAC"): str,
            })
        )

class MamarooOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("broker", default=self.config_entry.data.get("broker")): str,
                vol.Required("username", default=self.config_entry.data.get("username")): str,
                vol.Required("password", default=self.config_entry.data.get("password")): str,
                vol.Required("prefix", default=self.config_entry.data.get("prefix")): str,
                vol.Required("MAC", default=self.config_entry.data.get("MAC")): str,
            })
        )
