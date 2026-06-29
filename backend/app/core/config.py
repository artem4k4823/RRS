from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file='.env',
       
        
    )
    DATABASE_URL: str
    SECRET_KEY: str
    ACCCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_EXPIRE_TIME_DAYS: int
    ALGORITHM: str
    REDIS_URL: str
    POST_CACHED_KEY: str
    URL_CACHED_KEY: str
    CACHE_TTL_SECONDS: int
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str


settings = Settings()