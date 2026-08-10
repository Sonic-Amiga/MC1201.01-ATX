import sys

from pio_bus import bus
from qbus import qbus

if len(sys.argv) < 2:
    print("Usage: {} [address]".format(sys.argv[0]))
    sys.exit(0)

addr = int(sys.argv[1], 0)

devs = bus.find_devices()

if len(devs) == 0:
    print("No USB device found")
    sys.exit(255)

qbus = qbus.QBusDriver(devs[0])

while True:
    qbus.latch(addr)
    input("SEL")
    qbus.din()
    input("DIN")
    v = qbus.read()
    if v is None:
        input("READ: NO REPLY")
    else:
        input("READ: {}".format(hex(v)))
    qbus.release()
    input("RELEASE")
