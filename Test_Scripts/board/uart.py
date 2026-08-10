class UART:
    TX_STATUS_DONE = 1 << 7

    def __init__(self, qbus, addr):
        self.qbus = qbus
        self.base = addr
	
    def putchar(self, c):
        txs = 0
        while txs & UART.TX_STATUS_DONE == 0:
            txs = self.qbus.readWord(self.base + 4)
            if txs is None:
                print("FAIL: Unable to read tx status")
                return False
        res = self.qbus.writeWord(self.base + 6, ord(c))
        if not res:
            print("FAIL: Unable to write data")
        return res

    def putstr(self, s):
        for c in s:
            if not self.putchar(c):
                return False
        return True
