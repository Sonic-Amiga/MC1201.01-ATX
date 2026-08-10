import sys

from pio_bus import bus
from qbus import qbus

if len(sys.argv) < 3:
    print("Usage: %s <.rom file> <start address> [end address]" % (sys.argv[0]))
    print("If end address is not given, assuming full 8K size")
    sys.exit(0)

data = []
with open(sys.argv[1], "rb") as f:
    data = f.read()

start = int(sys.argv[2], 0)
if len(sys.argv) > 2:
    end = int(sys.argv[3], 0)
    if end <= start:
        print("Invalid addresses given!")
        sys.exit(255)
else:
    end = start + 8192

devs = bus.find_devices()

if len(devs) == 0:
    print("No USB device found")
    sys.exit(255)

qbus = qbus.QBusDriver(devs[0])

# If we are connected to the main board, enable full ROM window
qbus.writeExtReg1(0x0C)

ok = True
last_ok = True
for addr in range(start, end, 2):
    value = qbus.readWord(addr)
    if value is None:
        if last_ok:
            print()
        print("Error at offset %06o: no reply" % (addr))
        ok = False
        last_ok = False
        continue
    # .rom file contains raw data, i. e. addresses and data inverted.
    # Invert what we read in order to make comparison and diagnosis easier
    value = value ^ 0xFFFF
    # We also have to read the file in reverse order starting from the last word
    # (offset 8190)
    file_pos = 8190 - (addr - start)
    expect = ((data[file_pos + 1] << 8) | data[file_pos])
    mask = value ^ expect
    if value != expect:
        if last_ok:
            print()
        print("Error at offset %06o: expected 0x%04X, got 0x%04X, mask 0x%04X" % (addr, expect, value, mask))
        ok = False
    else:
        print(".", end='', flush=True)
        last_ok = True
print("PASS" if ok else "FAIL")
