"""Configuration management for investment-research-crew.
Loads settings from .env and environment variables.
Uses Pydantic for validation.
"""

from __future__ import annotations

import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Loads configuration from environment variables and .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # <-- ADD THIS
    )

    llm_provider: str = Field(default="openai", alias="LLM_PROVIDER")

    open_ai_key: str = Field(default="", alias="OPENAI_API_KEY")
    open_ai_url: str = Field(default="https://api.openai.com/v1", alias="OPENAI_API_URL")
    open_ai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")

    docker_ai_key: str = Field(default="", alias="DOCKER_AI_API_KEY")
    docker_ai_url: str = Field(default="http://localhost:12434/engines/v1", alias="DOCKER_AI_API_URL")
    docker_ai_model: str = Field(default="ai/gpt-oss", alias="DOCKER_AI_MODEL")


def load_settings() -> Settings:
    settings = Settings()
    # os.environ["OPENAI_BASE_URL"] = settings.open_ai_url
    # os.environ["OPENAI_API_KEY"] = settings.open_ai_key
    # os.environ["OPENAI_MODEL_NAME"] = settings.open_ai_model

    os.environ["OPENAI_BASE_URL"] = settings.docker_ai_url
    os.environ["OPENAI_API_KEY"] = settings.docker_ai_key
    os.environ["OPENAI_MODEL_NAME"] = settings.docker_ai_model
    os.environ["OPENAI_TRACING_ENABLED"] = "false"

    provider = (settings.llm_provider or "").strip().lower()

    if provider == "openai":
        if not settings.open_ai_key.strip():
            raise ValueError("Missing required setting: OPENAI_API_KEY")
    elif provider == "docker":
        # docker key may be optional; enforce if required
        # if not settings.docker_ai_key.strip():
        #     raise ValueError("Missing required setting: DOCKER_AI_API_KEY")
        pass
    else:
        raise ValueError("LLM_PROVIDER must be one of: openai, docker")

    return settings
