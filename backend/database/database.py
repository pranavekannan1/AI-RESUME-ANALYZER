from pymongo import MongoClient
from pymongo.database import Database

from core.config import settings

_client: MongoClient | None = None
_db: Database | None = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        if not settings.MONGODB_URI.strip():
            raise RuntimeError("MONGODB_URI is not configured.")
        _client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=10000)
    return _client


def get_database() -> Database:
    global _db
    if _db is None:
        _db = get_client()[settings.MONGODB_DATABASE]
    return _db


def init_db() -> None:
    db = get_database()
    db.command("ping")
    db.resumes.create_index("uploaded_at")


def close_db() -> None:
    global _client, _db
    if _client is not None:
        _client.close()
    _client = None
    _db = None


def get_db() -> Database:
    return get_database()
