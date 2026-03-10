import re
from pathlib import Path
import cv2
import pytesseract
import numpy as np
from pdf2image import convert_from_path

class OCRService:
    # Regex flexível para capturar CPFs com pontos, traços ou espaços
    cpf_pattern = r"\d{3}[.\s]?\d{3}[.\s]?\d{3}[-\s]?\d{2}"
    
    # Caminho do poppler (ajuste se necessário para seu ambiente de produção)
    POPPLER_PATH = r"C:\poppler-25.12.0\Library\bin"

    @staticmethod
    def preprocess_image(image):
        """
        Aplica técnicas de Visão Computacional para melhorar a leitura do OCR.
        """
        # 1. Escala de cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 2. Redimensionamento (FX/FY = 2.0 dobra o tamanho da imagem)
        # Isso é crucial para documentos digitalizados com DPI baixo.
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # 3. Remoção de ruído leve
        blur = cv2.GaussianBlur(gray, (3, 3), 0)

        # 4. Binarização de Otsu (Calcula o threshold ideal automaticamente)
        processed = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        return processed

    @staticmethod
    def clean_ocr_text(text: str) -> str:
        """
        Corrige confusões comuns do motor de OCR.
        """
        corrections = {
            "O": "0", "D": "0", "I": "1", 
            "l": "1", "/": "7", "S": "5", "B": "8"
        }
        for wrong, correct in corrections.items():
            text = text.replace(wrong, correct)
        return text

    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        """
        Algoritmo oficial de validação de dígitos verificadores do CPF.
        """
        cpf = re.sub(r"\D", "", cpf)

        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        for i in range(9, 11):
            value = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
            digit = ((value * 10) % 11) % 10
            if digit != int(cpf[i]):
                return False
        return True

    @classmethod
    def extract_text_from_image(cls, image_cv) -> str:
        """
        Extrai texto de um objeto de imagem OpenCV.
        """
        processed = cls.preprocess_image(image_cv)
        
        # PSM 11: Texto esparso (bom para encontrar números perdidos na página)
        # PSM 3: Totalmente automático (bom para documentos estruturados)
        config = "--oem 3 --psm 3" 
        
        text = pytesseract.image_to_string(processed, lang="por", config=config)
        print(f"Texto extraído: {text}")
        return text

    @classmethod
    def extract_cpfs(cls, file_path: str):
        """
        Método principal: Orquestra a abertura do arquivo e extração de CPFs.
        """
        path = Path(file_path)
        full_text = ""

        if path.suffix.lower() == ".pdf":
            # Converte PDF para lista de imagens PIL
            images = convert_from_path(
                file_path, 
                dpi=300, 
                poppler_path=cls.POPPLER_PATH
            )
            for img in images:
                # Converte PIL para OpenCV
                img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                full_text += cls.extract_text_from_image(img_cv) + "\n"
        else:
            img_cv = cv2.imread(file_path)
            if img_cv is None:
                return []
            full_text = cls.extract_text_from_image(img_cv)
            print(f"Texto completo extraído: {full_text}")

        # Tratamento pós-OCR
        clean_text = cls.clean_ocr_text(full_text)
        print(f"Texto limpo: {clean_text}")
        matches = re.findall(cls.cpf_pattern, clean_text)

        cpfs_validos = []
        for match in matches:
            digits_only = re.sub(r"\D", "", match)
            if cls.validate_cpf(digits_only):
                cpfs_validos.append(digits_only)

        # Retorna lista sem duplicatas
        return list(set(cpfs_validos))