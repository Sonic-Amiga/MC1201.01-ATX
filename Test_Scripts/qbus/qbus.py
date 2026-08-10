from pio_bus import pio8255 as ppa
from time import sleep

SYNC = 1 << 0
DIN  = 1 << 1
DOUT = 1 << 2
SEL1 = 1 << 3

# 8255Bus port assignment:
# A0 - AD7...AD0
# A1 - AD15...AD8
# A2 - output control signals:
#      bit0 - /SYNC
#      bit1 - /DIN
#      bit2 - /DOUT
#      bit3 - /SEL1
# C0 - input control signals:
#    bit 0 - /RPLY

class BusError(Exception):
    pass

class QBusDriver:
    def __init__(self, pio):
        self.pio = pio
        p0_mode = ppa.IOMODE(0, 0, ppa.IN, ppa.OUT, ppa.IN, ppa.IN)
        p2_mode = ppa.IOMODE(0, 0, ppa.OUT, ppa.IN, ppa.IN, ppa.IN)
        self.pio.write(ppa.MODE, [p0_mode, p0_mode, p2_mode])
        self.current_dir = ppa.IN
        self.release()

    def dir(self, d):
        if d == self.current_dir:
            return
        # We only change direction of ports A0 and A1
        p0_mode = ppa.IOMODE(0, 0, d, ppa.OUT, ppa.IN, ppa.IN)
        self.pio.write(ppa.MODE, [p0_mode, p0_mode])
        self.current_dir = d

    def control(self, v):
        # Our value is inverted for simplicity
        self.pio.writeByte(ppa.PORTA + 2, v ^ 0xFF)

    def getRPLY(self):
        return self.pio.readByte(ppa.PORTC) & 1

    def waitRPLY(self, state):
        timeout = 5
        while self.getRPLY() != state:
            timeout = timeout - 1
            if timeout == 0:
                return False
        return True

    def latch(self, addr):
        if not self.waitRPLY(1):
            raise BusError("Bus is not free in the beginning of transaction")
        self.dir(ppa.OUT)
        self.pio.writeWord(ppa.PORTA, addr ^ 0xFFFF)
        self.control(SYNC)

    def din(self):
        self.dir(ppa.IN)
        self.control(SYNC | DIN)

    def dout(self, data):
        self.pio.writeWord(ppa.PORTA, data ^ 0xFFFF)
        self.control(SYNC | DOUT)

    def readSel1(self):
        self.dir(ppa.IN)
        self.control(DIN | SEL1)
        return self.pio.readWord(ppa.PORTA) ^ 0xFFFF

    def writeSel1(self, val):
        self.dir(ppa.OUT)
        self.pio.writeWord(ppa.PORTA, val ^ 0xFFFF)
        self.control(DOUT | SEL1)

    def release(self):
        self.control(0) # Release the bus
        self.dir(ppa.IN)

    def read(self):
        if not self.waitRPLY(0):
            return None
        return self.pio.readWord(ppa.PORTA) ^ 0xFFFF

    # Complete read word cycle
    def readWord(self, addr):
        self.latch(addr)
        self.din()
        data = self.read()
        self.release()
        return data

    # Complete write word cycle
    def writeWord(self, addr, data):
        self.latch(addr)
        self.dout(data)
        res = self.waitRPLY(0)
        self.release()
        return res

    def readExtReg1(self):
        data = self.readSel1()
        self.release()
        return data

    def writeExtReg1(self, val):
        self.writeSel1(val)
        self.release()
