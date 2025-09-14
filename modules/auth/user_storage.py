import json
import os
import hashlib
from typing import Dict


class UserStorage:
    def __init__(self, users_file: str | None = None):
        if users_file is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            users_file = os.path.join(base_dir, "..", "..", "users.json")
            users_file = os.path.abspath(users_file)
        self.users_file = users_file
        self.users: Dict[str, str] = {}
        self._load_users()

    def _load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                self.users = json.load(f)

    def _persist(self):
        with open(self.users_file, "w") as f:
            json.dump(self.users, f)

    def register(self, username: str, password: str):
        if username in self.users:
            raise Exception("User already exists")
        hashed = hashlib.sha256(password.encode()).hexdigest()
        self.users[username] = hashed
        self._persist()
        return {"msg": f"User {username} registered successfully"}

    def validate(self, username: str, password: str) -> bool:
        hashed = hashlib.sha256(password.encode()).hexdigest()
        return self.users.get(username) == hashed


user_storage = UserStorage()