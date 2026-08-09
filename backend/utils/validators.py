from fastapi import HTTPException, UploadFile

ALLOWED_EXTENSIONS = {".pdf"}
RESUME_ONLY_MESSAGE = "Only a resume PDF file is allowed. Other file types are not supported."


async def validate_pdf(file: UploadFile) -> None:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is missing.")

    filename = file.filename.lower()

    if not filename.endswith(tuple(ALLOWED_EXTENSIONS)):
        raise HTTPException(status_code=400, detail=RESUME_ONLY_MESSAGE)

    # Read bytes from the request body and validate the binary signature.
    # A file with a .pdf name but a DOCX/PNG/etc payload must be rejected.
    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if not content.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail=RESUME_ONLY_MESSAGE)

    # Restore the upload stream position so the route can keep using the same file object.
    if hasattr(file.file, "seek"):
        file.file.seek(0)

    if file.content_type and file.content_type not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(status_code=400, detail=RESUME_ONLY_MESSAGE)
