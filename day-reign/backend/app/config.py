from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    mongodb_uri: str
    mongodb_db: str = "dayreign"
    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra = "ignore"
    )

settings = Settings()

