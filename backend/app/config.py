import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "OnboardIQ - Agentic AI-Powered Employee Onboarding Orchestrator"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"

    # Database
    DATABASE_URL: str = "sqlite:///./onboardiq.db"

    # LLM / Ollama configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "phi3:latest"
    USE_LOCAL_LLM: bool = True
    DEMO_MODE: bool = True

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000", "*"]

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
