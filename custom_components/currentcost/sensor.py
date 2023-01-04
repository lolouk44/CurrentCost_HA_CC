"""Support for reading Current Cost data from a serial port."""
import json
import logging
import xmltodict
import sys

import serial_asyncio
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity,  SensorDeviceClass, SensorStateClass
from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID, CONF_DEVICES, EVENT_HOMEASSISTANT_STOP, POWER_WATT
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)


CONF_SERIAL_PORT = "serial_port"
CONF_BAUDRATE = "baudrate"
CONF_DEVICES = "devices"

DEFAULT_NAME = "Current Cost"
DEFAULT_ID = "abaaa250-fd59-46e1-abd8-07545fb2b297"
DEFAULT_BAUDRATE = 57600
DEFAULT_DEVICES = [0,1,2,3,4,5,6,7,8,9]

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_SERIAL_PORT): cv.string,
        vol.Optional(CONF_BAUDRATE, default=DEFAULT_BAUDRATE): cv.positive_int,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_UNIQUE_ID, default=DEFAULT_ID): cv.string,
        vol.Optional(CONF_DEVICES, default=DEFAULT_DEVICES): vol.All(cv.ensure_list, [vol.Range(min=0, max=9)]),
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Current Cost sensor platform."""
    name = config.get(CONF_NAME)
    unique_id = config.get(CONF_UNIQUE_ID)
    port = config.get(CONF_SERIAL_PORT)
    baudrate = config.get(CONF_BAUDRATE)
    devices = config.get(CONF_DEVICES)
    _LOGGER.debug("devices: %s", config.get(CONF_DEVICES))
    #sensor = []
    sensor = CurrentCostSensor(name, f"current-cost-{unique_id}", port, baudrate, devices)
    #for variable in devices:
    #    sensor.append(CurrentCostSensor(f"{name}_appliance_{variable}", port, baudrate))
    #sensor.append(CurrentCostSensor(f"{name}_temperature", port, baudrate))

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, sensor.stop_serial_read())
    async_add_entities([sensor], True)


class CurrentCostSensor(SensorEntity):
    """Representation of a Current Cost sensor."""

    def __init__(self, name, unique_id, port, baudrate, devices):
        """Initialize the Current Cost sensor."""
        self._name = name
        self._attr_unique_id = unique_id
        self._unit = POWER_WATT
        self._icon = "mdi:flash-outline"
        self._device_class = SensorDeviceClass.POWER
        self._state_class = SensorStateClass.MEASUREMENT
        self._state = None
        self._port = port
        self._baudrate = baudrate
        self._serial_loop_task = None
        self._attributes = {"Temperature": None}
        self._devices = devices
        for variable in devices:
            self._attributes[f"Appliance {variable}"] = None
            self._attributes[f"Appliance {variable} Last 24h"] = None
            self._attributes[f"Appliance {variable} Last 30 days"] = None

    async def async_added_to_hass(self):
        """Handle when an entity is about to be added to Home Assistant."""
        self._serial_loop_task = self.hass.loop.create_task(
            self.serial_read(self._port, self._baudrate)
        )

    async def serial_read(self, device, rate, **kwargs):
        """Read the data from the port."""
        reader, _ = await serial_asyncio.open_serial_connection(
            url=device, baudrate=rate, **kwargs
        )
        while True:
            try:
                line = await reader.readline()
                line = line.decode("utf-8").strip()
                _LOGGER.debug("Line Received: %s", line)
            except Exception as error:
                _LOGGER.error("Error Reading From Serial Port: %s", error)
                pass
            try:
                data = xmltodict.parse(line)
                # Data can be parsed from line, continuing
                # First read real time data
                try:
                    appliance = int(data['msg']['sensor'])
                except:
                    appliance = None
                    pass
                
                temperature = None
                try:
                    temperature = float(data['msg']['tmpr'])
                except:
                    pass
                try:
                    temperature = float(data['msg']['tmprF'])
                except:
                    pass
                try:
                    imp = int(data['msg']['imp'])
                    ipu = int(data['msg']['ipu'])
                except:
                    imp = None
                    ipu = None
                    pass
                try:
                    wattsch1 = int(data['msg']['ch1']['watts'])
                except:
                    wattsch1 = 0
                    pass
                try:
                    wattsch2 = int(data['msg']['ch2']['watts'])
                except:
                    wattsch2 = 0
                    pass
                try:
                    wattsch3 = int(data['msg']['ch3']['watts'])
                except:
                    wattsch3 = 0
                    pass
                total_watts = wattsch1 + wattsch2 + wattsch3
                if appliance == 0:
                    self._state = total_watts
                    self._attributes[f"Channel 1"] = wattsch1
                    self._attributes[f"Channel 2"] = wattsch2
                    self._attributes[f"Channel 3"] = wattsch3
                if appliance is not None:
                    if imp is not None:
                        self._attributes[f"Impulses {appliance}"] = imp
                        self._attributes[f"Impulses/Unit {appliance}"] = ipu
                    else:
                        self._attributes[f"Appliance {appliance}"] = total_watts
                if temperature is not None:
                    self._attributes["Temperature"] = temperature
                    
                # Then read history data

                for variable in self._devices:
                    #self._attributes[f"Appliance {variable}"] = None
                    try:
                        if int(data['msg']['hist']['data'][int(variable)]['sensor']) == int(variable):
                            applianceHist = int(data['msg']['hist']['data'][int(variable)]['sensor'])
                        else:
                            applianceHist = None
                    except:
                        applianceHist = None
                        pass
                    if applianceHist is not None:
                        try:
                            last24h = float(data['msg']['hist']['data'][applianceHist]['d001'])
                            self._attributes[f"Appliance {applianceHist} Last 24h"] = last24h
                        except:
                            pass
                        try:
                            last30d = float(data['msg']['hist']['data'][applianceHist]['m001'])
                            self._attributes[f"Appliance {applianceHist} Last 30 days"] = last30d
                        except:
                            pass
                    
                # Then update HA Sensor info
                self.async_schedule_update_ha_state()

            # Data can not be parsed from line, raising exception
            except:
                _LOGGER.error(f"Error parsing data from serial port:\n    {sys.exc_info()[1]}\n    line received:\n    {line}")
                pass

    async def stop_serial_read(self):
        """Close resources."""
        if self._serial_loop_task:
            self._serial_loop_task.cancel()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def extra_state_attributes(self):
        """Return the attributes of the entity (if any JSON present)."""
        return self._attributes

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the units of measurement."""
        return self._unit

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self._device_class

    @property
    def state_class (self):
        """Return the state class of the sensor."""
        return self._state_class
