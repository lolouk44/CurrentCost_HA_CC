##Usage:

Add the following to your `configuration.yaml` file under the `sensor:` header:

```yaml
  - platform: currentcost
    serial_port: /dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0
    name: Current Cost
    baudrate: 57600
    devices:
      - 0
      - 2
      - 9

  - platform: template
    sensors:
      currentcost_temperature:
        entity_id: sensor.current_cost
        unit_of_measurement: '°C'
        value_template: '{{ state_attr("sensor.current_cost", "Temperature")[:-3] | float }}'
        friendly_name: CurrentCost Temperature
      currentcost_power:
        entity_id: sensor.current_cost
        unit_of_measurement: 'W'
        value_template: '{{ state_attr("sensor.current_cost", "Appliance 0")[:-2] | int }}'
        friendly_name: CurrentCost Power
      dehumidifier_power:
        entity_id: sensor.current_cost
        unit_of_measurement: 'W'
        value_template: '{{ state_attr("sensor.current_cost", "Appliance 2")[:-2] | int }}'
        friendly_name: Dehumidifier Power
```

{% if installed %}

## Changes as compared to your installed version:

### Breaking Changes

### Changes

### Features

{% if version_installed.replace("v", "").replace(".","") | int < 013  %}
- Added HACS

### Bugfixes

{% endif %}
---
{% endif %}