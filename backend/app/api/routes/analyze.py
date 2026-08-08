from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError

from database.crud import get_resume, update_resume_analysis, update_resume_text
from database.database import get_db
from services.llm_service import LLMService
from services.pdf_service import extract_text_from_pdf

router = APIRouter(tags=["Analysis"])


@router.post("/analyze/{resume_id}")
def analyze_resume(resume_id: str):
    try:
        db = get_db()
        resume = get_resume(db, resume_id)
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail=f"MongoDB error: {exc}") from exc

    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found.")

    resume_text = (resume.resume_text or "").strip()

    print("\n========== ANALYSIS DEBUG ==========")
    print("Resume ID:", resume.id)
    print("Filename:", resume.filename)
    print("Original filename:", resume.original_filename)
    print("Resume text length:", len(resume_text))

    if not resume_text and resume.file_data:
        try:
            resume_text = extract_text_from_pdf(resume.file_data).strip()
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"PDF recovery failed: {exc}") from exc
        if resume_text:
            update_resume_text(db, resume.id, resume_text)

    if not resume_text:
        raise HTTPException(status_code=400, detail="Resume text is empty. Please upload the resume again.")

    try:
        result = LLMService.analyze_resume(resume_text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {exc}") from exc

    update_resume_analysis(db=db, resume_id=resume.id, analysis=result.model_dump_json())

    return {"resume_id": resume.id, "analysis": result.model_dump()}
