"""Support for Hassio Info."""
from __future__ import annotations

from datetime import timedelta
from typing import Any

from homeassistant.components.hassio import DOMAIN as HASSIO_DOMAIN
from homeassistant.components.hassio import HassioDataUpdateCoordinator
from homeassistant.components.hassio.const import ATTR_SLUG
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_STATE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceRegistry, async_get_registry
from homeassistant.helpers.typing import ConfigType


PLATFORMS = ["switch"]

SCAN_INTERVAL = timedelta(seconds=60)

ADDONS_COORDINATOR = "hassio_info_addons_coordinator"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:  # noqa: C901
    """Set up the Hassio Info component."""
    if HASSIO_DOMAIN not in hass.config.components:
        _LOGGER.error("The core Supervisor integration is not set up")
        return False

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry."""
    dev_reg = await async_get_registry(hass)
    coordinator = HassioInfoDataUpdateCoordinator(hass, entry, dev_reg)
    hass.data[ADDONS_COORDINATOR] = coordinator
    await coordinator.async_refresh()

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    # Pop add-on data
    hass.data.pop(ADDONS_COORDINATOR, None)

    return True

class HassioInfoDataUpdateCoordinator(HassioDataUpdateCoordinator):
    """Class to retrieve Hass.io status."""

    def __init__(
        self, hass: HomeAssistant, config_entry: ConfigEntry, dev_reg: DeviceRegistry
    ) -> None:
        """Initialize coordinator."""
        super().__init__(hass, config_entry, dev_reg)
        self.update_interval = SCAN_INTERVAL
        self._schedule_refresh()

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        new_data = await HassioDataUpdateCoordinator._async_update_data(self)

        hassio = self.hass.data[HASSIO_DOMAIN]
        supervisor_info = await hassio.get_supervisor_info()

        for addon in supervisor_info.get("addons", []):
            addon_slug = addon[ATTR_SLUG]
            if addon_slug in new_data["addons"]:
                new_data["addons"][addon_slug][ATTR_STATE] = addon[ATTR_STATE]

        return new_data
