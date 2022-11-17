from structs.boot_sector import BootSector

boot_sector = BootSector()
boot_sector.new(100_000_000)

buffer = boot_sector.dump()

boot_sector2 = BootSector()
boot_sector2.parse(buffer)


# print(boot_sector.BytesPerSector)
# print(boot_sector.SectorsPerCluster)
print(boot_sector.ReservedBytes)
# print(boot_sector.SectorsPerFat)
# print(boot_sector.ReservedSectors)
# print(boot_sector.EndMarker)

# print(buffer)

# print(boot_sector2.BytesPerSector)
# print(boot_sector2.SectorsPerCluster)
print(boot_sector2.ReservedBytes)
# print(boot_sector2.SectorsPerFat)
# print(boot_sector2.ReservedSectors)
# print(boot_sector2.EndMarker)

assert len(buffer) == 512
assert buffer[-2:] == b'\x55\xAA'

assert boot_sector.MaggicCode == boot_sector2.MaggicCode
assert boot_sector.BytesPerSector == boot_sector2.BytesPerSector
assert boot_sector.SectorsPerCluster == boot_sector2.SectorsPerCluster
assert boot_sector.TotalCluster == boot_sector2.TotalCluster
assert boot_sector.ReservedSectors == boot_sector2.ReservedSectors
assert boot_sector.SectorsPerFat == boot_sector2.SectorsPerFat
assert boot_sector.EndMarker == boot_sector2.EndMarker
assert boot_sector.ReservedBytes == boot_sector2.ReservedBytes
