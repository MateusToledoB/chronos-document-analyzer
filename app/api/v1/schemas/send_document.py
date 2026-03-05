from fastapi import UploadFile, File, Form

class SendDocumentRequest:
    def __init__(
        self,
        document: UploadFile = File(...),
        file_type: str = Form(...)
    ):
        self.document = document
        self.file_type = file_type