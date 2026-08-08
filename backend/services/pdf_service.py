from io import BytesIO
from pathlib import Path

from pypdf import PdfReader


def extract_text_from_pdf(source: bytes | str | Path) -> str:
    if isinstance(source, (str, Path)):
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {path}")
        if path.suffix.lower() != ".pdf":
            raise ValueError("Only PDF files are supported.")
        reader = PdfReader(str(path))
    else:
        if not source:
            raise ValueError("PDF data is empty.")
        reader = PdfReader(BytesIO(source))

    if reader.is_encrypted:
        try:
            result = reader.decrypt("")
            if result == 0:
                raise ValueError("The PDF is encrypted and requires a password.")
        except ValueError:
            raise
        except Exception as exc:
            raise ValueError("The PDF is encrypted and cannot be read.") from exc

    pages: list[str] = []
    for page_number, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:
            raise ValueError(f"Could not extract text from PDF page {page_number}: {exc}") from exc
        if text.strip():
            pages.append(text.strip())

    extracted_text = "\n\n".join(pages).strip()
    if not extracted_text:
        raise ValueError(
            "No readable text was found in the PDF. If this is a scanned/image-only PDF, OCR is required."
        )
    return extracted_text
