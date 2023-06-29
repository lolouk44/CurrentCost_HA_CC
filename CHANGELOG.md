## [0.2.5] - 2023-06-30
### Changed
- version bump pyserial-asyncio==0.6 to fix for python 3.11 in 2023.6

## [0.2.4] - 2023-01-14
### Added
- Support for unique_id to help sensor customisation
### Changed
- Replaced deprecated DEVICE_CLASS_* Constants ([fixes #20](https://github.com/lolouk44/CurrentCost_HA_CC/issues/20))
- Fixed default icon (flash-circle -> lightning-bolt-circle)

## [0.2.3] - 2022-09-18
### Changed
- Gracefully handle when unable to read serial port ([fixes #17](https://github.com/lolouk44/CurrentCost_HA_CC/issues/17))

## [0.2.2] - 2021-12-14
### Changed
- Updated Sensor definition: replace deprecated device_state_attributes with extra_state_attributes

## [0.2.1] - 2021-08-19
### Added
- Added handling of temperature in Fahrenheit

## [0.2.0] - 2021-08-11
### Added
- Added last 24h and last 30 days energy used in KWh to the attributes

## [0.1.10] - 2021-08-10
### Changed
- Removed "Setting up State Class" error message used for testing

## [0.1.8] - 2021-08-09
### Added
- Updated support for [Long Term Statistics](https://www.home-assistant.io/blog/2021/08/04/release-20218/#long-term-statistics)
### Changed
- Updated README and INFO to use "modern" Template Sensors and allow support for Long Term Statistics for templated sensors

## [0.1.7] - 2021-07-28
### Breaking Change
- Standardized the way sensor data is reported (removed the unit of measurement) - Please update your templates (see README)

## [0.1.6] - 2021-07-27
### Breaking Change
- Standardized the way sensor data is reported (removed the unit of measurement) - Please update your templates (see README)

## [0.1.5] - 2021-03-30
### Changed
- Added version to manifest

## [0.1.4] - 2020-09-10
### Changed
- repo completely overhauled for a PR to make it ready for publishing in HACS

## [0.1.3] - 2020-09-08
### Changed
- Repo structure changed to be HACS Compliant

## [0.1.2] - 2020-09-08
### Changed
- Better error handling: Stop any data processing when error parsing data

## [0.1.1] - 2020-04-03
### Added
- First release (but not tagged on Github)
