from fastapi import APIRouter, status
from typing import List

from schemas.user import User, UserCreate, UserUpdate
from services.users import UserService

router = APIRouter()


@router.get("/", response_model=List[User])
def list_users():
    return UserService.list_users()


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    return UserService.get_user(user_id)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
    return UserService.create_user(payload.model_dump())


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, payload: UserUpdate):
    return UserService.update_user(user_id, payload.model_dump())


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    UserService.delete_user(user_id)
    return None


@router.post("/{user_id}/deactivate", response_model=User)
def deactivate_user(user_id: int):
    return UserService.deactivate_user(user_id)
