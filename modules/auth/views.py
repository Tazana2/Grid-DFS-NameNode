import uuid
from modules.auth.user_storage import user_storage
from TEMP_STORAGE import TOKENS


def register_user(username: str, password: str):
    return user_storage.register(username, password)


def authenticate_user(username: str, password: str) -> bool:
    return user_storage.validate(username, password)


def create_token(username: str) -> str:
    token = str(uuid.uuid4())
    TOKENS[token] = username
    return token