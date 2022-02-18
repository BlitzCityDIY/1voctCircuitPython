# SPDX-FileCopyrightText: 2022 BlitzCityDIY
# SPDX-License-Identifier: MIT

import board
import time
import math
import simpleio
import adafruit_mcp4728

i2c = board.I2C()  # uses board.SCL and board.SDA
mcp4728 = adafruit_mcp4728.MCP4728(i2c)

volts = [
    {'label': "c3", '1vOct': 0.000},
    {'label': "d3", '1vOct': 0.167},
    {'label': "e3", '1vOct': 0.333},
    {'label': "f3", '1vOct': 0.417},
    {'label': "g3", '1vOct': 0.583},
    {'label': "a3", '1vOct': 0.750},
    {'label': "b3", '1vOct': 0.917},
    {'label': "c4", '1vOct': 1.000},
    ]

pitches = []

def map_volts(n, volt, vref, bits):
    n = simpleio.map_range(volt, 0, vref, 0, bits)
    pitches.append(n)
    
for v in volts:
    map_volts(v['label'], v['1vOct'], 3.3, 4095)

print(pitches)

while True:
    for v in range(8):
        mcp4728.channel_b.raw_value = int(pitches[v])
        print(v)
        time.sleep(2)