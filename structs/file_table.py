
END_INDEX = 0xffffffff


class FileTable:

    def __init__(self, f, offset: int, size: int, bytes_per_sector: int):
        self.io = f
        self.offset = offset
        self.size = size
        self.bytes_per_sector = bytes_per_sector

    def cluster_list():
        pass
        # TODO: get cluster list of a file

    def empty_cluster(self):
        val = self.read_index(3)
        if val == END_INDEX:
            return

        self.update_index(3, self.read_index(val))
        self.update_index(val, END_INDEX)
        yield val

    def format(self):
        self.io.seek(self.offset)
        self.io.write(END_INDEX.to_bytes(4, 'little') * 2)

        for i in range(3, self.size // 4):
            self.io.write(i.to_bytes(4, 'little'))

        self.io.write(END_INDEX.to_bytes(4, 'little'))

    def read_index(self, index: int) -> int:
        index = index*4
        cluster = index // self.bytes_per_sector
        offset = index % self.bytes_per_sector

        self.io.seek(self.offset + cluster*self.bytes_per_sector)
        buffer = self.io.read(self.bytes_per_sector)

        return int.from_bytes(buffer[offset:offset+4], 'little')

    def update_index(self, index: int, value: int) -> None:
        index = index*4
        cluster = index // self.bytes_per_sector
        offset = index % self.bytes_per_sector

        self.io.seek(self.offset + cluster*self.bytes_per_sector)
        buffer = self.io.read(self.bytes_per_sector)

        buffer = buffer[:offset] + \
            value.to_bytes(4, 'little') + buffer[offset+4:]

        self.io.seek(self.offset + cluster*self.bytes_per_sector)
        self.io.write(buffer)
