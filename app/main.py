from fastapi import Depends, FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from uvicorn import Config, Server
from pydantic import BaseModel
from typing import Annotated

##our files
from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users
from .db.db import database, User, Website, Product, CartedProd
from .test.test import add_user


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

@app.post("/login")
async def login_for_access_token(email: Annotated[str, Form()] ):
    print(email)
    return 0

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
