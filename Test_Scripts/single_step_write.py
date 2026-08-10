import sys

from pio_bus import bus
from qbus import qbus

if len(sys.argv) < 3:
    print("Usage: %s <address> <value>" % (sys.argv[0]))
    sys.exit(0)

addr = int(sys.argv[1], 0)
data = int(sys.argv[2], 0)

devs = bus.find_devices()

if len(devs) == 0:
    print("No USB device found")
    sys.exit(255)

qbus = qbus.QBusDriver(devs[0])

while True:
    qbus.latch(addr)
    input("SYNC")
    qbus.dout(data)
    input("WRITE")
    qbus.release()
    input("RELEASE")
