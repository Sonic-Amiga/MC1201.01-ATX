import sys

from pio_bus import bus
from qbus import qbus

devs = bus.find_devices()

if len(devs) == 0:
    print("No USB device found")
    sys.exit(255)

qbus = qbus.QBusDriver(devs[0])

while True:
    data = qbus.readSel1()
    input("SEL, data = %06o" % (data))
    qbus.release()
    input("RELEASE")
