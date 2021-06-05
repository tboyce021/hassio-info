"""Support for Hassio Info."""
import logging

from homeassistant.components.hassio import DOMAIN as HASSIO_DOMAIN
from homeassistant.helpers.discovery import load_platform

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = [HASSIO_DOMAIN]


async def async_setup(hass, config):
    """Set up the Hassio Info component."""
    if HASSIO_DOMAIN not in hass.config.components:
        _LOGGER.error("The core Supervisor integration is not set up")
        return False

    return True

async def async_setup_entry(hass, entry):
    """Set up Hassio Info from a config entry."""
    for component in ["switch"]:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True

async def async_unload_entry(hass, entry):
    """Unload Hassio Info config entry."""
    for component in ["switch"]:
        await hass.config_entries.async_forward_entry_unload(entry, component)

    return True
