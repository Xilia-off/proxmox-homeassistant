"""API wrapper around ProxmoxVE for Home Assistant."""

from __future__ import annotations

from typing import Any

from proxmoxer import ProxmoxAPI


class ProxmoxRemoteAPI:
    """Thin wrapper for Proxmox operations used by entities and services."""

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        verify_ssl: bool,
        port: int,
    ) -> None:
        self._host = host
        self._username = username
        self._password = password
        self._verify_ssl = verify_ssl
        self._port = port
        self._client = self._build_client()

    def _build_client(self) -> ProxmoxAPI:
        return ProxmoxAPI(
            self._host,
            user=self._username,
            password=self._password,
            verify_ssl=self._verify_ssl,
            port=self._port,
            service="PVE",
        )

    def list_vms(self, node: str) -> list[dict[str, Any]]:
        return self._client.nodes(node).qemu.get()

    def vm_status(self, node: str, vmid: int) -> dict[str, Any]:
        return self._client.nodes(node).qemu(vmid).status.current.get()

    def start_vm(self, node: str, vmid: int) -> None:
        self._client.nodes(node).qemu(vmid).status.start.post()

    def stop_vm(self, node: str, vmid: int) -> None:
        self._client.nodes(node).qemu(vmid).status.stop.post()

    def shutdown_vm(self, node: str, vmid: int) -> None:
        self._client.nodes(node).qemu(vmid).status.shutdown.post()

    def shutdown_node(self, node: str) -> None:
        self._client.nodes(node).status.shutdown.post()
