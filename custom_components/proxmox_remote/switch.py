"""Switch platform to control Proxmox VMs."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_setup_platform(hass: HomeAssistant, config, async_add_entities, discovery_info=None):
    """Set up Proxmox VM switches."""
    del config, discovery_info
    integration_data = hass.data[DOMAIN]
    api = integration_data["api"]
    node = integration_data["node"]
    vm_ids = integration_data["vms"]

    entities = [ProxmoxVMSwitch(api, node, vmid) for vmid in vm_ids]
    async_add_entities(entities, True)


class ProxmoxVMSwitch(SwitchEntity):
    """Representation of a Proxmox VM power switch."""

    def __init__(self, api, node: str, vmid: int) -> None:
        self._api = api
        self._node = node
        self._vmid = vmid
        self._attr_name = f"Proxmox VM {vmid}"
        self._attr_unique_id = f"proxmox_vm_{node}_{vmid}"
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs) -> None:
        del kwargs
        await self.hass.async_add_executor_job(self._api.start_vm, self._node, self._vmid)
        await self.async_update()

    async def async_turn_off(self, **kwargs) -> None:
        del kwargs
        await self.hass.async_add_executor_job(self._api.shutdown_vm, self._node, self._vmid)
        await self.async_update()

    async def async_update(self) -> None:
        status = await self.hass.async_add_executor_job(self._api.vm_status, self._node, self._vmid)
        self._attr_is_on = status.get("status") == "running"

    @property
    def extra_state_attributes(self):
        return {"node": self._node, "vmid": self._vmid}
