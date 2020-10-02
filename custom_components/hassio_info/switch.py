"""
Support for Hassio switches.
"""
from datetime import timedelta
import logging

from homeassistant.components.hassio import DOMAIN as HASSIO_DOMAIN
from homeassistant.components.hassio.const import (
    ATTR_ADDONS,
    ATTR_NAME,
)
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import ATTR_STATE, STATE_UNAVAILABLE, STATE_UNKNOWN

from .const import (
    ATTR_SLUG,
    ICON,
    STATE_NONE,
    STATE_STARTED
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=10)
PARALLEL_UPDATES = 1


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Hassio Info switch based on a config entry."""
    hassio = hass.data[HASSIO_DOMAIN]

    info = await hassio.get_supervisor_info()
    addons = info[ATTR_ADDONS]

    switches = []
    for addon in addons:
        switches.append(AddonSwitch(hassio, addon))

    async_add_entities(switches, True)


class AddonSwitch(SwitchEntity):
    """Representation of an Addon switch."""

    def __init__(self, hassio, addon):
        self._hassio = hassio
        self._addon_slug = addon[ATTR_SLUG]
        self._name = addon[ATTR_NAME]
        self._state = STATE_UNKNOWN

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return ICON

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def is_on(self):
        """Return the boolean response if switch is on."""
        return bool(self._state == STATE_STARTED)

    @property
    def unique_id(self):
        """Return a unique ID for the device."""
        return self._addon_slug

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        await self._hassio.start_addon(self._addon_slug)

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        await self._hassio.stop_addon(self._addon_slug)

    async def async_update(self):
        """Update the state."""
        if not self._hassio.is_connected():
            self._state = STATE_UNKNOWN
            return

        info = await self._hassio.get_addon_info(self._addon_slug)
        if info[ATTR_STATE] is None or info[ATTR_STATE] == STATE_NONE:
            self._state = STATE_UNAVAILABLE
        else:
            self._state = info[ATTR_STATE]
