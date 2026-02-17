# One place to load and access all environment variables.
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = 'gpt-4o-mini'
    APP_ENV: str = 'development'

    model_config = SettingsConfigDict(env_file=".env")