# Philips Hue GU10 LTG002 Bluetooth Python API
The purpose of this repository is to implement communication with LTG002 bulbs using only Bluetooth with pairing.

## Pairing
Run `pair.py` and get close to the bulb to increase BT signal strength.

## Colors
Warm values are mapped between range of 0-255, however cold colors are only available between ranges of 128-255.

## Technical issues
Some characteristics used are not broadcasted by the device so have to be faked in `philips_hue_bulb.py` in order to achieve results.
