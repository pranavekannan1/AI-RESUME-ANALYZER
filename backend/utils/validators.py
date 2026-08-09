from fastapi import HTTPException, UploadFile

ALLOWED_EXTENSIONS = {".pdf"}
RESUME_ONLY_MESSAGE = "Only a resume PDF file is allowed. Other file types are not supported."


def validate_pdf(file: UploadFile) -> None:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is missing.")

    filename = file.filename.lower()

    if not filename.endswith(tuple(ALLOWED_EXTENSIONS)):
        raise HTTPException(status_code=400, detail=RESUME_ONLY_MESSAGE)

    if file.content_type and file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail=RESUME_ONLY_MESSAGE)
