from fastapi import APIRouter, HTTPException
from models.auth import TokenResponse, LoginRequest, RegisterRequest
from .views import authenticate_user, create_token, register_user

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    if authenticate_user(req.username, req.password):
        token = create_token(req.username)
        return TokenResponse(access_token=token, token_type="bearer")
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/register")
def register(req: RegisterRequest):
    try:
        register_user(req.username, req.password)
    except Exception:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"msg": f"User {req.username} registered successfully"}