from structs.entry import *

class Sector:

    def __init__(self, bytes_per_sector: int):
        self.bytes_per_sector = bytes_per_sector
        self.entryList = []
        for i in range (0, int(bytes_per_sector / 64)):
            entry = Entry()
            self.entryList.append(entry.new('',Attributes.EMPTY,0,0))
    
    def getEntry(self, i):
        return self.entryList[i]

    def setEntry(self, i ,newEntry):
        self.entryList[i/64] = newEntry

