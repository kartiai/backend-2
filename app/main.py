from fastapi import Depends, FastAPI
from uvicorn import Config, Server
from typing import List, Dict
import os

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users, upload

from .db.db import database, User
from .models.user import UserBase
from .test.test import add_user
import logging

if os.getenv('DEBUG') == "True":
    logging.basicConfig(level=logging.DEBUG)
app = FastAPI(##dependencies=[Depends(get_query_token)]
)
# postgres % curl -X POST http://0.0.0.0:8000/upload/put \
#      -F "files=@/Users/bibinabogdan/Desktop/job/blast-indexer2/blast-builder-indexer/indexer_core/docs/postgres/data/postgres/postgresql.conf" \
#      -H "Content-Type: multipart/form-data" \
#      -H "API-Key: your_secret_key"
##https://testdriven.io/blog/fastapi-docker-traefik/
##https://www.fastapitutorial.com/blog/serving-html-fastapi/
##https://fastapi.tiangolo.com/tutorial/sql-databases/
app.include_router(users.router)
app.include_router(items.router)
app.include_router(upload.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    #dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/", response_model=List[UserBase])
async def root():
    users = await User.objects.all()
    return [user.dict() for user in users]

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