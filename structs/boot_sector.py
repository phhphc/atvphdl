import math
from struct import unpack, pack


class BootSector:

    # 4 bytes
    MaggicCode = bytes
    # 4 bytes
    BytesPerSector = int
    # 4 bytes
    SectorsPerCluster = int
    # 4 bytes
    TotalCluster = int
    # 4 bytes
    ReservedSectors = int
    # 4 bytes
    SectorsPerFat = int
    # 490 bytes
    ReservedBytes = bytes
    # 2 bytes
    EndMarker = bytes

    def parse(self, buffer: bytes) -> None:
        (
            self.MaggicCode,
            self.BytesPerSector,
            self.SectorsPerCluster,
            self.TotalCluster,
            self.ReservedSectors,
            self.SectorsPerFat,
            self.ReservedBytes,
            self.EndMarker
        ) = unpack("=4sIIIII486s2s", buffer)

    def dump(self) -> bytes:
        return pack(
            "=4sIIIII486s2s",
            self.MaggicCode,
            self.BytesPerSector,
            self.SectorsPerCluster,
            self.TotalCluster,
            self.ReservedSectors,
            self.SectorsPerFat,
            self.ReservedBytes,
            self.EndMarker
        )

    def new(self, volume_size: int):
        
        self.MaggicCode = b'IDRS'
        self.BytesPerSector = 512
        self.SectorsPerCluster = 8
        self.ReservedSectors = 1

        byte_per_cluster = self.BytesPerSector * self.SectorsPerCluster
        volume_size = volume_size - (volume_size % byte_per_cluster)

        self.TotalCluster = volume_size // byte_per_cluster
        self.SectorsPerFat = math.ceil(
            self.TotalCluster * 4 / self.BytesPerSector)
        self.ReservedBytes = b'\x00'*486
        self.EndMarker = b'\x55\xAA'