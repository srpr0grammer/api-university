from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://admin:admin@172.17.0.4:5432/university-db'
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = True


settings = Settings()
