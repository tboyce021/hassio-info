"""Support for Hassio Info."""
import logging

from homeassistant.components.hassio import DOMAIN as HASSIO_DOMAIN
from homeassistant.helpers.discovery import load_platform

from .const import DOMAIN
from .handler import extend_hassio

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = [HASSIO_DOMAIN]


async def async_setup(hass, config):
    """Set up the Hassio Info component."""
    extend_hassio(hass.data[HASSIO_DOMAIN])
    
    load_platform(hass, 'sensor', DOMAIN, {}, config)
    load_platform(hass, 'switch', DOMAIN, {}, config)
    return True
