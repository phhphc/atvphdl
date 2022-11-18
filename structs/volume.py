from structs.boot_sector import *
from structs.file_table import *
from structs.entry import *
from structs.data import *

import os
from hashlib import sha256
from Crypto.Cipher import AES

class Volume:
    boot_sector = BootSector
    file_table = FileTable


    def __del__(self):
        self.io.close()

    def open(self, filename: str) -> None:
        f = open(filename, "r+b")
        self.io = f

        self.boot_sector = BootSector()
        self.boot_sector.parse(f.read(0x200))

        reserved_byte = self.boot_sector.ReservedSectors * self.boot_sector.BytesPerSector

        total_sector = self.boot_sector.TotalCluster * self.boot_sector.SectorsPerCluster

        bytes_per_fat = self.boot_sector.SectorsPerFat * self.boot_sector.BytesPerSector
        self.file_table = FileTable(
            f, reserved_byte, bytes_per_fat, self.boot_sector.BytesPerSector)

        data_offset = reserved_byte + bytes_per_fat
        data_size = total_sector * self.boot_sector.BytesPerSector - data_offset
        self.data = Data(
            f, data_offset, data_size, self.boot_sector.BytesPerSector, self.boot_sector.SectorsPerCluster
        )

        self.entry_per_sector = self.boot_sector.BytesPerSector // Entry.ENTRY_SIZE
        self.bytes_per_cluster = self.boot_sector.BytesPerSector * self.boot_sector.SectorsPerCluster


    def new(self, filename: str, volume_size: int) -> None:
        f = open(filename, "w+b")
        self.io = f

        self.boot_sector = BootSector()
        self.boot_sector.new(volume_size)

        boot_sector_size = f.write(self.boot_sector.dump())
        reserved_byte = self.boot_sector.ReservedSectors * self.boot_sector.BytesPerSector
        f.write(b'\x00'*(reserved_byte - boot_sector_size))

        total_sector = self.boot_sector.TotalCluster * self.boot_sector.SectorsPerCluster
        for _ in range(total_sector - self.boot_sector.ReservedSectors):
            f.write(b'\x00'*self.boot_sector.BytesPerSector)

        bytes_per_fat = self.boot_sector.SectorsPerFat * self.boot_sector.BytesPerSector
        self.file_table = FileTable(
            f, reserved_byte, bytes_per_fat, self.boot_sector.BytesPerSector)
        self.file_table.format()

        data_offset = reserved_byte + bytes_per_fat
        data_size = total_sector * self.boot_sector.BytesPerSector - data_offset
        self.data = Data(
            f, data_offset, data_size, self.boot_sector.BytesPerSector, self.boot_sector.SectorsPerCluster
        )

        self.entry_per_sector = self.boot_sector.BytesPerSector // Entry.ENTRY_SIZE
        self.bytes_per_cluster = self.boot_sector.BytesPerSector * self.boot_sector.SectorsPerCluster


    def list_entry(self, first_cluster)-> list[Entry]:
        cluster = first_cluster
        entries = []

        while cluster!= FileTable.END_INDEX:
            for sector in range(self.boot_sector.SectorsPerCluster):
                buffer = self.data.read_sector(cluster, sector)
                offset = 0
                while len(buffer) > 0:
                    tmp_entry = Entry()
                    tmp_entry.parse(buffer[:Entry.ENTRY_SIZE])
                    if tmp_entry.Attributes != Attributes.EMPTY:
                        tmp_entry.set_position(cluster, sector, offset)
                        entries.append(tmp_entry)
                    buffer = buffer[Entry.ENTRY_SIZE:]
                    offset = offset + Entry.ENTRY_SIZE
            cluster = self.file_table.read_index(cluster)

        return entries


    def encrypt_entry(self, entry: Entry, password: str):
        if entry.Nonce != b'\x00'*8:
            raise AttributeError("entry must not be encrypt")

        position = entry.get_position()
        assert position!=None
        
        entry.Nonce = os.urandom(8)
        key = sha256(password.encode()).digest()
        cipher = AES.new(key, AES.MODE_CTR, nonce=entry.Nonce)

        cluster = entry.FirstCluster
        size = entry.ContentSize
        while True:
            for sector in range(self.boot_sector.SectorsPerCluster):
                buffer = self.data.read_sector(cluster, sector)
                if size < self.boot_sector.BytesPerSector:
                    buffer = buffer[:size]
                
                buffer = cipher.encrypt(buffer)
                self.data.write_sector(cluster, sector, buffer)

                size = size - self.boot_sector.BytesPerSector
                if size <= 0:
                    break

            if size <= 0:
                    break
            cluster = self.file_table.read_index(cluster)

        cluster, sector, offset = position
        buffer = self.data.read_sector(cluster, sector)
        buffer = buffer[:offset] + entry.dump() + buffer[offset + Entry.ENTRY_SIZE:]
        self.data.write_sector(cluster,sector,buffer)


    def decrypt_entry(self, entry: Entry, password: str):
        if entry.Nonce == b'\x00'*8:
            raise AttributeError("entry is not encrypted")

        position = entry.get_position()
        assert position!=None
        
        key = sha256(password.encode()).digest()
        cipher = AES.new(key, AES.MODE_CTR, nonce=entry.Nonce)

        cluster = entry.FirstCluster
        size = entry.ContentSize
        while True:
            for sector in range(self.boot_sector.SectorsPerCluster):
                buffer = self.data.read_sector(cluster, sector)
                if size < self.boot_sector.BytesPerSector:
                    buffer = buffer[:size]
                
                buffer = cipher.decrypt(buffer)
                self.data.write_sector(cluster, sector, buffer)

                size = size - self.boot_sector.BytesPerSector
                if size <= 0:
                    break

            if size <= 0:
                    break
            cluster = self.file_table.read_index(cluster)

        entry.Nonce = b'\x00'*8
        cluster, sector, offset = position
        buffer = self.data.read_sector(cluster, sector)
        buffer = buffer[:offset] + entry.dump() + buffer[offset + Entry.ENTRY_SIZE:]
        self.data.write_sector(cluster,sector,buffer)  


    def delete_entry(self, entry: Entry):
        position = entry.get_position()
        assert position != None
        cluster, sector, offset = position
        buffer = self.data.read_sector(cluster, sector)
        buffer = buffer[:offset] + b'\x00'*Entry.ENTRY_SIZE + buffer[offset+Entry.ENTRY_SIZE:]
        self.data.write_sector(cluster, sector, buffer)

        self.save_entry_to_dir_cluster(FileTable.DELE_DIR_FIRST_CLUSTER, entry)


    def recover_entry(self, entry: Entry):
        position = entry.get_position()
        assert position != None
        cluster, sector, offset = position
        buffer = self.data.read_sector(cluster, sector)
        buffer = buffer[:offset] + b'\x00'*Entry.ENTRY_SIZE + buffer[offset+Entry.ENTRY_SIZE:]
        self.data.write_sector(cluster, sector, buffer)

        self.save_entry_to_dir_cluster(FileTable.ROOT_DIR_FIRST_CLUSTER, entry)


    def import_file(self, filename: str) -> None:
        with open(filename, "rb") as fin:
            fin.seek(0, os.SEEK_END)
            file_size = fin.tell()

            entry = Entry()
            new_cluster = next(self.file_table.empty_cluster())
            entry.new(filename.encode(), Attributes.FILE, new_cluster, file_size)

            self.save_entry_to_dir_cluster(FileTable.ROOT_DIR_FIRST_CLUSTER, entry)

            fin.seek(0)
            while True:
                for sector in range(self.boot_sector.SectorsPerCluster):
                    content = fin.read(self.boot_sector.BytesPerSector)
                    self.data.write_sector(new_cluster, sector, content)
                    
                    file_size = file_size - self.boot_sector.BytesPerSector
                    if file_size <= 0:
                        return

                new_cluster = self.file_table.append_cluster_list(new_cluster)


    def export_file(self, entry:Entry, filename:str="")-> None:
        if entry.Nonce != b'\x00'*8:
            print("file is encrypted !")
            return

        if filename=="":
            filename = entry.Name.strip(b"\x00").decode()

        cluster = entry.FirstCluster
        size = entry.ContentSize
        with open(filename, "wb") as fout:
            while True:
                for sector in range(self.boot_sector.SectorsPerCluster):
                    buffer = self.data.read_sector(cluster, sector)
                    if size < self.boot_sector.BytesPerSector:
                        buffer = buffer[:size]
                    fout.write(buffer)

                    size = size - self.boot_sector.BytesPerSector
                    if size <= 0:
                        return
                cluster = self.file_table.read_index(cluster)


    def get_content(self, entry:Entry):
        if entry.Nonce != b'\x00'*8:
            print("file is encrypted !")
            return

        cluster = entry.FirstCluster
        size = entry.ContentSize

        while True:
            for sector in range(self.boot_sector.SectorsPerCluster):
                buffer = self.data.read_sector(cluster, sector)
                if size < self.boot_sector.BytesPerSector:
                    buffer = buffer[:size]
                
                yield buffer
                size = size - self.boot_sector.BytesPerSector
                if size <= 0:
                    return

            cluster = self.file_table.read_index(cluster)


    def save_entry_to_dir_cluster(self, first_dir_cluster: int, entry: Entry):
        dir_cluster = first_dir_cluster
        while True:
            for sector in range(self.boot_sector.SectorsPerCluster):
                buffer = self.data.read_sector(dir_cluster, sector)
                
                for entry_num in range(self.entry_per_sector):
                    offset = entry_num*Entry.ENTRY_SIZE
                    tmp_entry = Entry()
                    tmp_entry.parse(buffer[offset:offset+Entry.ENTRY_SIZE])

                    if tmp_entry.Attributes == Attributes.EMPTY:
                        buffer = buffer[:offset] + entry.dump() + buffer[offset + Entry.ENTRY_SIZE:]
                        self.data.write_sector(dir_cluster, sector, buffer)
                        return

            next_cluster = self.file_table.read_index(dir_cluster)
            if next_cluster == FileTable.END_INDEX:
                break
            else:
                dir_cluster = next_cluster

        new_cluster = self.file_table.append_cluster_list(dir_cluster)
        self.data.write_sector(new_cluster, 0, entry.dump())
