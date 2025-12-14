from backend.features import URGENT_WORDS, SENSITIVE_WORDS
import re

def explain(text: str):
    explanations = []
    text_lower = text.lower()

    if any(w in text_lower for w in URGENT_WORDS):
        explanations.append("Linguagem de urgência identificada")

    if any(w in text_lower for w in SENSITIVE_WORDS):
        explanations.append("Solicitação de informações sensíveis")

    if re.search(r'https?://\d+\.\d+\.\d+\.\d+', text_lower):
        explanations.append("URL com endereço IP detectada")

    if text_lower.count("http") >= 3:
        explanations.append("Múltiplos links detectados")

    if not explanations:
        explanations.append("Nenhum indicador crítico identificado")

    return explanations

