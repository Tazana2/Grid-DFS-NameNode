import uuid
from TEMP_STORAGE import USERS, TOKENS


def authenticate_user(username: str, password: str) -> bool:
    return username in USERS and USERS[username] == password

def create_token(username: str) -> str:
    token = str(uuid.uuid4())
    TOKENS[token] = username
    return token