all: Test_ROM.hex

Test_ROM.obj: Test_ROM.mac
	macro11 -o $@ $^

Test_ROM.bin: Test_ROM.obj
	obj2bin.pl --raw --rt11 --memsize 0174000 --outfile $@ $^

Test_ROM.rom: Test_ROM.bin
	rev16.py -E -x $< -b $@

Test_ROM.hex: Test_ROM.rom Test_ROM.cat
	srec_cat @Test_ROM.cat

.PHONY: release
release: Test_ROM.hex
	cp -vf $@ ../ROM_Images/
	

clean:
	rm -f *.obj *.bin *.rom *.hex
