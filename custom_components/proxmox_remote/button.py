"""Button platform for Proxmox actions."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_setup_platform(hass: HomeAssistant, config, async_add_entities, discovery_info=None):
    """Set up Proxmox action buttons."""
    del config, discovery_info
    integration_data = hass.data[DOMAIN]
    api = integration_data["api"]
    node = integration_data["node"]

    async_add_entities([ProxmoxNodeShutdownButton(api, node)])


class ProxmoxNodeShutdownButton(ButtonEntity):
    """Button to cleanly shutdown the Proxmox node."""

    def __init__(self, api, node: str) -> None:
        self._api = api
        self._node = node
        self._attr_name = f"Proxmox Node {node} Shutdown"
        self._attr_unique_id = f"proxmox_node_shutdown_{node}"

    async def async_press(self) -> None:
        await self.hass.async_add_executor_job(self._api.shutdown_node, self._node)
