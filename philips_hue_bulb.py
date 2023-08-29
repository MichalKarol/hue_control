import asyncio
from uuid import uuid4
from bluepy.btle import *
from bleak import BleakClient


class PhilipsHueBulb:
    def __init__(self, address) -> None:
        self.address = address
        self.peripheral = None

    def connect(self):
        if self.peripheral:
            return self.peripheral
        self.peripheral = Peripheral()
        self.peripheral.connect(self.address, ADDR_TYPE_RANDOM)
        self.characteristic_hex_map = {
            hex(characteristic.getHandle()): characteristic
            for characteristic in self.peripheral.getCharacteristics()
        }
        # Fake characteristics
        self.characteristic_hex_map["0x64"] = Characteristic(
            self.peripheral, uuid4(), None, 0b00001000, int("64", 16)
        )
        self.characteristic_hex_map["0x41"] = Characteristic(
            self.peripheral, uuid4(), None, 0b00001000, int("41", 16)
        )
        self.characteristic_hex_map["0x5c"] = Characteristic(
            self.peripheral, uuid4(), None, 0b00001000, int("5c", 16)
        )
        print(self.characteristic_hex_map["0x14"].read().hex())
        return self.peripheral

    def pair(self):
        async def inner():
            async with BleakClient(self.address) as client:
                while True:
                    hex_characteristics = {
                        hex(key): characteristic
                        for key, characteristic in client.services.characteristics.items()
                    }
                    await client.write_gatt_char(
                        hex_characteristics["0x22"], b"\x01", True
                    )
                    value = await client.read_gatt_char(hex_characteristics["0x22"])
                    if value[0] == 0x01:
                        break

                paired = await client.pair()
                print(f"Paired: {paired}")

        asyncio.run(inner())

    def off(self):
        print(self.characteristic_hex_map["0x40"].read().hex())
        self.characteristic_hex_map["0x40"].write(bytes.fromhex("01010005020400"))

    def on(self):
        print(self.characteristic_hex_map["0x40"].read().hex())
        self.characteristic_hex_map["0x40"].write(bytes.fromhex("01010105020400"))

    def color(self, value, warm):
        value_warm = 1 if warm else 0
        padded_value = hex(value)[2:].zfill(2)
        padded_warm = hex(value_warm)[2:].zfill(2)
        print(self.characteristic_hex_map["0x40"].read().hex())
        self.characteristic_hex_map["0x40"].write(
            bytes.fromhex(f"0101010302{padded_value}{padded_warm}05020100")
        )

    def brightness(self, value):
        padded_value = hex(value)[2:].zfill(2)
        print(self.characteristic_hex_map["0x40"].read().hex())
        self.characteristic_hex_map["0x40"].write(
            bytes.fromhex(f"0201{padded_value}05020400")
        )
