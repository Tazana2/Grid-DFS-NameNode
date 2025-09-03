import uuid
from typing import Dict, List
from models.node import RegisterDataNodeRequest, BlockMetadata

class Storage:
    def __init__(self) -> None:
        self.datanodes: Dict[str, RegisterDataNodeRequest] = {}
        self.files: Dict[str, Dict] = {}
        self.rr_index = 0 # round robin

    def register_datanode(self, req: RegisterDataNodeRequest):
        self.datanodes[req.id] = req

    def allocate_file(self, filename: str, filesize: int, block_size: int, owner: str, directory: str = "/"):
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
                datanode={
                    "id": datanode.id,
                    "ip": datanode.ip,
                    "grpc_port": datanode.rpc_port,
                },
                size=min(block_size, filesize - i * block_size),
                index=i
            )
            blocks.append(block.model_dump())

        self.files[filename] = {
            "blocks": blocks,
            "owner": owner,
            "dir": directory
        }
        return blocks

    def ls_files(self, owner: str):
        return {fn: meta for fn, meta in self.files.items() if meta["owner"] == owner}

    def rm_file(self, filename: str, owner: str):
        if filename not in self.files or self.files[filename]["owner"] != owner:
            raise Exception("File not found or permission denied")
        deleted = self.files.pop(filename)
        return deleted
    
    def mkdir(self, dirname: str, owner: str):
        return {"msg": f"Directory {dirname} created for {owner}"}

    def rmdir(self, dirname: str, owner: str):
       return {"msg": f"Directory {dirname} removed for {owner}"}
    
    def get_metadata(self, filename: str):
        return self.files.get(filename)
    
storage = Storage()