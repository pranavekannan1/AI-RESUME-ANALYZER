from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database import init_db, close_db

from app.api.routes.upload import router as upload_router
from app.api.routes.analyze import router as analyze_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()

    yield

    close_db()


app = FastAPI(
    title="AI Resume Analyzer",
    version="1.0.0",
    lifespan=lifespan,
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

cors_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://rescan-resume-analyzer.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# API ROUTES
# --------------------------------------------------

app.include_router(upload_router)
app.include_router(analyze_router)


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


@app.get("/health/")
def health():
    return {
        "status": "healthy",
    }