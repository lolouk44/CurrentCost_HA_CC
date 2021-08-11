![currentcost logo](logo.png)

[![version](https://img.shields.io/github/v/release/lolouk44/CurrentCost_HA_CC)](https://github.com/lolouk44/CurrentCost_HA_CC/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
# CurrentCost Custom Component for Home Assistant

This repo is a custom component for [Home Assistant](https://www.home-assistant.io/)

The `currentcost` sensor platform is using the data provided by a [CurrentCost](http://www.currentcost.com/) device connected to the serial port via a [data cable](http://www.currentcost.com/product-datacable.html).

The sensor returns the Total Power (usually on Appliance 0) as a state, and the temperature as an attribute.
It is also possible to list additional appliances by listing the appliance number that CurrentCost devices are paired with

Confirmed working devices:
- Currentcost Envi (aka CC128)
- Currentcost EnviR

## HACS Installation

The easiest way to install this custom component is via [HACS](https://hacs.xyz/)
1) Follow the [installation instructions](https://hacs.xyz/docs/installation/prerequisites) to install HACS
2) Click on the HACS icon in the left side bar, click on the elipsis on the right handside and select `Custom Repositories`
3) enter `https://github.com/lolouk44/CurrentCost_HA_CC` in the URL box, select `Integration` as a category


## Manual Installation
To install the CurrentCost custom component:
1) Create a folder called `custom_components` in your config folder (same folder where configuration.yaml is locate, if that folder does not already exist)
2) Create a folder called `currentcost` (no spaces, lowercase)
3) Copy the files inside the [CurrentCost_HA_CC](https://github.com/lolouk44/CurrentCost_HA_CC/tree/master/custom_components/CurrentCost_HA_CC) folder into the `currentcost` folder


## Configuration

To setup a CurrentCost sensor to your installation:
1) Add the following code to your `configuration.yaml` file under the existing `sensor` and `template` headers. (do not copy/paste the `sensor` or `template` headers). 
If `sensor` or `template` do not already exist, add the code block including the `sensor` or `template` header.

```yaml
# Example configuration.yaml entry
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
        unit_of_measurement: '°C'
        state: '{{ state_attr("sensor.current_cost", "Temperature") | float -3 }}' # Manual adjustment of -3°C in case the temp sensor is high than real temperature
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


### serial_port:
**description**: Local serial port where the sensor is connected and access is granted.  
**required**: true  
**type**: string  
note: when using HA in a docker environment, make sure you assign a name to the device when mounting it, e.g. `--device=/dev/ttyUSB0:/dev/ttyUSB0` as opposed to just `--device=/dev/ttyUSB0`
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
