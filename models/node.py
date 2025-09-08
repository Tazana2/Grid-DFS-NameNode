from pydantic import BaseModel
from typing import Optional

class RegisterDataNodeRequest(BaseModel):
    id: str
    ip: str
    rest_port: int
    rpc_port: int
    capacity: int
    last_seen: Optional[str] = None

class AllocateRequest(BaseModel):
    filename: str
    filesize: int
    block_size: int = 64 * 1024 * 1024 # 64MB default
    owner: str
    directory: str = "/"

class BlockMetadata(BaseModel):
    block_id: str
    datanode: dict
    size: int
    index: int