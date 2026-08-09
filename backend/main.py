from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from database.database import init_db, close_db

from app.api.routes.upload import router as upload_router
from app.api.routes.analyze import router as analyze_router
from app.api.routes.health import router as health_router


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


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,

    # Allows Vercel production + preview deployment URLs
    allow_origin_regex=r"https://.*\.vercel\.app",

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# API ROUTES
# --------------------------------------------------

app.include_router(upload_router)
app.include_router(analyze_router)
app.include_router(health_router)


# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Welcome to AI Resume Analyzer",
        "docs": "/docs",
        "health": "/health/",
    }