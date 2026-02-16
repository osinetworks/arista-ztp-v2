# Deployment Guide: Arista ZTP with Containerlab

Follow these steps to deploy the ZTP lab and see Zero Touch Provisioning in action.

## 🛠 Prerequisites

- **Containerlab**: Installed on your Linux host.
- **Docker**: Installed and running.
- **Arista cEOS image**: Ensure you have a cEOS image (e.g., `ceos:4.32.9M`) imported into Docker. 
  > [!NOTE]
  > Check your image name with `docker images` and update `arista-ztp-v2.yaml.template` if it differs from `ceos:4.32.9M`.

## 🚀 Step 1: Customize Device Identity (Optional)

Containerlab by default assigns random serial numbers and MAC addresses. To ensure consistent targeted provisioning, we use `ceos-config` files to fix these identities.

1.  **Check Identities**: Look at the files in `ztp-data/configs/sw1/ceos-config` and `ztp-data/configs/sw2/ceos-config`.
2.  **Edit if Needed**: You can change the `SERIALNUMBER` and `SYSTEMMACADDR` values in these files.
3.  **Prepare Configs**: Ensure you have matching configuration files in `ztp-data/configs/` named after the serial numbers (e.g., `123111.cfg`).

## ⚙️ Step 2: Configure Environment

We use a centralized configuration system to manage lab variables.

1.  **Environment File**: Ensure you have a `.env` file in the root directory. You can use `.env.template` as a starting point.
    ```bash
    cp .env.template .env
    ```
2.  **Reconfigure**: Run the reconfiguration script to generate the actual files from templates:
    ```bash
    ./reconfigure.py
    ```
    This will update `dnsmasq.conf`, `ztp-data/bootstrap`, and `arista-ztp-v2.yaml`.

## 🏗 Step 3: Build the ZTP Server

The ZTP server handles both DHCP (via `dnsmasq`) and HTTP (via Python) to serve the bootstrap script and configs.

```bash
# Build the custom image
bash docker-build-ztp-server.sh
```

## 🏗 Step 4: Deploy the Topology

Spin up the lab using Containerlab. This will create the ZTP server, the management switch, and the nodes to be provisioned.

```bash
sudo ./run.sh
```

> [!IMPORTANT]
> The switches (`sw1`, `sw2`) start with no configuration and will immediately start sending DHCP requests.

## 📺 Step 5: Monitor logs

Open a new terminal to watch the ZTP server logs. This is where you'll see the magic happen.

```bash
docker logs -f ztp-server
```

**What to look for:**
1. `DHCPDISCOVER` from the switches.
2. `DHCPOFFER` from the server (providing the bootstrap URL).
3. `GET /bootstrap` - The switch downloads the script.
4. `GET /configs/<SERIAL>.cfg` - The switch fetches its specific configuration.

## 🧪 Step 6: Verify the Results

Once the logs show the config download is complete, verify the switch state.

```bash
# Access the switch CLI
docker exec -it sw1 Cli

# Verify hostname (should match your config)
show hostname

# Check ZTP status
show ztp status
```

## 🔧 Troubleshooting

- **No DHCP Activity**: Ensure `mgmt-sw` is up and has its interfaces correctly bridged in the `arista-ztp-v2.yaml`.
- **File Not Found (404)**: Check the switch serial with `show version` and ensure a matching file exists in `ztp-data/configs/`.
- **Reconfiguration Issues**: If variables aren't updating, ensure you edited `.env` and ran `./reconfigure.py`.

## 🧹 Cleaning Up

To stop the lab and remove all containers:

```bash
sudo ./stop.sh
```


