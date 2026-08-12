all: Test_ROM.hex

Test_ROM.OBJ: Test_ROM.mac
	macro11 -o $@ $^
	
Test_ROM.bin: Test_ROM.obj
	obj2bin.pl --raw --rt11 --outfile $@ $^

Test_ROM.rom: Test_ROM.bin
	rev16.py -E -x $< -b $@

Test_ROM.hex: Test_ROM.rom Test_ROM.cat
	srec_cat @Test_ROM.cat
