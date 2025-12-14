import pandas as pd
from pathlib import Path

def normalize_label(label):
    if label in (1, "1", "phishing", "spam", "malicious"):
        return 1
    if label in (0, "0", "legitimate", "ham", "benign"):
        return 0
    raise ValueError(f"Unknown label: {label}")

def load_datasets():
    texts = []
    labels = []

    # SMS Spam
    sms = pd.read_csv(
        "data/sms_spam.csv",
        sep="\t",
        names=["label", "text"],
        dtype=str
    )
    for _, r in sms.iterrows():
        texts.append(r["text"])
        labels.append(normalize_label(r["label"]))

    # Enron legit emails
    emails = pd.read_csv("data/enron_legit.csv", dtype=str)
    for _, r in emails.iterrows():
        texts.append(r["message"])
        labels.append(0)

    # URLs
    for p in Path("data/domains").glob("*.txt"):
        texts.append(p.read_text(errors="ignore"))
        labels.append(1)

    return texts, labels

