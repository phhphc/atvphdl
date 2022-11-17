
class Data:

    def __init__(self, f, offset: int, size: int, bytes_per_sector: int, sectors_per_cluster: int):
        self.io = f
        self.offset = offset 
        self.size = size 
        self.bytes_per_sector = bytes_per_sector
        self.sectors_per_cluster = sectors_per_cluster

    def ahnfw()
