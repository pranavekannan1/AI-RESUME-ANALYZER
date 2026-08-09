from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pymongo.database import Database

from database.crud import create_resume
from database.database import get_db
from services.file_service import FileService
from services.pdf_service import extract_text_from_pdf
from utils.validators import validate_pdf

router = APIRouter(tags=["Upload"])


@router.post("/upload/")
async def upload_resume(
    file: UploadFile = File(...),
    db: Database = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided.",
        )

    validate_pdf(file)

    try:
        # Read uploaded PDF
        file_data = await file.read()

        if not file_data:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        file_size = len(file_data)

        # Save PDF to uploads directory
        saved_filename = FileService.save_file( # pyright: ignore[reportAttributeAccessIssue]
            file_data=file_data,
            original_filename=file.filename,
        )

        # Get saved PDF path
        pdf_path = FileService.get_file_path(saved_filename)

        # Extract text from PDF
        resume_text = extract_text_from_pdf(
            str(pdf_path)
        ).strip()

        # Save resume to MongoDB
        resume = create_resume(
            db=db,
            filename=saved_filename,
            original_filename=file.filename,
            file_size=file_size,
            resume_text=resume_text,
            file_data=file_data,
        )

        # Return MongoDB ObjectId as a string
        return {
            "resume_id": resume.id,
            "filename": resume.filename,
            "original_filename": resume.original_filename,
            "message": "Resume uploaded successfully.",
        }

    except HTTPException:
        raise

    except Exception as exc:
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Resume upload failed: {exc}",
        ) from exc

