from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pymongo.database import Database

from core.config import settings
from database.crud import create_resume
from database.database import get_db
from services.file_service import FileService
from services.pdf_service import extract_text_from_pdf

router = APIRouter(tags=["Upload"])


@router.post("/upload/")
async def upload_resume(file: UploadFile = File(...), db: Database = Depends(get_db)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_data = await file.read()
    if not file_data:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(file_data) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"PDF is too large. Maximum size is {settings.MAX_FILE_SIZE // (1024 * 1024)} MB.",
        )

    try:
        resume_text = extract_text_from_pdf(file_data).strip()
        saved_filename = FileService.save_file(file_data, file.filename)
        resume = create_resume(
            db=db,
            filename=saved_filename,
            original_filename=file.filename,
            file_size=len(file_data),
            resume_text=resume_text,
            file_data=file_data,
        )

        return {
            "resume_id": resume.id,
            "filename": resume.filename,
            "original_filename": resume.original_filename,
            "file_size": resume.file_size,
            "message": "Resume uploaded successfully.",
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Resume upload failed: {exc}") from exc
