from structs.boot_sector import *
from structs.file_table import *
from structs.volume import *

File_Name = "MyDir.DRS"
File_Size = 100_000_000

def main():
    volume = Volume()
    volume.new(File_Name, File_Size)


if __name__ == '__main__':
    main()
