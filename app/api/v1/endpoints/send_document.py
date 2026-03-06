from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.schemas.send_document import SendDocumentRequest
from app.utils.file_utils import FileUtils
from app.utils.uuid_utils import UUIDUtils
from app.services.ocr_service import OCRService

router = APIRouter()

@router.post("/cpf_validation")
async def send_document(data: SendDocumentRequest = Depends()):

    document = data.document
    file_id = UUIDUtils.generate_uuid()
    file_extension = FileUtils.extract_file_extension(document.filename)
    file_path = FileUtils.save_file(document, file_id, file_extension)
    
    try:
        matches = OCRService.extract_cpf(file_path)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"matches": matches}

    
