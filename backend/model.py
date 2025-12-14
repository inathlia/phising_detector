import pickle
from backend.features import extract_features
from backend.rules import explain

with open("backend/model.pkl", "rb") as f:
    model = pickle.load(f)

def classify_risk(score):
    if score < 10:
        return "Muito Seguro", "Nenhum risco aparente."
    if score < 25:
        return "Baixo Risco", "Conteúdo aparentemente legítimo."
    if score < 40:
        return "Levemente Suspeito", "Alguns sinais fracos detectados."
    if score < 60:
        return "Suspeito", "Vários indicadores de golpe."
    if score < 75:
        return "Alto Risco", "Alta probabilidade de phishing."
    if score < 90:
        return "Muito Alto Risco", "Golpe altamente provável."
    return "Crítico", "Golpe confirmado. NÃO interaja."

def analyze_content(text):
    features = extract_features(text)
    prob = model.predict_proba([features])[0][1]
    score = round(prob * 100, 1)

    level, message = classify_risk(score)

    return {
        "risk_percentage": score,
        "risk_level": level,
        "user_message": message,
        "explanations": explain(text)
    }

