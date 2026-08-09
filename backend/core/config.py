from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# backend/
BASE_DIR = Path(__file__).resolve().parents[1]

# backend/.env
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):

    # --------------------------------------------------
    # Application
    # --------------------------------------------------

    APP_NAME: str = "AI Resume Analyzer API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # --------------------------------------------------
    # Gemini
    # --------------------------------------------------

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.5-flash"

    # --------------------------------------------------
    # MongoDB
    # --------------------------------------------------

    MONGODB_URI: str = ""
    MONGODB_DATABASE: str = "cluster"

    # --------------------------------------------------
    # Local database
    # --------------------------------------------------

    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'resume_analyzer.db'}"

    # --------------------------------------------------
    # File uploads
    # --------------------------------------------------

    UPLOAD_DIR: str = str(BASE_DIR / "uploads")
    MAX_FILE_SIZE: int = 5 * 1024 * 1024

    # --------------------------------------------------
    # CORS
    # --------------------------------------------------

    CORS_ORIGINS: str = (
        "http://localhost:3000,"
        "http://127.0.0.1:3000"
    )

    # --------------------------------------------------
    # Environment configuration
    # --------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        if isinstance(value, list):
            return ",".join(str(item) for item in value)

        if value is None:
            return ""

        return str(value)

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]


settings = Settings()