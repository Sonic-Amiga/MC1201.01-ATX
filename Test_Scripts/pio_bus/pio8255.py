PORTA = 0x00
PORTB = 0x08
PORTC = 0x10
MODE = 0x18

IN  = 1
OUT = 0

def IOMODE(ma, mb, pa, pb, pcl, pch):
    return 0x80 | (ma << 5) | (pa << 4) | (pch << 3) | (mb << 2) | (pb << 1) | pch
