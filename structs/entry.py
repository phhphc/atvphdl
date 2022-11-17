from struct import unpack, pack
from enum import Enum

class Attributes(Enum):
    EMPTY = b'\x00'
    FILE = b'\x01'
    FOLDER = b'\x02'

class Entry:
    # n bytes
    Name: bytes
    # 1
    Attributes: bytes
    #  4 little endian
    FirstCluster: int
    # 16 bytes use for AES CTR
    Nonce: bytes
    # 4 bytes
    ContentSize: int

    def get_content():
        pass
        # TODO: get file content

    def new(self, Name: bytes, Attributes: bytes, FirstCluster: int, ContentSize: int) -> None:
        self.Name = Name
        self.Attributes = Attributes
        self.FirstCluster = FirstCluster
        self.Nonce = b'\x00'*16
        self.ContentSize = ContentSize

        # Create new entry

    def dump(self) -> bytes:
        return pack(
            "=39s1sI16sI",
            self.Name,
            self.Attributes,
            self.FirstCluster,
            self.Nonce,
            self.ContentSize
        )
        # export entry data into 64 bytes

    def parse(self, buffer) -> None:
        (
            self.Name,
            self.Attributes,
            self.FirstCluster,
            self.Nonce,
            self.ContentSize
        ) = unpack("=39s1sI16sI", buffer)
        # parse 64 bytes input to entry data

# Entry size 64 bytes
