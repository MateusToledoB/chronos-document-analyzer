from app.core.settings import settings
from app.api.router import api_router
from fastapi import FastAPI


app = FastAPI(title=settings.app_name)

app.include_router(api_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}