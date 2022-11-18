
class Data:

    def __init__(self, f, offset: int, size: int, bytes_per_sector: int, sectors_per_cluster: int):
        self.io = f
        self.offset = offset 
        self.size = size 
        self.bytes_per_sector = bytes_per_sector
        self.sectors_per_cluster = sectors_per_cluster

        self.bytes_per_cluster = self.bytes_per_sector*self.sectors_per_cluster

    def read_sector(self, cluster: int, sector: int):
        total_offset = self.offset + cluster*self.bytes_per_cluster + sector*self.bytes_per_sector
        self.io.seek(total_offset)

        buffer = self.io.read(self.bytes_per_sector)
        return buffer

    def write_sector(self, cluster: int, sector: int, buffer: bytes):
        total_offset = self.offset + cluster*self.bytes_per_cluster + sector*self.bytes_per_sector
        self.io.seek(total_offset)

        if (len(buffer) > self.bytes_per_sector):
            raise BufferError("size of buffer must smaller or equal %d"%self.bytes_per_sector)
        if (len(buffer) < self.bytes_per_sector):
            buffer = buffer + b'\x00'*(self.bytes_per_sector - len(buffer))

        self.io.write(buffer)

