from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Resume Analyzer API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-3.6-flash"

    MONGODB_URI: str
    MONGODB_DATABASE: str = "ai_resume_analyzer"

    MAX_FILE_SIZE: int = 5 * 1024 * 1024
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [x.strip() for x in self.CORS_ORIGINS.split(",") if x.strip()]


settings = Settings()
