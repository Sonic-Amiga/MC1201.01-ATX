all: REmulator_wcload.hex

REmulator_ALL.hex: Remulator_ALL.cat 000_mc1201.rom 012_mc1201.rom 013_mc1201.rom 031_mc1201.rom 054_mc1201.rom
	srec_cat @$<

REmulator_wcload.hex: REmulator_wcload.cat a205.hex REmulator_ALL.hex
	srec_cat @$<
