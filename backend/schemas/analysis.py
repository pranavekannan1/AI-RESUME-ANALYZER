from pydantic import BaseModel, Field


class AnalysisResponse(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    summary: str
    skills: list[str]
    strengths: list[str]
    weaknesses: list[str]
    suggestions: list[str]
