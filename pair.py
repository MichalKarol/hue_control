from config import ADDRESSES
from philips_hue_bulb import PhilipsHueBulb

bulbs = [PhilipsHueBulb(addr) for addr in ADDRESSES]

for bulb in bulbs:
    bulb.pair()
