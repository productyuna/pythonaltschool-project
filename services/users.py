from typing import List, Optional
from fastapi import HTTPException, status

from services.db import users, next_id


class UserService:
    @staticmethod
    def list_users() -> List[dict]:
        return users

    @staticmethod
    def get_user(user_id: int) -> dict:
        user = next((u for u in users if u["id"] == user_id), None)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    def create_user(data: dict) -> dict:
        new_user = {"id": next_id("user"), **data}
        users.append(new_user)
        return new_user

    @staticmethod
    def update_user(user_id: int, data: dict) -> dict:
        user = UserService.get_user(user_id)
        user.update({k: v for k, v in data.items() if v is not None})
        return user

    @staticmethod
    def delete_user(user_id: int) -> None:
        user = UserService.get_user(user_id)
        users.remove(user)

    @staticmethod
    def deactivate_user(user_id: int) -> dict:
        user = UserService.get_user(user_id)
        user["is_active"] = False
        return user
