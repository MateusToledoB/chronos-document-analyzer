import re
from pathlib import Path
import numpy as np
from pdf2image import convert_from_path
import easyocr

class OCRValidateCPFService:
    LANGUAGE = 'pt'
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.reader = easyocr.Reader([cls.LANGUAGE], gpu=False)
        return cls._instance

