from pydantic import BaseModel

class RegisterDataNodeRequest(BaseModel):
    id: str
    ip: str
    rest_port: int
    rpc_port: int
    capacity: int

class AllocateRequest(BaseModel):
    filename: str
    filesize: int
    block_size: int = 64 * 1024 * 1024 # 64MB default

class BlockMetadata(BaseModel):
    block_id: str
    ip: str
    port: int
    size: int
    index: int