# SPDX-FileCopyrightText: 2022 BlitzCityDIY
# SPDX-License-Identifier: MIT

import board
import time
import math
import digitalio
import random
import simpleio
import adafruit_mcp4728
import neopixel

i2c = board.I2C()  # uses board.SCL and board.SDA
mcp4728 = adafruit_mcp4728.MCP4728(i2c)

pixel_pin = board.NEOPIXEL
num_pixels = 1

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=False)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 75, 0)
YELLOW = (255, 255, 0)
AQUA = (0, 255, 255)
PURPLE = (255, 0, 255)
PINK = (255, 0, 75)

colors = [PURPLE, BLUE, AQUA, GREEN, YELLOW, ORANGE, RED, PINK]

volts = [
    {'label': "c3", '1vOct': 0.000},
    #{'label': "d3", '1vOct': 0.167},
    {'label': "e3", '1vOct': 0.333},
    #{'label': "f3", '1vOct': 0.417},
    {'label': "g3", '1vOct': 0.583},
    #{'label': "a3", '1vOct': 0.750},
    {'label': "b3", '1vOct': 0.917},
    #{'label': "c4", '1vOct': 1.000},
    ]

pitches = []

def map_volts(n, volt, vref, bits):
    n = simpleio.map_range(volt, 0, vref, 0, bits)
    pitches.append(n)

for v in volts:
    map_volts(v['label'], v['1vOct'], 3.3, 4095)

print(pitches)

gate = digitalio.DigitalInOut(board.D5)
gate.direction = digitalio.Direction.INPUT
gate.pull = digitalio.Pull.UP

led = digitalio.DigitalInOut(board.D6)
led.direction = digitalio.Direction.OUTPUT

gate_state = False


v = 0
while True:
    if not gate.value and gate_state is False:
        gate_state = True
        led.value = True
    #for v in range(4):
        #v = random.randint(0, 7)

        mcp4728.channel_b.raw_value = int(pitches[v])
        pixels.fill(colors[v])
        pixels.show()
        print(mcp4728.channel_b.raw_value)
        v += 1
        if v > 3:
            v = 0
    if gate.value and gate_state is True:
        gate_state = False
        led.value = False
    #time.sleep(2)