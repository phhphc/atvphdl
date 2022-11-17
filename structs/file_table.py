
EMPTY_INDEX = bytes.fromhex('ffffffff')
END_INDEX = bytes.fromhex('fffff0f0')


class FileTable:

    def __init__(self, f, offset: int, size: int):
        self.io = f
        self.offset = offset
        self.size = size

    def cluster_list():
        pass
        # TODO: get cluster list of a file

    def empty_cluster():
        pass

    def format(self):
        self.io.seek(self.offset)
        self.io.write(END_INDEX*2)

        for _ in range(self.size // 4 - 2):
            self.io.write(EMPTY_INDEX)
