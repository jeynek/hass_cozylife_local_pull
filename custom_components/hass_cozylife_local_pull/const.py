DOMAIN = "hass_cozylife_local_pull"

# http://doc.doit/project-5/doc-8/
SWITCH_TYPE_CODE = '00'
LIGHT_TYPE_CODE = '01'
# sensor type code (placeholder; keep if some devices report sensor-type code)
SENSOR_TYPE_CODE = '02'
SUPPORT_DEVICE_CATEGORY = [SWITCH_TYPE_CODE, LIGHT_TYPE_CODE, SENSOR_TYPE_CODE]

# Device DPIDs (kept as strings to match device message keys)
SWITCH = '1'
WORK_MODE = '2'

# Updated DPIDs & scaling based on iam-medvedev/homebridge-cozylife-temperature-sensor:
# - Temperature: DPID "8" (value = temperature * 10)
# - Humidity:  DPID "4" (value = humidity %)
# - Battery:   DPID "9" (value = battery * 10)
TEMP = '8'
HUMIDITY = '4'
BATTERY = '9'

# Legacy/light DPIDs (values kept as strings)
BRIGHT = '4'
HUE = '5'
SAT = '6'

LIGHT_DPID = [SWITCH, WORK_MODE, TEMP, BRIGHT, HUE, SAT]
SWITCH_DPID = [SWITCH, ]
# Sensor DPID list (temperature, humidity, battery)
SENSOR_DPID = [TEMP, HUMIDITY, BATTERY]

LANG = 'en'
API_DOMAIN = 'api-us.doiting.com'
