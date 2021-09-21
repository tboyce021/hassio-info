"""
Support for Hassio switches.
"""
from __future__ import annotations

from homeassistant.components.hassio import (
    async_start_addon,
    async_stop_addon
)
from homeassistant.components.hassio.const import DATA_KEY_ADDONS
from homeassistant.components.hassio.entity import HassioAddonEntity
from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_STATE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import ADDONS_COORDINATOR


STATE_STARTED = "started"

SWITCH_DESCRIPTION_ADDON_STATE = SwitchEntityDescription(
    key=ATTR_STATE,
    name="State",
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Switch set up for Hass.io config entry."""
    coordinator = hass.data[ADDONS_COORDINATOR]

    entities = [
        HassioInfoAddonSwitch(
            coordinator, SWITCH_DESCRIPTION_ADDON_STATE, addon
        )
        for addon in coordinator.data["addons"].values()
    ]
    async_add_entities(entities, True)


class HassioInfoAddonSwitch(HassioAddonEntity, SwitchEntity):
    """Switch to turn on/off a Hass.io add-on."""

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return bool(self.coordinator.data[DATA_KEY_ADDONS][self._addon_slug][
            self.entity_description.key] == STATE_STARTED)

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        await async_start_addon(self.hass, self.addon_slug)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        await async_stop_addon(self.hass, self.addon_slug)
        await self.coordinator.async_request_refresh()
