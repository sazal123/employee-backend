from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_ENV: str
    APP_DEBUG: bool

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    UPLOAD_DIR: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
