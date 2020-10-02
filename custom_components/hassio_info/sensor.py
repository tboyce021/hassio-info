"""
Support for Hassio sensors.
"""
import asyncio
import logging

from homeassistant.components.hassio import DOMAIN as HASSIO_DOMAIN
from homeassistant.components.hassio.const import (
    ATTR_ADDONS,
    ATTR_NAME,
)
from homeassistant.helpers.entity import Entity
from homeassistant.const import ATTR_STATE, STATE_UNAVAILABLE, STATE_UNKNOWN

from .const import (
    ATTR_SLUG,
    ICON,
    SENSOR_NAMES,
    SENSOR_TYPES,
    STATE_NONE
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the platform."""
    hassio = hass.data[HASSIO_DOMAIN]

    info = await hassio.get_supervisor_info()
    addons = info[ATTR_ADDONS]

    for addon in addons:
        for sensor_type in SENSOR_TYPES:
            async_add_entities([AddonSensor(hassio, addon, sensor_type)], True)

class AddonSensor(Entity):
    """Representation of an Addon sensor."""

    def __init__(self, hassio, addon, sensor_type):
        """Initialize the Addon sensor."""
        self._hassio = hassio
        self._addon_slug = addon[ATTR_SLUG]
        self._name = '{}: {}'.format(addon[ATTR_NAME], SENSOR_NAMES[sensor_type])
        self._sensor_type = sensor_type
        self._state = None

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return ICON

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique ID for the device."""
        return '{}-{}'.format(self._addon_slug, self._sensor_type)

    async def async_update(self):
        """Update the state."""
        if not self._hassio.is_connected():
            self._state = STATE_UNKNOWN
            return

        info = await self._hassio.get_addon_info(self._addon_slug)
        if info[self._sensor_type] is None or info[self._sensor_type] == STATE_NONE:
            self._state = STATE_UNAVAILABLE
        else:
            self._state = info[self._sensor_type]
