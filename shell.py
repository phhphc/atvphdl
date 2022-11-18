from structs.volume import *
from getpass import getpass

File_Name = "MyDir.DRS"
File_Size = 100_000
class Shell:
    
    def __init__(self) -> None:
        self.volume = Volume()
        self.entries = []
        self.trashes = []

    def new(self):
        self.volume.new(File_Name, File_Size)

    def open(self):
        self.volume.open(File_Name)

    def reload(self):
        self.entries = self.volume.list_entry(FileTable.ROOT_DIR_FIRST_CLUSTER)
        self.trashes = self.volume.list_entry(FileTable.DELE_DIR_FIRST_CLUSTER)

    def ls(self):
        for entry in self.entries:
            print(entry.Name.decode())

    def trash(self):
        for entry in self.trashes:
            print(entry.Name.decode())

    def rm(self, args):
        if len(args) == 0:
            print("Usage: rm [filename] to remove file")

        for filename in args:
            found = False
            for entry in self.entries:
                if self.match_name(entry.Name.decode(), filename):
                    self.volume.delete_entry(entry)
                    found = True
                    break

            if not found:
                print("file", filename, "not found in file dir")


    def rc(self, args):
        if len(args) == 0:
            print("Usage: rm [filename] to remove file")
            return

        for filename in args:
            found = False
            for entry in self.trashes:
                if self.match_name(entry.Name.decode(), filename):
                    self.volume.recover_entry(entry)
                    found = True
                    break

            if not found:
                print("file", filename, "not found in trash")


    def import_file(self, args):
        if len(args) == 0:
            print("Usage: import [filename] to import to volume")
            return

        for filename in args:
            try:
                self.volume.import_file(filename)
            except FileNotFoundError:
                print("file", filename, "not found in your device")


    def export_file(self, args):
        if len(args) < 0:
            print("Usage: export [filename] to export to volume")
            return

        filename = args[0]
        found = False
        for entry in self.entries:
            if self.match_name(entry.Name.decode(), filename):
                found = True
                if len(args) > 1:
                    self.volume.export_file(entry,args[1])
                else:
                    self.volume.export_file(entry)

        if not found:
            print("file", filename, "not found in file dir")


    def cat(self, args):
        if len(args) == 0:
            print("Usage: cat [filename] to read file")
            return

        filename = args[0]
        found = False
        for entry in self.entries:
            if self.match_name(entry.Name.decode(), filename):
                found = True
                for buffer in self.volume.get_content(entry):
                    print(buffer.decode(), end="")

        if not found:
            print("file", filename, "not found in file dir")


    def encrypt(self, args):
        if len(args) == 0:
            print("Usage: encrypt [filename] to encrypt")
        
        filename = args[0]
        found = False
        for entry in self.entries:
            if self.match_name(entry.Name.decode(), filename):
                password = getpass("password: ")
                self.volume.encrypt_entry(entry, password)
                found = True

        if not found:
            print("file", filename, "not found in file dir")


    def decrypt(self, args):
        if len(args) == 0:
            print("Usage: decrypt [filename] to decrypt")
        
        filename = args[0]
        found = False
        for entry in self.entries:
            if self.match_name(entry.Name.decode(), filename):
                password = getpass("password: ")
                self.volume.decrypt_entry(entry, password)
                found = True

        if not found:
            print("file", filename, "not found in file dir")


    def serve(self):
        try:
            while True:
                self.reload()
                line = input("\033[92m\n|=> \033[0m")
                cmd, *args = line.strip().split(' ')
                if cmd == "ls":
                    self.ls()
                elif cmd == "trash":
                    self.trash()
                elif cmd == "rm":
                    self.rm(args)
                elif cmd == "rc":
                    self.rc(args)
                elif cmd == "exit":
                    return
                elif cmd == "import":
                    self.import_file(args)
                elif cmd == "export":
                    self.export_file(args)
                elif cmd == "cat":
                    self.cat(args)
                elif cmd == "encrypt":
                    self.encrypt(args)
                elif cmd == "decrypt":
                    self.decrypt(args)
                else:
                    print("cmd: ", cmd, "not found")

        except KeyboardInterrupt:
            pass


    def match_name(self, a: str, b:str)-> bool:
        return a.strip("\x00") == b.strip("\x00")