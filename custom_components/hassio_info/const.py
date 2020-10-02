"""Constants for the Hassio Info integration."""

DOMAIN = "hassio_info"

ICON = 'mdi:home-assistant'

ATTR_SLUG = "slug"

STATE_NONE = "none"
STATE_STARTED = "started"

SENSOR_VERSION = 'version'
SENSOR_VERSION_LATEST = 'version_latest'

SENSOR_NAMES = {
    SENSOR_VERSION: 'Version',
    SENSOR_VERSION_LATEST: 'Latest Version'
}

SENSOR_TYPES = [
    SENSOR_VERSION,
    SENSOR_VERSION_LATEST
]
