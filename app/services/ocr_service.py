import os
import re

import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\mateus.benkenstein\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

os.environ["TESSDATA_PREFIX"] = r"C:\Users\mateus.benkenstein\AppData\Local\Programs\Tesseract-OCR\tessdata"


class OCRService:
    @staticmethod
    def extract_cpf(file_path):
        extension = os.path.splitext(file_path)[1].lower()
        if extension == ".pdf":
            text = OCRService._extract_text_from_pdf(file_path)
        else:
            text = OCRService._extract_text_from_image(file_path)

        cpf_pattern = r"\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11}"
        matches = re.findall(cpf_pattern, text)
        return matches

    @staticmethod
    def _extract_text_from_image(file_path):
        # cv2.imread returns None for unsupported/corrupt files.
        image = cv2.imread(file_path)
        if image is None:
            raise ValueError(
                "Unable to read uploaded file as an image. "
                "Supported formats: .png, .jpg, .jpeg, .bmp, .tiff, .tif, .webp"
            )

        return OCRService._ocr_image(image)

    @staticmethod
    def _extract_text_from_pdf(file_path):
        try:
            import fitz  # PyMuPDF
        except ImportError as exc:
            raise ValueError(
                "PDF support requires PyMuPDF. Install dependency 'pymupdf'."
            ) from exc

        text_parts = []
        with fitz.open(file_path) as document:
            for page in document:
                page_text = page.get_text("text") or ""
                if page_text.strip():
                    text_parts.append(page_text)
                    continue

                # If page has no embedded text, render and apply OCR.
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                image_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                    pix.height,
                    pix.width,
                    pix.n,
                )
                if pix.n == 4:
                    image_array = cv2.cvtColor(image_array, cv2.COLOR_BGRA2BGR)
                text_parts.append(OCRService._ocr_image(image_array))

        return "\n".join(text_parts)

    @staticmethod
    def _ocr_image(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )[1]

        return pytesseract.image_to_string(thresh, lang="por")
