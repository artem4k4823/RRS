from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file='.env',
        extra='ignore',
        
    )
    
    DATABASE_URL: PostgresDsn


settings = Settings()