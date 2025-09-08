from fastapi import APIRouter, Depends, HTTPException
from models.node import RegisterDataNodeRequest, AllocateRequest
from services.auth import get_current_user
from .storage import storage

router = APIRouter()

@router.post("/register_datanode")
def register_datanode(req: RegisterDataNodeRequest):
    storage.register_datanode(req)
    return {"msg": "DataNode Registered Succesfully!", "datanodes": storage.datanodes}

@router.post("/allocate")
def allocate(req: AllocateRequest, user: str = Depends(get_current_user)):
    blocks = storage.allocate_file(req.filename, req.filesize, req.block_size, user, req.directory)
    return {"filename": req.filename, "blocks": blocks}

@router.get("/metadata/{filename}")
def metadata(filename: str, directory: str,user: str = Depends(get_current_user)):
    meta = storage.get_metadata(filename, directory, user)
    if not meta:
        raise HTTPException(status_code=404, detail="File not found")
    return meta

@router.get("/ls")
def list_files(directory: str = "/", user: str = Depends(get_current_user)):
    return storage.ls_files(user, directory)

@router.delete("/rm/{filename}")
def remove_file(filename: str, directory: str, user: str = Depends(get_current_user)):
    deleted = storage.rm_file(filename, directory ,user)
    return {"msg": f"File {filename} deleted", "deleted": deleted}

@router.post("/mkdir")
def make_dir(dirname: str, parent: str, user: str = Depends(get_current_user)):
    return storage.mkdir(dirname, user, parent)

@router.delete("/rmdir")
def remove_dir(dirname: str, parent: str = "/", user: str = Depends(get_current_user)):
    result = storage.rmdir(dirname, user, parent)
    return result

@router.get("/tree")
def tree(user: str = Depends(get_current_user)):
    return storage.directories.get(user, {})