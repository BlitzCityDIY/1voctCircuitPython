import asyncio
import board
import digitalio
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
    #{'label': "b3", '1vOct': 0.917},
    {'label': "c4", '1vOct': 1.000},
    ]

pitches = []

def map_volts(n, volt, vref, bits):
    n = simpleio.map_range(volt, 0, vref, 0, bits)
    pitches.append(n)
    
for v in volts:
    map_volts(v['label'], v['1vOct'], 3.3, 4095)

print(pitches)

chord = []

chord.append(pitches[0])
chord.append(pitches[2])
chord.append(pitches[4])
chord.append(pitches[6])

async def scale(interval):
    for v in range(7):
        mcp4728.channel_b.raw_value = int(pitches[v])
        await asyncio.sleep(interval)  # Don't forget the "await"!
        print("note")

async def triad(interval):
    for v in range(4):
        mcp4728.channel_a.raw_value = int(chord[v])
        await asyncio.sleep(interval)  # Don't forget the "await"!
        print("chord")


async def main():
    scale_task = asyncio.create_task(scale(1.5))
    triad_task = asyncio.create_task(triad(3))

    await asyncio.gather(scale_task, triad_task)  # Don't forget "await"!
    print("done")

while True:
    asyncio.run(main())
