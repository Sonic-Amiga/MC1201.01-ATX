import sys

from pio_bus import bus
from qbus import qbus

if len(sys.argv) < 3:
    print("Usage: %s <start address> <end address>" % (sys.argv[0]))
    sys.exit(0)

start = int(sys.argv[1], 0)
end = int(sys.argv[2], 0)
if end <= start:
    print("Invalid addresses given!")
    sys.exit(255)

devs = bus.find_devices()

if len(devs) == 0:
    print("No USB device found")
    sys.exit(255)        

qbus = qbus.QBusDriver(devs[0])

class RAMTester:
    def __init__(self, qbus):
        self.qbus = qbus

    def err(self, text):
        if self.last_ok:
            print()
        print("ERROR:", text)
        self.last_ok = False
        self.good = False

    def test_addr(self, addr, value):
        ok = self.qbus.writeWord(addr, value)
        if not ok:
            self.err("No reply writing 0x%04X at address %06o" % (value, addr))
            return False
        readback = self.qbus.readWord(addr)
        if readback is None:
            self.err("No reply reading address %06o" % (value, addr))
            return False
        mask = readback ^ value
        if mask == 0:
            return True
        self.err("Address %06o: expected 0x%04X, got 0x%04X, mask 0x%04X" % (addr, value, readback, mask))
        return False

    def test_range(self, start, end):
        self.good = True
        self.last_ok = False
        for addr in range(start, end):
            if self.test_addr(addr, 0x0000) and \
               self.test_addr(addr, 0x55AA) and \
               self.test_addr(addr, 0xAA55):
                print(".", end='', flush=True)
                self.last_ok = True
        print("PASS" if self.good else "FAIL")

RAMTester(qbus).test_range(start, end)

print("Done!")
