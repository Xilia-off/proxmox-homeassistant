"""The Proxmox Remote integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.const import CONF_PASSWORD, CONF_PORT, CONF_USERNAME
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.typing import ConfigType

from .api import ProxmoxRemoteAPI
from .const import (
    CONF_HOST,
    CONF_NODE,
    CONF_VERIFY_SSL,
    CONF_VMS,
    DEFAULT_PORT,
    DEFAULT_VERIFY_SSL,
    DOMAIN,
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_HOST): cv.string,
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
                vol.Required(CONF_NODE): cv.string,
                vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
                vol.Optional(CONF_VERIFY_SSL, default=DEFAULT_VERIFY_SSL): cv.boolean,
                vol.Optional(CONF_VMS, default=[]): vol.All(cv.ensure_list, [vol.Coerce(int)]),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

SERVICE_VM_SCHEMA = vol.Schema({vol.Required("vmid"): vol.Coerce(int)})


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Proxmox Remote from YAML."""
    conf = config.get(DOMAIN)
    if conf is None:
        return True

    api = ProxmoxRemoteAPI(
        host=conf[CONF_HOST],
        username=conf[CONF_USERNAME],
        password=conf[CONF_PASSWORD],
        verify_ssl=conf[CONF_VERIFY_SSL],
        port=conf[CONF_PORT],
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["api"] = api
    hass.data[DOMAIN]["node"] = conf[CONF_NODE]
    hass.data[DOMAIN]["vms"] = conf[CONF_VMS]

    async def _handle_start_vm(call: ServiceCall) -> None:
        await hass.async_add_executor_job(api.start_vm, conf[CONF_NODE], call.data["vmid"])

    async def _handle_stop_vm(call: ServiceCall) -> None:
        await hass.async_add_executor_job(api.stop_vm, conf[CONF_NODE], call.data["vmid"])

    async def _handle_shutdown_vm(call: ServiceCall) -> None:
        await hass.async_add_executor_job(api.shutdown_vm, conf[CONF_NODE], call.data["vmid"])

    async def _handle_shutdown_node(call: ServiceCall) -> None:
        del call
        await hass.async_add_executor_job(api.shutdown_node, conf[CONF_NODE])

    hass.services.async_register(DOMAIN, "start_vm", _handle_start_vm, schema=SERVICE_VM_SCHEMA)
    hass.services.async_register(DOMAIN, "stop_vm", _handle_stop_vm, schema=SERVICE_VM_SCHEMA)
    hass.services.async_register(DOMAIN, "shutdown_vm", _handle_shutdown_vm, schema=SERVICE_VM_SCHEMA)
    hass.services.async_register(DOMAIN, "shutdown_node", _handle_shutdown_node)

    await async_load_platform(hass, "switch", DOMAIN, {}, config)
    await async_load_platform(hass, "button", DOMAIN, {}, config)

    return True
