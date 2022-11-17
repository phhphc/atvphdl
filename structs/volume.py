from structs.boot_sector import *
from structs.file_table import *


class Volume:
    boot_sector = BootSector
    file_table = FileTable

    def new(self, filename: str, volume_size: int) -> None:

        with open(filename, "wb") as f:
            print("new file")
            self.boot_sector = BootSector()
            self.boot_sector.new(volume_size)

            boot_sector_size = f.write(self.boot_sector.dump())
            reserved_byte = self.boot_sector.ReservedSectors * self.boot_sector.BytesPerSector

            f.write(b'\x00'*(reserved_byte - boot_sector_size))

            total_sector = self.boot_sector.TotalCluster * self.boot_sector.SectorsPerCluster
            for _ in range(total_sector - self.boot_sector.ReservedSectors):
                f.write(b'\x00'*self.boot_sector.BytesPerSector)

            bytes_per_fat = self.boot_sector.SectorsPerFat * self.boot_sector.BytesPerSector
            self.file_table = FileTable(f, reserved_byte, bytes_per_fat)
            self.file_table.format()
