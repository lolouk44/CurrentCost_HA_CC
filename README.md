# CurrentCost Custom Component for Home Assistant

This repo is a custom component for [Home Assistant](https://www.home-assistant.io/)

The `currentcost` sensor platform is using the data provided by a [CurrentCost](http://www.currentcost.com/) device connected to the serial port via a [data cable](http://www.currentcost.com/product-datacable.html).

The sensor returns the Total Power (usually on Appliance 0) as a state, and the temperature as an attribute.
It is also possible to list additional appliances by listing the appliance number that CurrentCost devices are paired with

Confirmed working devices:
- Currentcost EnviR


## Configuration

To setup a CurrentCost sensor to your installation:
1) Create a folder called `custom_components` in your config folder (same folder where configuration.yaml is locate, if that folder does not already exist)
2) Create a folder called `currentcost` (no spaces, lowercase)
3) Copy the files from this repo into the `currentcost` folder
4) Add the following to your `configuration.yaml` file under the `sensor` header:

```yaml
# Example configuration.yaml entry
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
        value_template: '{{ state_attr("sensor.current_cost", "Temperature")[:-3]  }}'
        friendly_name: CurrentCost Temperature
      currentcost_power:
        entity_id: sensor.current_cost
        unit_of_measurement: 'W'
        value_template: '{{ state_attr("sensor.current_cost", "Appliance 0")[:-2]  }}'
        friendly_name: CurrentCost Power
      dehumidifier_power:
        entity_id: sensor.current_cost
        unit_of_measurement: 'W'
        value_template: '{{ state_attr("sensor.current_cost", "Appliance 2")[:-2]  }}'
        friendly_name: Dehumidifier Power
```


### serial_port:
**description**: Local serial port where the sensor is connected and access is granted.  
**required**: true  
**type**: string  
### name:
**description**: Friendly name to use for the frontend. Default to "Current Cost".  
**required**: false  
**type**: string  
### baudrate:
**description**: Baudrate of the serial port. 57600 is the value needed for EnviR devices.  
**required**: false  
**default**: 57600 Bps  
**type**: integer  
### devices:
**description**: List of appliance numbers paired with a CurrentCost sensor  
**required**: false  
**default**: 0  
**type**: integer  
