"""
Provides a Group with additional light specific state attributes.

Allows the group to be treated as a light.
"""

from homeassistant.const import STATE_ON

from homeassistant.components.group import (Group)

from homeassistant.components.light import \
    (ATTR_BRIGHTNESS, ATTR_COLOR_TEMP, ATTR_RGB_COLOR, ATTR_XY_COLOR, Light)


class GroupLight(Group, Light):
    """Extension to Group to add light specific state attributes."""

    # pylint: disable=too-many-arguments
    def __init__(self, hass, name, entity_ids=None, user_defined=True,
                 icon=None, view=False, object_id=None, group_domain='light'):
        """Defer to Group constructor."""
        Group.__init__(self, hass, name, entity_ids=entity_ids,
                       user_defined=user_defined, icon=icon, view=view,
                       object_id=object_id, group_domain=group_domain)

    @property
    def is_on(self):
        """Group of lights is on."""
        return self.state is STATE_ON

    @property
    def brightness(self):
        """Brightness of the light group."""
        new_brightness = 0
        for state in self._tracking_states:
            if ATTR_BRIGHTNESS not in state.attributes:
                return None
            new_brightness += state.attributes.get(ATTR_BRIGHTNESS)
        new_brightness /= float(len(self._tracking_states))
        return new_brightness

    @property
    def color_temp(self):
        """Return the CT color value."""
        for state in self._tracking_states:
            if ATTR_COLOR_TEMP not in state.attributes:
                return None
            return state.attributes.get(ATTR_COLOR_TEMP)

    @property
    def xy_color(self):
        """Return the XY color value."""
        for state in self._tracking_states:
            if ATTR_XY_COLOR not in state.attributes:
                return None
            return state.attributes.get(ATTR_XY_COLOR)

    @property
    def rgb_color(self):
        """Return the RGB color value."""
        for state in self._tracking_states:
            if ATTR_RGB_COLOR not in state.attributes:
                return None
            return state.attributes.get(ATTR_RGB_COLOR)

    @property
    def state_attributes(self):
        """Return the state attributes for the group."""
        data = {}
        # pylint: disable=no-member
        data.update(Light.state_attributes.fget(self))
        # pylint: disable=no-member
        data.update(Group.state_attributes.fget(self))
        return data
