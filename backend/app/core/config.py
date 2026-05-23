from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file='.env',
       
        
    )
    DATABASE_URL: str
    SECRET_KEY: str
    EXPIRE_TIME: int
    ALGORITHM: str


settings = Settings()