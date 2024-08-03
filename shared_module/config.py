import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentVariable(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    openai_api_key: str


EnvVar = EnvironmentVariable()  # type: ignore
