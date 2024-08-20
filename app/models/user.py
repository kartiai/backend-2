from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    id: int
    email: str
    active: bool

    class Config:
        orm_mode = True