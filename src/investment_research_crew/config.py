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

    docker_url_alias: str = "DOCKER_AI_API_URL"
    docker_url: str = "http://localhost:12434/engines/v1"
    lmstudio_url: str = "http://127.0.0.1:1234/v1"
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"

    llm_provider: str = Field(default="openai", alias="LLM_PROVIDER")

    rabbitmq_url: str = Field(default=rabbitmq_url, alias="RABBITMQ_URL")

    open_ai_key: str = Field(default="", alias="OPENAI_AI_API_KEY")
    open_ai_url: str = Field(default="https://api.openai.com/v1", alias="OPENAI_AI_API_URL")
    open_ai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_AI_MODEL")

    docker_ai_key: str = Field(default="", alias="DOCKER_AI_API_KEY")
    docker_ai_url: str = Field(default=docker_url, alias=docker_url_alias)
    docker_ai_model: str = Field(default="openai/gpt-oss", alias="DOCKER_AI_MODEL")

    lmstudio_ai_key: str = Field(default="", alias="LMSTUDIO_AI_API_KEY")
    lmstudio_ai_url: str = Field(default=lmstudio_url, alias="LMSTUDIO_AI_API_URL")
    lmstudio_ai_model: str = Field(default="openai/gpt-oss", alias="LMSTUDIO_AI_MODEL")

    model_in_use: str = ""
    key_in_use: str = ""
    url_in_use: str = ""

    # API Settings
    host: str = Field(default="0.0.0.0", alias="API_HOST")
    port: int = Field(default=8000, alias="API_PORT")
    reload: bool = Field(default=True, alias="API_RELOAD")


def load_settings() -> Settings:
    """
    Docstring for load_settings

    :return: Description
    :rtype: Settings
    """
    settings = Settings()

    # API Settings
    #     host = settings.host
    # port = settings.port
    # reload = settings.reload

    provider = (settings.llm_provider or "").strip().lower()

    if provider == "openai":
        if not settings.open_ai_key.strip():
            raise ValueError("Missing required setting: OPENAI_AI_API_KEY")
        os.environ["OPENAI_BASE_URL"] = settings.open_ai_url
        os.environ["OPENAI_API_KEY"] = settings.open_ai_key
        os.environ["OPENAI_MODEL_NAME"] = settings.open_ai_model
        os.environ["OPENAI_TRACING_ENABLED"] = "true"
        settings.model_in_use = settings.open_ai_model
        settings.key_in_use = settings.open_ai_key
        settings.url_in_use = settings.open_ai_url
    elif provider == "docker":
        # docker key may be optional; enforce if required
        if not settings.docker_ai_key.strip():
            raise ValueError("Missing required setting: DOCKER_AI_API_KEY")
        os.environ["OPENAI_BASE_URL"] = settings.docker_ai_url
        os.environ["OPENAI_API_KEY"] = settings.docker_ai_key
        os.environ["OPENAI_MODEL_NAME"] = settings.docker_ai_model
        os.environ["OPENAI_TRACING_ENABLED"] = "false"
        settings.model_in_use = settings.docker_ai_model
        settings.key_in_use = settings.docker_ai_key
        settings.url_in_use = settings.docker_ai_url
    elif provider == "lmstudio":
        if not settings.lmstudio_ai_key.strip():
            raise ValueError("Missing required setting: LMSTUDIO_AI_API_KEY")
        os.environ["OPENAI_BASE_URL"] = settings.lmstudio_ai_url
        os.environ["OPENAI_API_KEY"] = settings.lmstudio_ai_key
        os.environ["OPENAI_MODEL_NAME"] = settings.lmstudio_ai_model
        os.environ["OPENAI_TRACING_ENABLED"] = "false"
        settings.model_in_use = settings.lmstudio_ai_model
        settings.key_in_use = settings.lmstudio_ai_key
        settings.url_in_use = settings.lmstudio_ai_url
    else:
        raise ValueError("LLM_PROVIDER must be one of: openai, docker, lmstudio")
    return settings
