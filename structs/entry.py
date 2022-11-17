from struct import unpack, pack


class Entry:
    # 1 bytes
    IsUsed: bytes
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

    def new(self, IsUsed: bytes, Name: bytes, Attributes: bytes, FirstCluster: int, Nonce: bytes, ContentSize: int) -> None:
        self.isUsed = IsUsed
        self.Name = Name
        self.Attributes = Attributes
        self.FirstCluster = FirstCluster
        self.Nonce = Nonce
        self.ContentSize = ContentSize

        # Create new entry

    def dump(self) -> bytes:
        return pack(
            "=1s38s1sI16sI",
            self.IsUsed,
            self.Name,
            self.Attributes,
            self.FirstCluster,
            self.Nonce,
            self.ContentSize
        )
        # export entry data into 64 bytes

    def parse(self, buffer) -> None:
        (
            self.IsUsed,
            self.Name,
            self.Attributes,
            self.FirstCluster,
            self.Nonce,
            self.ContentSize
        ) = unpack("=1s38s1sI16sI", buffer)
        # parse 64 bytes input to entry data

# Entry size 64 bytes
