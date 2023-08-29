from config import ADDRESSES
from philips_hue_bulb import PhilipsHueBulb
import time

MINUTE = 60

bulbs = [PhilipsHueBulb(addr) for addr in ADDRESSES]
for bulb in bulbs:
    bulb.connect()

for bulb in bulbs:
    bulb.off()

for bulb in bulbs:
    bulb.color(255, True)
    bulb.brightness(5)

for bulb in bulbs:
    bulb.on()

for i in range(20):
    for bulb in bulbs:
        bulb.color(255 - i * 10, True)
        bulb.brightness(20 + i * 4)
    time.sleep(MINUTE)

for i in range(10):
    for bulb in bulbs:
        bulb.color(255 - i * 10, False)
        bulb.brightness(min(100 + i * 17, 255))
    time.sleep(MINUTE)
