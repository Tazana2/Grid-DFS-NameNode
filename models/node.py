from pydantic import BaseModel

class RegisterDataNodeRequest(BaseModel):
    id: str
    ip: str
    port: int
    capacity: int

class AllocateRequest(BaseModel):
    filename: str
    filesize: int
    block_size: int = 64 * 1024 * 1024 # 64MB default

class BlockMetadata(BaseModel):
    block_id: str
    datanode: str
    size: int
    index: int