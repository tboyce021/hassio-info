""" Config Flow to configure Hassio Info integration. """
import logging

from homeassistant.components.hassio import DOMAIN as HASSIO_DOMAIN
from homeassistant.config_entries import CONN_CLASS_LOCAL_POLL, ConfigFlow

from .const import DOMAIN, TITLE

_LOGGER = logging.getLogger(__name__)


class HassioInfoFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a Hassio Info config flow."""

    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if HASSIO_DOMAIN not in self.hass.config.components:
            return self.async_abort(reason="hassio_required")
        if user_input is not None:
            return self.async_create_entry(title=TITLE, data={})

        return self.async_show_form(step_id="user")