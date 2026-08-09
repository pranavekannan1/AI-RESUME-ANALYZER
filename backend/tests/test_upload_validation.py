import asyncio
from io import BytesIO

import pytest
from fastapi import HTTPException, UploadFile

from utils.validators import validate_pdf


def test_pdf_validator_rejects_non_pdf_bytes_with_pdf_name() -> None:
    file = UploadFile(
        filename="fake.pdf",
        file=BytesIO(b"PK\x03\x04not-a-real-pdf"),
        headers={"content-type": "application/octet-stream"},
    )

    with pytest.raises(HTTPException) as exc:
        asyncio.run(validate_pdf(file))

    assert exc.value.status_code == 400


def test_pdf_validator_accepts_pdf_signature() -> None:
    file = UploadFile(
        filename="resume.pdf",
        file=BytesIO(b"%PDF-1.4\n1 0 obj\n<<>>"),
        headers={"content-type": "application/pdf"},
    )

    asyncio.run(validate_pdf(file))
