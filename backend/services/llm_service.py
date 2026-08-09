import json

from google import genai
from google.genai import types

from core.config import settings
from prompts.resume_prompt import build_resume_prompt
from schemas.analysis import AnalysisResponse


class LLMService:

    @staticmethod
    def analyze_resume(resume_text: str) -> AnalysisResponse:

        if not resume_text.strip():
            raise ValueError(
                "Resume text is empty. Cannot analyze resume."
            )

        api_key = settings.GEMINI_API_KEY.strip()

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        client = genai.Client(
            api_key=api_key
        )

        model = settings.GEMINI_MODEL.strip()

        if not model:
            model = "gemini-3.5-flash"

        prompt = build_resume_prompt(resume_text)

        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=AnalysisResponse,
                ),
            )

        except Exception as exc:
            raise RuntimeError(
                f"Gemini request failed using model '{model}': {exc}"
            ) from exc

        text = (response.text or "").strip()

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        try:
            data = json.loads(text)

            return AnalysisResponse.model_validate(data)

        except Exception as exc:
            raise ValueError(
                f"Gemini returned invalid analysis JSON: {text[:500]}"
            ) from exc