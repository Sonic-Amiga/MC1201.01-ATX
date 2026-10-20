# My TL866 doesn't support 4067, let's make our own quick-n-dirty solution.

import sys

from pio_bus import bus
from pio_bus import pio8255 as ppa

devs = bus.find_devices()

if len(devs) == 0:
    print("No USB device found")
    sys.exit(255)

pio = devs[0]

# 8255Bus port assignment:
# A0 - I0...I7
# A1 - I8...I15
# B0 bits 0...3 - S0...S3
# B0 bit 4 - /EN
# C0 bit 0 - COM with 2.2K pull-up to +5V

p_mode = ppa.IOMODE(0, 0, ppa.OUT, ppa.OUT, ppa.IN, ppa.IN)
pio.write(ppa.MODE, [p_mode, p_mode])

fails = 0

def do_test(en):
    global fails
    for sel in range(0, 16):
        pio.writeByte(ppa.PORTB, (en << 4) | sel)
        for bit in range(0, 16):
            inputs = (1 << bit) ^ 0xFFFF
            pio.writeWord(ppa.PORTA, inputs)
            out = pio.readByte(ppa.PORTC) & 1
            expect = 0 if en == 0 and bit == sel else 1
            if out == expect:
                res = "OK"
            else:
                res = "FAIL"
                fails = fails + 1
            print("EN", en, "SEL", sel, "BIT", bit, "RESULT", out, res)

do_test(0)
do_test(1)

if fails == 0:
    print("PASS")
else:
    print("FAIL", fails, "tests")
