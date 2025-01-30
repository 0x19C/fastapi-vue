import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM

from src.routes import users, datasets, models


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("CORPY_FRONTEND", "http://localhost:4173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)

app.include_router(users.router)
app.include_router(datasets.router)
app.include_router(models.router)

app.mount("/storage", StaticFiles(directory="storage"), name="storage")
