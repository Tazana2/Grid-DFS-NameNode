from fastapi import APIRouter, Depends, HTTPException
from models.node import RegisterDataNodeRequest, AllocateRequest
from services.auth import get_current_user
from .storage import storage

router = APIRouter()


@router.post("/register_datanode")
def register_datanode(req: RegisterDataNodeRequest):
    storage.register_datanode(req)
    return {"msg": "DataNode Registered Succesfully!"}

@router.post("/allocate")
def allocate(req: AllocateRequest, user: str = Depends(get_current_user)):
    try:
        blocks = storage.allocate_file(req.filename, req.filesize, req.block_size, user, req.directory)
        return {"filename": req.filename, "blocks": blocks}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/metadata/{filename}")
def metadata(filename: str, directory: str, user: str = Depends(get_current_user)):
    try:
        return storage.get_metadata(filename, directory, user)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/ls")
def list_files(directory: str = "/", user: str = Depends(get_current_user)):
    try:
        return storage.ls_files(user, directory)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/rm/{filename}")
def remove_file(filename: str, directory: str, user: str = Depends(get_current_user)):
    try:
        deleted = storage.rm_file(filename, directory, user)
        return {"msg": f"File {filename} deleted", "deleted": deleted}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/mkdir")
def make_dir(dirname: str, parent: str = "/", user: str = Depends(get_current_user)):
    try:
        return storage.mkdir(dirname, user, parent)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/rmdir")
def remove_dir(dirname: str, parent: str = "/", user: str = Depends(get_current_user)):
    try:
        result = storage.rmdir(dirname, user, parent)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tree")
def tree(user: str = Depends(get_current_user)):
    return storage.directories.get(user, {})