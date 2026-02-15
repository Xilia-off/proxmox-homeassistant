# proxmox-homeassistant

Extension Home Assistant (custom component) pour piloter Proxmox VE via API HTTPS.

## Fonctionnalités

- Switch par VM pour démarrer / éteindre proprement (`shutdown`).
- Bouton pour éteindre le nœud Proxmox.
- Services Home Assistant:
  - `proxmox_remote.start_vm`
  - `proxmox_remote.stop_vm`
  - `proxmox_remote.shutdown_vm`
  - `proxmox_remote.shutdown_node`

## Installation

Copiez le dossier `custom_components/proxmox_remote` dans votre configuration Home Assistant:

```bash
cp -r custom_components/proxmox_remote /config/custom_components/
```

Redémarrez Home Assistant.

## Configuration (`configuration.yaml`)

```yaml
proxmox_remote:
  host: proxmox.rudy3.fr
  port: 8006
  username: root@pam
  password: !secret proxmox_password
  node: pve
  verify_ssl: true
  vms:
    - 100
    - 101
```

## Compatibilité HTTPS

- Avec un endpoint Proxmox en HTTPS (`proxmox.rudy3.fr`), laissez `verify_ssl: true` si votre certificat est valide.
- Si certificat auto-signé en phase de test, vous pouvez temporairement mettre `verify_ssl: false`.
- Home Assistant peut être exposé séparément (ex: `ha.rudy3.fr`), cela n'impacte pas l'API Proxmox tant que HA peut joindre `https://proxmox.rudy3.fr:8006`.
