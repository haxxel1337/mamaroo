import asyncio
import json
import logging
from bleak import BleakClient
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

UUID = "622d0101-2416-0fa7-e132-2f1495cc2ce0"
MODES = ["", "Car Ride", "Kangaroo", "Tree Swing", "Rock-A-Bye", "Wave"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    async_add_entities([MamarooSensor(entry)])

class MamarooSensor(SensorEntity):
    def __init__(self, entry: ConfigEntry):
        self._entry = entry
        self._mac = entry.data["MAC"]
        self._mqtt_client = None
        self._status = None

    async def async_added_to_hass(self):
        await self.connect_mqtt()
        await self.connect_bluetooth()

    async def connect_mqtt(self):
        # Logic to connect to MQTT broker
        pass

    async def connect_bluetooth(self):
        self._client = BleakClient(self._mac)
        await self._client.connect()
        await self._client.start_notify(UUID, self.notification_handler)

    def notification_handler(self, sender, data):
        status = {"mode": data[1], "speed": data[2], "power": data[5]}
        if status != self._status:
            self._status = status
            self.async_write_ha_state()

    @property
    def state(self):
        return self._status

    @property
    def extra_state_attributes(self):
        return self._status if self._status else {}

    async def async_will_remove_from_hass(self):
        await self._client.disconnect()
