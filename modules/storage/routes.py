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
    blocks = storage.allocate_file(req.filename, req.filesize, req.block_size)
    return {"filename": req.filename, "blocks": blocks}

@router.get("/metadata/{filename}")
def metadata(filename: str, user: str = Depends(get_current_user)):
    meta = storage.get_metadata(filename)
    if not meta:
        raise HTTPException(status_code=404, detail="File not found")
    return meta
