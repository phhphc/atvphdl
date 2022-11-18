


class FileTable:
    END_INDEX = 0xffffffff
    ROOT_DIR_FIRST_CLUSTER = 0x00000000
    DELE_DIR_FIRST_CLUSTER = 0x00000001
    EMPTY_CLUSTER_HEAD = 0x00000002

    def __init__(self, f, offset: int, size: int, bytes_per_sector: int):
        self.io = f
        self.offset = offset
        self.size = size
        self.bytes_per_sector = bytes_per_sector

    def cluster_list():
        pass
        # TODO: get cluster list of a file

    def empty_cluster(self):
        val = self.read_index(FileTable.EMPTY_CLUSTER_HEAD)
        if val == FileTable.END_INDEX:
            return

        self.update_index(FileTable.EMPTY_CLUSTER_HEAD, self.read_index(val))
        self.update_index(val, FileTable.END_INDEX)
        yield val
    
    def append_cluster_list(self, pre_cluster:int):
        if self.read_index(pre_cluster) != FileTable.END_INDEX:
            raise IndexError("pre_cluster index must be END_INDEX")
        
        new_cluster = next(self.empty_cluster())
        self.update_index(pre_cluster, new_cluster)
        return new_cluster

    def format(self):
        self.io.seek(self.offset)
        self.io.write(FileTable.END_INDEX.to_bytes(4, 'little') * 2)

        for i in range(3, self.size // 4):
            self.io.write(i.to_bytes(4, 'little'))

        self.io.write(FileTable.END_INDEX.to_bytes(4, 'little'))

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
