from fastapi import APIRouter
from app.api.v1.endpoints.cpf_validation import router as send_document_router

api_router_v1 = APIRouter()

api_router_v1.include_router(send_document_router)
