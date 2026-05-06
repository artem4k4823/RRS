from pydantic import PostgresDsn, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConf(BaseModel):
    host: str = '127.0.0.1'
    port: str = '8003'


class Database(BaseModel):
    database_url: PostgresDsn = 'db/url'    
    
    
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file='.env'
    )
    database: Database = Database()
    
    
settings = Settings()