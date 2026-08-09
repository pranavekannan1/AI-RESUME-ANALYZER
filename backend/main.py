from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from database.database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()

    yield

    close_db()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to AI Resume Analyzer",
        "docs": "/docs",
        "health": "/health/",
    }


@app.get("/health/")
def health():
    return {
        "status": "healthy"
    }