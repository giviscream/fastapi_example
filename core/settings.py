from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.example",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        frozen=True,
    )
    DATABASE_URL: PostgresDsn

    @property
    def async_database_url(self) -> str:
        """Возвращает строку подключения для асинхронной работы"""
        return str(self.DATABASE_URL)


settings = Settings()
