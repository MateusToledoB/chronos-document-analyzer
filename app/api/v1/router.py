from fastapi import APIRouter
from app.api.v1.endpoints.send_document import router as send_document_router

api_router_v1 = APIRouter()

api_router_v1.include_router(send_document_router)
