from typing import Optional, Dict
from threading import RLock
from app.core.security import hash_password, verify_password

class UserService:
    def __init__(self):
        self._users: Dict[str, Dict] = {}
        self._lock = RLock()

    def create_user(self, username: str, email: str, password: str) -> bool:
        with self._lock:
            if username in self._users:
                return False
            self._users[username] = {
                "username": username,
                "email": email,
                "password_hash": hash_password(password),
            }
            return True

    def authenticate(self, username: str, password: str) -> bool:
        with self._lock:
            u = self._users.get(username)
            return bool(u and verify_password(password, u["password_hash"]))

    def exists(self, username: str) -> bool:
        with self._lock:
            return username in self._users

    def get(self, username: str) -> Optional[Dict]:
        with self._lock:
            return self._users.get(username)

user_service = UserService()
