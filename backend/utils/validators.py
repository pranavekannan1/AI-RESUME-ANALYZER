from fastapi import HTTPException, UploadFile

ALLOWED_EXTENSIONS = {".pdf"}


def validate_pdf(file: UploadFile) -> None:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is missing.")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
