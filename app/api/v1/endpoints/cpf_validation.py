from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.schemas.cpf_validation import SendDocumentRequest
from app.utils.file_utils import FileUtils
from app.utils.uuid_utils import UUIDUtils
from app.services.ocr_service import OCRService
from app.utils.validadion_utils import ValidationUtils

router = APIRouter()

@router.post("/cpf_validation")
async def send_document(data: SendDocumentRequest = Depends()):

    document = data.document
    cpf_number = data.cpf_number
    file_id = UUIDUtils.generate_uuid()
    file_extension = FileUtils.extract_file_extension(document.filename)
    file_path = FileUtils.save_file(document, file_id, file_extension)
    
    try:
        matches = OCRService.extract_cpfs(file_path)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    try:
        validation = ValidationUtils.calculate_cpf_similarity(
                target_cpf=data.cpf_number, 
                matched_cpfs=matches
            )
            
        return {
            "status": "success" if validation["is_valid_match"] else "failed",
            "score": f"{validation['best_score']}%",
            "detected_cpfs": matches,
            "best_match": validation["best_match"]
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(exc)}")


