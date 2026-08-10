import sys

from pio_bus import bus
from qbus import qbus
from board import ram
from board import uart

devs = bus.find_devices()

if len(devs) == 0:
    print("No USB device found")
    sys.exit(255)        

qbus = qbus.QBusDriver(devs[0])

data = qbus.readExtReg1()
res = "PASS" if (data & 0xFF00) == 0o160000 else "FAIL"
print("Start address register = %06o: %s" % (data, res))

# Регистр управления памятью должен запоминать биты 2 и 3
print("Memory control register test... ", end='')
ok = True
for i in range(0, 4):
    val = i << 2
    qbus.writeExtReg1(val)
    data = qbus.readExtReg1()
    if (data & 0xFF0C) != 0o160000 | val:
        if ok:
            print("FAIL")
        print("ERROR: wrote %06o, read %06o" % (val, data))
        ok = False
if ok:
    print("PASS")

ram_test = ram.RAMTester(qbus)

# Системное ОЗУ обязательно должно присутствовать и работать
print("System memory test...")
ram_test.test_range(0o177600, 0o177700)

# Границы системного ОЗУ.
# С адреса 0o177700 располагается встроенный периферийный блок ЦП, но во время выполнения тестов
# процессор должен быть отключен, поэтому он не ответит.
print("System memory boundary test... ", end='')
lower = qbus.readWord(0o177576)
upper = qbus.readWord(0o177700)
if lower is None and upper is None:
    print("PASS")
else:
    print("Lower boundary", "OK" if lower is None else "FAIL", ", upper boundary", "OK" if upper is None else "FAIL")

print("UART test... ", end='')
uart = uart.UART(qbus, 0o177560)
res = uart.putstr("HELLORLD\r\n")
if res:
    print("PASS")
print("Done!")
