import uuid
from typing import Dict, List
from models.node import RegisterDataNodeRequest, BlockMetadata

class Storage:
    def __init__(self) -> None:
        self.datanodes: Dict[str, RegisterDataNodeRequest] = {}
        self.files: Dict[str, List[BlockMetadata]] = {}
        self.rr_index = 0 # round robin

    def register_datanode(self, req: RegisterDataNodeRequest):
        self.datanodes[req.id] = req

    def allocate_file(self, filename: str, filesize: int, block_size: int):
        blocks = []
        datanode_ids = list(self.datanodes.keys())
        if not datanode_ids:
            raise Exception("There isn't any DataNode registered")
        
        num_block = (filesize + block_size - 1) // block_size
        for i in range(num_block):
            block_id = f"{filename}_block_{i}_{uuid.uuid4().hex[:6]}"
            datanode = self.datanodes[datanode_ids[self.rr_index % len(datanode_ids)]]
            self.rr_index += 1

            block = BlockMetadata(
                block_id=block_id,
                ip=datanode.ip,
                port=datanode.rpc_port,
                size=min(block_size, filesize - i * block_size),
                index=i
            )
            blocks.append(block)

        self.files[filename] = blocks
        return blocks

    def get_metadata(self, filename: str):
        return self.files.get(filename)
    
storage = Storage()