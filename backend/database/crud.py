from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from pymongo.database import Database


@dataclass
class Resume:
    id: str
    filename: str
    original_filename: str
    file_size: int
    resume_text: str
    analysis: str | None
    uploaded_at: datetime
    file_data: bytes | None = None


def _to_resume(document: dict[str, Any] | None) -> Resume | None:
    if document is None:
        return None
    return Resume(
        id=str(document["_id"]),
        filename=document["filename"],
        original_filename=document["original_filename"],
        file_size=int(document["file_size"]),
        resume_text=document.get("resume_text", "") or "",
        analysis=document.get("analysis"),
        uploaded_at=document.get("uploaded_at") or datetime.now(timezone.utc),
        file_data=bytes(document["file_data"]) if document.get("file_data") is not None else None,
    )


def create_resume(
    db: Database,
    filename: str,
    original_filename: str,
    file_size: int,
    resume_text: str,
    file_data: bytes,
) -> Resume:
    document = {
        "filename": filename,
        "original_filename": original_filename,
        "file_size": file_size,
        "resume_text": resume_text,
        "analysis": None,
        "file_data": file_data,
        "uploaded_at": datetime.now(timezone.utc),
    }
    result = db.resumes.insert_one(document)
    document["_id"] = result.inserted_id
    return _to_resume(document)  # type: ignore[return-value]


def get_resume(db: Database, resume_id: str) -> Resume | None:
    try:
        object_id = ObjectId(resume_id)
    except Exception:
        return None
    return _to_resume(db.resumes.find_one({"_id": object_id}))


def update_resume_text(db: Database, resume_id: str, resume_text: str) -> Resume | None:
    try:
        object_id = ObjectId(resume_id)
    except Exception:
        return None
    db.resumes.update_one({"_id": object_id}, {"$set": {"resume_text": resume_text}})
    return get_resume(db, resume_id)


def update_resume_analysis(db: Database, resume_id: str, analysis: str) -> Resume | None:
    try:
        object_id = ObjectId(resume_id)
    except Exception:
        return None
    db.resumes.update_one({"_id": object_id}, {"$set": {"analysis": analysis}})
    return get_resume(db, resume_id)
