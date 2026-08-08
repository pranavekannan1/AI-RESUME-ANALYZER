from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.analyze import router as analyze_router
from app.api.routes.health import router as health_router
from app.api.routes.upload import router as upload_router
from core.config import settings
from core.logger import logger
from database.database import close_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info("AI Resume Analyzer MongoDB initialized.")
    yield
    close_db()
    logger.info("AI Resume Analyzer shutting down.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Resume Analyzer Backend",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(analyze_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to AI Resume Analyzer",
        "docs": "/docs",
        "health": "/health/",
    }
