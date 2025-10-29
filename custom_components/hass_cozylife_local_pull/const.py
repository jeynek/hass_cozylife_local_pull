"""Constants for the CozyLife Local Pull integration."""

DOMAIN = "hass_cozylife_local_pull"

SIGNAL_NEW_TCP_CLIENT = f"{DOMAIN}_new_tcp_client"

CONF_LANG = "lang"
CONF_IP_ADDRESS = "ip_address"

# Device type codes
SWITCH_TYPE_CODE = '00'
LIGHT_TYPE_CODE = '01'
SENSOR_TYPE_CODE = '02'
SUPPORT_DEVICE_CATEGORY = [SWITCH_TYPE_CODE, LIGHT_TYPE_CODE, SENSOR_TYPE_CODE]

# Device DPIDs (strings)
SWITCH = '1'
WORK_MODE = '2'
COLOR_TEMP = '3'  # Color temperature for lights (0-1000)
BRIGHT = '4'
HUE = '5'  # 0-65535 (scale to 0-360)
SAT = '6'  # 0-65535 (scale to 0-1000)

# Sensor DPIDs
SENSOR_TEMP = '8'  # Temperature *10
HUMIDITY = '4'  # Humidity % (or *10)
BATTERY = '9'  # Battery *10

LIGHT_DPID = [SWITCH, WORK_MODE, COLOR_TEMP, BRIGHT, HUE, SAT]
SWITCH_DPID = [SWITCH]
SENSOR_DPID = [SENSOR_TEMP, HUMIDITY, BATTERY]

LANG = 'en'
API_DOMAIN = 'api-us.doiting.com'
