from pydantic_settings import BaseSettings
from decouple import config
from fastapi.templating import Jinja2Templates
from pathlib import Path


user = config('USER')
password = config('PASSWORD')
servername = config('SERVERNAME')
port = config('PORT')
database = config('DATABASE')

class Settings(BaseSettings):
    DB_URL: str = f'postgres+asyncpg://{user}:{password}@{servername}:{port}/{database}'
    TEMPLATES: Jinja2Templates = Jinja2Templates(directory='templates')
    MEDIA: Path = Path('media')
    
    class Config:
        case_sensitive = True


settings: BaseSettings = Settings()