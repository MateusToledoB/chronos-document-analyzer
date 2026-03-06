from fastapi import UploadFile, File, Form

class SendDocumentRequest:
    def __init__(
        self,
        document: UploadFile = File(...),
        cpf_number: str = Form(...)
    ):
        self.document = document
        self.cpf_number = cpf_number
