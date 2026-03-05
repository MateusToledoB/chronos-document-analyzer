
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "chronos-document-analyzer"


settings = Settings()