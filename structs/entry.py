from struct import unpack, pack
from enum import Enum

class Attributes:
    EMPTY = b'\x00'
    FILE = b'\x01'
    FOLDER = b'\x02'

class Entry:

    ENTRY_SIZE = 64

    # n bytes
    Name: bytes
    # 1
    Attributes: bytes
    #  4 little endian
    FirstCluster: int
    # 8 bytes use for AES CTR
    Nonce: bytes
    # 4 bytes
    ContentSize: int

    def new(self, Name: bytes, Attributes: bytes, FirstCluster: int, ContentSize: int) -> None:
        self.Name = Name
        self.Attributes = Attributes
        self.FirstCluster = FirstCluster
        self.Nonce = b'\x00'*8
        self.ContentSize = ContentSize

        # Create new entry

    def dump(self) -> bytes:
        return pack(
            "=47s1sI8sI",
            self.Name,
            self.Attributes,
            self.FirstCluster,
            self.Nonce,
            self.ContentSize
        )
        # export entry data into 64 bytes


    def set_position(self, cluster:int, sector:int, offset:int):
        self.cluster = cluster
        self.sector = sector
        self.offset = offset

    def get_position(self):
        if self.cluster == None or self.sector==None or self.offset ==None:
            return None
        return (self.cluster, self.sector, self.offset)

    def parse(self, buffer) -> None:
        (
            self.Name,
            self.Attributes,
            self.FirstCluster,
            self.Nonce,
            self.ContentSize
        ) = unpack("=47s1sI8sI", buffer)
        # parse 64 bytes input to entry data

# Entry size 64 bytes
