from pathlib import Path
from uuid import uuid4


class FileService:
    UPLOAD_DIR = Path(__file__).resolve().parents[1] / "uploads"

    @classmethod
    def ensure_upload_directory(cls) -> None:
        cls.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def save_file(cls, file_data: bytes, original_filename: str) -> str:
        if not file_data:
            raise ValueError("Uploaded file is empty.")

        cls.ensure_upload_directory()
        extension = Path(original_filename).suffix.lower() or ".pdf"
        filename = f"{uuid4().hex}{extension}"
        (cls.UPLOAD_DIR / filename).write_bytes(file_data)
        return filename

    @classmethod
    async def save_upload(cls, file) -> str:
        content = await file.read()
        return cls.save_file(content, file.filename or "resume.pdf")

    @classmethod
    def get_file_path(cls, filename: str) -> Path:
        return cls.UPLOAD_DIR / filename
