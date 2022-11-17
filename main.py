from structs.boot_sector import *
from structs.file_table import *
from structs.volume import *

File_Name = "MyDir.DRS"
File_Size = 100_000

def main():
    volume = Volume()
    volume.new(File_Name, File_Size)

    for _ in range(3):
        print(next(volume.file_table.empty_cluster()))

    volume.import_file(bytes('abc.txt','utf-8'))

if __name__ == '__main__':
    main()
