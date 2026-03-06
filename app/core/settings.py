from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "chronos-document-analyzer"
     
    # files local storage
    FILES_PATH: str = "files/"


settings = Settings()