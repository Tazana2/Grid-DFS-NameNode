from fastapi import APIRouter, HTTPException
from models.auth import TokenResponse, LoginRequest
from .views import authenticate_user, create_token

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    if authenticate_user(req.username, req.password):
        token = create_token(req.username)
        return TokenResponse(access_token=token, token_type="bearer")
    raise HTTPException(status_code=401, detail="Invalid credentials")
