##Usage:

**Please note: Home Assistant 2021.12 or higher is required for this custom component to work**

Add the following code to your `configuration.yaml` file under the existing `sensor` and `template` headers. (do not copy/paste the `sensor` or `template` headers). 
If `sensor` or `template` do not already exist, add the code block including the `sensor` or `template` header.

```yaml
sensor:
  - platform: currentcost
    serial_port: /dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0
    name: Current Cost
    baudrate: 57600
    devices:
      - 0
      - 2
      - 9
  # Add this sensor if you want to see data in the energy tab
  - platform: integration
    source: sensor.current_cost
    name: Total Energy
    unit_prefix: k
    round: 2

template:
  - sensor:
      - name: "CurrentCost Temperature"
        unit_of_measurement: '°C' # or °F for Fahrenheits
        state: '{{ state_attr("sensor.current_cost", "Temperature") | float -3 }}' # Manual adjustment of -3°C in case the temp sensor is higher than real temperature
        device_class: temperature
        state_class: measurement # Add state_class: measurement for long term statistics are required
  - sensor:
      - name: "CurrentCost Power"
        unit_of_measurement: 'W'
        state: '{{ state_attr("sensor.current_cost", "Appliance 0") }}'
        device_class: power
        state_class: measurement
  - sensor:
      - name: "Dehumidifier Power"
        unit_of_measurement: 'W'
        state: '{{ state_attr("sensor.current_cost", "Appliance 2") }}'
        device_class: power
        state_class: measurement
  - sensor:
      - name: "Total Energy Used Last 24h" # Note: this data is published by the Current Cost device every 2h
        unit_of_measurement: 'KWh'
        state: '{{ state_attr("sensor.current_cost", "Appliance 0 Last 24h") }}'
        device_class: energy
```

{% if installed %}

## Changes as compared to your installed version:
The sensors unit of measurement is no longer returned with the sensor
Please update your template sensors (see README)

### Breaking Changes
The sensors unit of measurement is no longer returned with the sensor
Please update your template sensors (see README)

### Changes

### Features

{% if version_installed.replace(".","") | int < 13  %}
- Added HACS
{% endif %}

### Bugfixes

---
{% endif %}