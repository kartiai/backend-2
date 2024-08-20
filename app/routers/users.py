from fastapi import APIRouter

from ..db.db import User

router = APIRouter()
##https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

@router.get("/users/", tags=["users"])
async def read_users():
    return await User.objects.all()

@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}

@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}