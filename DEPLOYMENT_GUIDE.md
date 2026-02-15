# Deployment Guide: Arista ZTP with Containerlab

Follow these steps to deploy the ZTP lab and see Zero Touch Provisioning in action.

## 🛠 Prerequisites

- **Containerlab**: Installed on your Linux host.
- **Docker**: Installed and running.
- **Arista cEOS image**: Ensure you have a cEOS image (e.g., `ceos:4.32.9M`) imported into Docker. 
  > [!NOTE]
  > Check your image name with `docker images` and update `ztp-ceos.yaml` if it differs from `ceos:4.32.9M`.

## 🚀 Step 1: Customize Device Identity (Optional)

Containerlab by default assigns random serial numbers and MAC addresses. To ensure consistent targeted provisioning, we use `ceos-config` files to fix these identities.

1.  **Check Identities**: Look at the files in `ztp-data/configs/sw1/ceos-config` and `ztp-data/configs/sw2/ceos-config`.
2.  **Edit if Needed**: You can change the `SERIALNUMBER` and `SYSTEMMACADDR` values in these files.
3.  **Prepare Configs**: Ensure you have matching configuration files in `ztp-data/configs/` named after the serial numbers (e.g., `123111.cfg`).

## 🏗 Step 2: Build the ZTP Server

The ZTP server handles both DHCP (via `dnsmasq`) and HTTP (via Python) to serve the bootstrap script and configs.

```bash
# Build the custom image
bash docker-build-ztp-server.sh
```

## 🏗 Step 3: Deploy the Topology


Spin up the lab using Containerlab. This will create the ZTP server, the management switch, and the nodes to be provisioned.

```bash
sudo clab deploy -t ztp-ceos.yaml
```

> [!IMPORTANT]
> The switches (`sw1`, `sw2`) start with no configuration and will immediately start sending DHCP requests.

## 📺 Step 3: Monitor logs

Open a new terminal to watch the ZTP server logs. This is where you'll see the magic happen.

```bash
docker logs -f ztp-server
```

**What to look for:**
1. `DHCPDISCOVER` from the switches.
2. `DHCPOFFER` from the server (providing the bootstrap URL).
3. `GET /bootstrap` - The switch downloads the script.
4. `GET /configs/generic.cfg` - The switch fetches the configuration.

## 🧪 Step 4: Verify the Results

Once the logs show the config download is complete, verify the switch state.

```bash
# Access the switch CLI
docker exec -it sw1 Cli

# Verify hostname (should be ZTP-DEVICE or similar)
show hostname

# Check ZTP status
show ztp status
```

## 🔧 Troubleshooting

- **No DHCP Activity**: Ensure `mgmt-sw` is up and has its interfaces correctly bridged in the `ztp-ceos.yaml`.
- **File Not Found (404)**: If you want to use serial-based provisioning, check the switch serial with `show version` and create a matching file in `ztp-data/configs/<SERIAL>.cfg`.
- **Connection Refused**: Ensure the Python server is running on port 8080 inside the `ztp-server` container.

## 🧹 Cleaning Up

To stop the lab and remove all containers:

```bash
sudo clab destroy -t ztp-ceos.yaml --cleanup
```

