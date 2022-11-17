from structs.entry import *
from structs.sector import *

class Data:

    def __init__(self, f, offset: int, size: int, bytes_per_sector: int, sectors_per_cluster: int):
        self.io = f
        self.offset = offset 
        self.size = size 
        self.bytes_per_sector = bytes_per_sector
        self.sectors_per_cluster = sectors_per_cluster
        self.sectorList = []
        for i in range (0, int(size / bytes_per_sector)):
            sector = Sector(bytes_per_sector)
            self.sectorList.append(sector)
    
    def getSector(self, i):
        return self.sectorList[i/self.bytes_per_sector]


