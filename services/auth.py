from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from TEMP_STORAGE import TOKENS

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_token(token: str):
    return TOKENS.get(token)

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username
    