import json

from core.config import settings
from prompts.resume_prompt import build_resume_prompt
from schemas.analysis import AnalysisResponse


class LLMService:
    @staticmethod
    def analyze_resume(resume_text: str) -> AnalysisResponse:
        if not resume_text.strip():
            raise ValueError("Resume text is empty. Cannot analyze resume.")
        if not settings.GEMINI_API_KEY.strip():
            raise ValueError("GEMINI_API_KEY is not configured.")

        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError("google-genai is not installed. Run pip install -r requirements.txt") from exc

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        model = settings.GEMINI_MODEL.strip() or "gemini-3.6-flash"
        prompt = build_resume_prompt(resume_text)

        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": AnalysisResponse,
                },
            )
        except Exception as exc:
            raise RuntimeError(f"Gemini request failed using model '{model}': {exc}") from exc

        text = (response.text or "").strip()
        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        try:
            return AnalysisResponse.model_validate(json.loads(text))
        except Exception as exc:
            raise ValueError(f"Gemini returned invalid analysis JSON: {text[:500]}") from exc
