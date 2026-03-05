from fastapi import APIRouter
from app.api.v1.schemas.send_document import SendDocumentRequest
router = APIRouter()

@router.post("/send_document")
async def send_document(data: SendDocumentRequest):
    # Process the uploaded document and file type
    document = data.document
    file_type = data.file_type

    
    