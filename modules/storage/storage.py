import uuid
from typing import Dict
from models.node import RegisterDataNodeRequest, BlockMetadata

class Storage:
    def __init__(self) -> None:
        self.datanodes: Dict[str, RegisterDataNodeRequest] = {}
        self.directories: Dict[str, Dict] = {}  # owner -> root tree
        self.rr_index = 0

    def register_datanode(self, req: RegisterDataNodeRequest):
        self.datanodes[req.id] = req

    def _ensure_user_root(self, owner: str):
        if owner not in self.directories:
            self.directories[owner] = {
                "/": {"subdirs": {}, "files": {}}
            }

    def _get_dir(self, owner: str, path: str):
        self._ensure_user_root(owner)
        parts = [p for p in path.strip("/").split("/") if p]
        curr = self.directories[owner]["/"]
        print(f"parts: {parts}\n curr: {curr}\n path: {path}")
        for part in parts:
            if part not in curr["subdirs"]:
                raise Exception(f"Directory {path} not found")
            curr = curr["subdirs"][part]
        return curr
    
    def _collect_files_in_dir(self, dir_ref: Dict):
        collected = []
        for fname, meta in dir_ref["files"].items():
            collected.append((fname, meta))
        for sub in dir_ref["subdirs"].values():
            collected.extend(self._collect_files_in_dir(sub))
        return collected

    def mkdir(self, dirname: str, owner: str, parent: str = "/"):
        self._ensure_user_root(owner)
        parent_dir = self._get_dir(owner, parent)
        if dirname in parent_dir["subdirs"]:
            raise Exception("Directory already exists")
        parent_dir["subdirs"][dirname] = {"subdirs": {}, "files": {}}
        return {"msg": f"Directory {dirname} created at {parent} for {owner}"}

    def rmdir(self, dirname: str, owner: str, parent: str = "/"):
        self._ensure_user_root(owner)
        parent_dir = self._get_dir(owner, parent)
        if dirname not in parent_dir["subdirs"]:
            raise Exception("Directory not found")

        dir_to_remove = parent_dir["subdirs"][dirname]

        deleted_blocks = []
        for fname, meta in self._collect_files_in_dir(dir_to_remove):
            deleted_blocks.extend(meta["blocks"])

        parent_dir["subdirs"].pop(dirname)

        return {
            "msg": f"Directory {dirname} and its files removed",
            "deleted_blocks": deleted_blocks
        }

    def allocate_file(self, filename: str, filesize: int, block_size: int, owner: str, directory: str = "/"):
        datanode_ids = list(self.datanodes.keys())
        if not datanode_ids:
            raise Exception("There isn't any DataNode registered")

        blocks = []
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

        dir_ref = self._get_dir(owner, directory)
        dir_ref["files"][filename] = {
            "blocks": blocks,
            "owner": owner,
            "dir": directory
        }
        return blocks

    def get_metadata(self, filename: str, directory: str, owner: str):
        dir_ref = self._get_dir(owner, directory)
        if filename not in dir_ref["files"]:
            raise Exception("File not found")
        return dir_ref["files"][filename]

    def rm_file(self, filename: str, directory: str, owner: str):
        dir_ref = self._get_dir(owner, directory)
        if filename not in dir_ref["files"]:
            raise Exception("File not found")
        deleted = dir_ref["files"].pop(filename)
        return deleted

    def ls_files(self, owner: str, directory: str = "/"):
        dir_ref = self._get_dir(owner, directory)
        return {
            "directories": list(dir_ref["subdirs"].keys()),
            "files": list(dir_ref["files"].keys())
        }


storage = Storage()