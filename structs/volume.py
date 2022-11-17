from structs.boot_sector import *
from structs.file_table import *
from structs.entry import *
from structs.data import *


class Volume:
    boot_sector = BootSector
    file_table = FileTable

    def __del__(self):
        self.io.close()

    def new(self, filename: str, volume_size: int) -> None:
        f = open(filename, "w+b")
        self.io = f

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
        self.file_table = FileTable(
            f, reserved_byte, bytes_per_fat, self.boot_sector.BytesPerSector)
        self.file_table.format()

        data_offset = reserved_byte + bytes_per_fat
        data_size = total_sector * self.BytesPerSector - data_offset
        self.data = Data(
            f, data_offset, data_size, self.boot_sector.BytesPerSector, self.boot_sector.SectorsPerCluster
        )



    def import_file(self, filename) -> None:
        # get empty cluster
        empty_cluster = next(self.file_table.empty_cluster())

        # create new entry
        entry = Entry()
        file_size = 123
        entry.new(filename, Attributes.FILE, empty_cluster, file_size)

        # save entry root folder
        entry.dump()

        # copy content to cluster
        pass
        # toi offset cua file cluster
        # copy noi dung file vo
