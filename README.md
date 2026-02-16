# Arista ZTP Lab for Containerlab

This project provides a robust, beginner-friendly example of **Zero Touch Provisioning (ZTP)** for Arista EOS switches using **Containerlab**. It demonstrates how network devices can automatically discover their configuration and bootstrap themselves into a production-ready state.

## 🚀 Key Features

- **Centralized Configuration**: All lab variables (IPs, DHCP ranges, file names) are managed in a single `.env` file.
- **Template-Based Automation**: Configuration and topology files are generated from templates, ensuring consistency across the environment.
- **Targeted Provisioning**: Documents how to pre-assign serial and MAC numbers to specific switches (`sw1`, `sw2`) before deployment, ensuring they always get the intended configuration.
- **Serial-Based Logic**: The bootstrap script identifies switches by their serial number, allowing for targeted configuration delivery.
- **Simulated Infrastructure**: Includes a management switch for Layer 2 connectivity and a Linux-based ZTP server.

## 📐 Network Topology

The topology is defined in `arista-ztp-v2.yaml`. All nodes are connected to a management VLAN on the `mgmt-sw`.

```mermaid
graph TD
    subgraph "Provisioning Infrastructure (VLAN 10)"
        ZTP["ztp-server (192.168.100.1)"]
        MSW["mgmt-sw (Central Hub)"]
    end
    
    subgraph "Nodes to be Provisioned"
        SW1["sw1 (Fixed Serial: 123111)"]
        SW2["sw2 (Fixed Serial: 123222)"]
    end
    
    MSW --- ZTP
    MSW --- |eth1| SW1
    MSW --- |eth2| SW2
    SW1 -.-> |Link| SW2
```

## 🔍 How ZTP Works in this Lab

1.  **Preparation**: Run `./reconfigure.py` to populate all templates with values from `.env`.
2.  **Boot**: `sw1` and `sw2` boot with `suppress-startup-config: true`, triggering Arista's native ZTP process.
3.  **Identity Injection**: Before deployment, we use `ceos-config` files to fix the serial and MAC numbers for each node. This prevents Containerlab from assigning random IDs on every boot.
4.  **DHCP Discovery**: The switches send DHCP requests on all interfaces.
5.  **DHCP Response**: The `ztp-server` (running `dnsmasq`) offers an IP and **DHCP Option 67**, pointing to the bootstrap URL (e.g., `http://192.168.100.1:8080/bootstrap`).
6.  **Bootstrap Execution**: The switch downloads and runs the `bootstrap` Python script.
7.  **Serial Detection**: The script runs `FastCli -c "show version"` to detect the hardware serial number (e.g., `123111`).
8.  **Config Fetch**: 
    - It tries to fetch `<SERIAL>.cfg` (e.g., `123111.cfg`) from the server.
    - If no specific config exists, it falls back to `generic.cfg`.
9.  **Application**: The config is written to `/mnt/flash/startup-config`, and the device reboots (or applies) to complete provisioning.

## 📂 Project Structure

```text
.
├── DEPLOYMENT_GUIDE.md        # Detailed setup instructions
├── README.md                  # Project overview (you are here)
├── .env                       # Central environment variables
├── reconfigure.py             # Script to generate configs from templates
├── arista-ztp-v2.yaml.template # Topology template
├── dnsmasq.conf.template      # DHCP configuration template
├── ztp-data/
│   ├── bootstrap.template     # ZTP bootstrap script template
│   └── configs/               # Folder for .cfg files
└── ...
```

---

For detailed setup instructions, see the [Deployment Guide](DEPLOYMENT_GUIDE.md).


