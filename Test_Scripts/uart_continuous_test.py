import sys

from pio_bus import bus
from qbus import qbus
from board import uart

devs = bus.find_devices()

if len(devs) == 0:
    print("No USB device found")
    sys.exit(255)        

qbus = qbus.QBusDriver(devs[0])

uart = uart.UART(qbus, 0o177560)
res = True
while res:
    res = uart.putchar('A')
