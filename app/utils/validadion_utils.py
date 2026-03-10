from rapidfuzz import fuzz
import re

class ValidationUtils:
    
    @staticmethod
    def clean_cpf(cpf: str) -> str:
        """Remove qualquer caractere que não seja número."""
        return re.sub(r"\D", "", cpf)

    @classmethod
    def calculate_cpf_similarity(cls, target_cpf: str, matched_cpfs: list[str]) -> dict:
        """
        Compara um CPF alvo com uma lista de CPFs encontrados.
        Retorna o melhor score e o CPF correspondente.
        """
        target_cleaned = cls.clean_cpf(target_cpf)
        
        if not matched_cpfs:
            return {
                "best_score": 0,
                "best_match": None,
                "is_valid_match": False
            }

        # Calcula o score para cada match encontrado
        # fuzz.ratio compara a similaridade entre as strings (0 a 100)
        results = []
        for match in matched_cpfs:
            match_cleaned = cls.clean_cpf(match)
            score = fuzz.ratio(target_cleaned, match_cleaned)
            results.append({"cpf": match_cleaned, "score": score})

        # Ordena para pegar o maior score
        best_result = max(results, key=lambda x: x["score"])
        
        # Definimos um threshold (limiar) de 90% para considerar um "sucesso"
        # Isso tolera erro de 1 dígito lido errado pelo OCR
        is_valid = best_result["score"] >= 90

        return {
            "best_score": round(best_result["score"], 2),
            "best_match": best_result["cpf"],
            "is_valid_match": is_valid,
            "all_scores": results
        }