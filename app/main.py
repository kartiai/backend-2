from fastapi import Depends, FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from uvicorn import Config, Server
from pydantic import BaseModel
from typing import Annotated
from fastapi import status,HTTPException
from ormar import NoMatch
from datetime import timedelta
from jose import jwt
from datetime import datetime

##our files
from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users
from .db.db import database, User, Website, Product, CartedProd
from .test.test import add_user

SECRET_KEY = "871824CB7E7F31A266649B8AA92B8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class LoginPostBody(BaseModel):
    name: str
    password: str


app = FastAPI()##dependencies=[Depends(get_query_token)]
app.mount("/frontend", StaticFiles(directory="app/frontend/static"), name="static")
templates = Jinja2Templates(directory="./app/frontend/templates")
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


##routes html application
@app.get("/", response_class=HTMLResponse)
async def index_html(request: Request):
    return templates.TemplateResponse("index.html",{ "request": request })

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html",{ "request": request })

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    result = await User.objects.all()
    print(result)
    return templates.TemplateResponse("register.html",{ "request": request })

@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    return templates.TemplatesResponse("profile.html",{ "request": request })

class Token(BaseModel):
    access_token: str
    code: int

async def authenticate_user(email: str, password: str):
    try:
        user = await User.objects.get(email=email)
        print(user)
        if user.password == password:
            return user
        return None
    # if not Hasher.verify_password(password, user.hashed_password):
    #     return False
    except NoMatch:
        return None

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(await User.objects.all())
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        return {"code": 401, "access_token": ""}

    token = create_access_token(data = {"email":  user.email})
    user.token = token
    user.save()
    print(jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)['exp'])
    return {"code": 200, "access_token": token}

@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await add_user()

@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

if __name__ == "__main__":  # pragma: no cover
    server = Server(
        Config(
            "runserver:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
        ),
    )

    # do something you want before running the server
    # eg. setting up custom loggers
    server.run()
