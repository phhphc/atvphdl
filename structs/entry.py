

class Entry:

    Name: bytes
    # 
    Attributes: bytes
    #  
    FirstCluster: int
    # 16 bytes use for AES CTR
    Nonce: bytes 
    # 4 bytes
    ContentSize: int 

    def get_content():
        pass
        # TODO: get file content

    def new(name, ) -> None:
        pass
        # Create new entry

    def dump() -> bytes:
        pass
        # export entry data into 64 bytes

    def parse(buffer) -> None:
        pass 
        # parse 64 bytes input to entry data

# Entry size 64 bytes