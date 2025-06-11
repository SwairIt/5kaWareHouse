from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field


BASE_DIR = Path(__file__).resolve().parent.parent.parent

print(BASE_DIR / ".env")

class Settings(BaseSettings):
    BOT_TOKEN: SecretStr = Field(..., validation_alias="BOT_TOKEN")
    DB_LITE: str = f"sqlite+aiosqlite:///{BASE_DIR}/my_base.db"

    model_config = SettingsConfigDict(
        env_file = BASE_DIR / ".env",
        env_file_encoding = "utf-8"
    )

settings = Settings()