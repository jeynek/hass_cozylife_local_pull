# AI Slop (GitHub CoPilot) fork of CozyLife Local Control for Home Assistant (Fixed & Optimized)

This fork tries to add humidity and temperature sensor.
This is a modified version (fork) of the original, official `hass_cozylife_local_pull` integration created by the CozyLife Team. The original version appears to be in an early development stage and contains critical bugs that make it largely non-functional in modern Home Assistant installations.

This fork has been completely repaired, modernized, and optimized for maximum reliability and speed on a local network.

**Status as of September 25, 2025: This forked version is verified and fully functional.**

## Key Fixes & Improvements Over the Original

* **Protocol & Color Control Fixes:** The original code misinterpreted the device communication protocol. The key fix addresses the control parameter (DPID `'2'`), which is **not** for switching between color/white modes, but for activating special effects. The new code now correctly uses `'2': 0` for all standard operations, which fully enables changing colors and color temperature.
* **Stability & Reliability:** Fixed bugs that caused the light bulb to become unavailable or crash when changing colors or sending other commands.
* **Code Modernization:** The codebase has been rewritten using modern `async` standards and updated to be compliant with recent Home Assistant versions. All deprecated functions and constants have been replaced, including the switch from Mireds to Kelvin for color temperature.
* **User Interface (UI) Bug Fixes:** Resolved visual glitches in the Home Assistant frontend, such as the brightness slider rendering with the wrong color after switching modes.
* **High-Performance by Default (Optimistic Mode):** The integration has been completely rewritten to be "optimistic" and **does not use polling** to check the bulb's status. It sends commands as quickly as possible and immediately assumes they were successful. This makes it extremely fast and ideal for high-frequency use cases like Ambilight (HyperHDR), while also reducing network traffic. The trade-off is that Home Assistant will not detect state changes made from outside (e.g., using the CozyLife app).

## Tested Hardware
This integration was successfully tested and debugged with the following affordable Wi-Fi RGB bulbs from Temu:
* [Product Link on Temu.com](https://www.temu.com/goods.html?_bg_fs=1&goods_id=601102518752308&sku_id=17605095486273)

## Setup Guide (Step-by-Step)

### 1. First-Time Pairing in the CozyLife App
Before using Home Assistant, you must first pair the bulbs with your Wi-Fi network using the official mobile app.
* Install the **CozyLife Smart** app: [Link for iOS](https://apps.apple.com/cz/app/cozylife-smart/id1548663863?l=cs) (a similar app is available for Android).
* Create an account and follow the in-app instructions to add and connect your bulbs to your **2.4 GHz Wi-Fi network**.
* Name your bulbs in the app for easy identification.

### 2. Network Configuration (IMPORTANT)
For reliable local control, each bulb must have a fixed IP address.
* Log in to your Wi-Fi router's administration page.
* Find the list of connected devices and identify the IP address of your new bulb (e.g., by its name or MAC address).
* In your router's DHCP server settings, set up a **static IP reservation** for the bulb's MAC address. This ensures the bulb will always have the same IP address and never be assigned a different one.
* Repeat this step for all bulbs you wish to integrate. Make a note of their static IP addresses.

### 3. Installation in Home Assistant
* Clone or download this repository.
* Copy the entire `hass_cozylife_local_pull` folder into the `custom_components` directory of your Home Assistant installation. The final path should look like: `/config/custom_components/hass_cozylife_local_pull/`.

### 4. Configuration in `configuration.yaml`
Open your main `configuration.yaml` file and add the following, listing the static IP addresses of your bulbs:
```yaml
hass_cozylife_local_pull:
  lang: en
  ip:
    - "192.168.1.101" # IP Address of your first bulb
    - "192.168.1.102" # IP Address of your second bulb
```

### 5. Restart Home Assistant
Save your changes and restart the entire Home Assistant instance to load the new custom component. Your bulbs should now appear as new entities.

## Troubleshoot
* **Device is Unavailable:** This is most often caused by Wi-Fi signal issues. These bulbs have weak antennas. Ensure a strong 2.4 GHz Wi-Fi signal at the bulb's location. Consider setting up a dedicated 2.4 GHz SSID for your IoT devices to prevent issues with band steering on your router.
* **Check `configuration.yaml`:** Ensure the IP addresses are correct and you have a static IP reservation for each bulb.
* **Check Path:** Ensure the integration is in the correct folder: `custom_components/hass_cozylife_local_pull/`.
* **Router Settings:** Check if "Client Isolation" or "AP Isolation" is enabled on your router's main Wi-Fi network and disable it.

---
*The original project README is preserved below for historical context.*
<details>
  <summary>Show Original README</summary>
  
  # CozyLife & Home Assistant 
  
  CozyLife Assistant integration is developed for controlling CozyLife devices using local net, officially 
  maintained by the CozyLife Team.
  
  
  ## Supported Device Types
  
  - RGBCW Light
  - CW Light
  - Switch & Plug
  
  
  ## Install
  
  * A home assistant environment that can access the external network
  * clone the repo to the custom_components directory
  * configuration.yaml
  ```
  hass_cozylife_local_pull:
   lang: en
   ip:
     - "192.168.1.99"
  ```
  
  
  ### Feedback
  * Please submit an issue
  * Send an email with the subject of hass support to info@cozylife.app
  
  ### Troubleshoot 
  * Check whether the internal network isolation of the router is enabled
  * Check if the plugin is in the right place
  * Restart HASS multiple times
  * View the output log of the plugin
  * It is currently the first version of the plugin, there may be problems that cannot be found
  
  
  ### TODO
  - Sending broadcasts regularly has reached the ability to discover devices at any time
  - Support sensor device
  
  ### PROGRESS
  - None
</details>
