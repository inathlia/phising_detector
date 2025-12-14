import re
import math
from collections import Counter
import tldextract
from urllib.parse import urlparse

URGENT_WORDS = [
    "urgent", "immediately", "suspend", "verify",
    "expire", "limited", "act now", "blocked"
]

SENSITIVE_WORDS = [
    "password", "credit card", "bank", "ssn",
    "cpf", "account", "login", "verify identity"
]

URL_SHORTENERS = ["bit.ly", "tinyurl", "t.co", "goo.gl"]

BRAND_WORDS = ["paypal", "google", "apple", "amazon", "microsoft"]

def entropy(s):
    probs = [n / len(s) for n in Counter(s).values()]
    return -sum(p * math.log2(p) for p in probs)

def extract_features(text: str):
    t = text.lower()
    urls = re.findall(r'https?://\S+', t)

    features = {
        "length": len(t),
        "num_urls": len(urls),
        "num_digits": sum(c.isdigit() for c in t),
        "num_upper": sum(c.isupper() for c in text),
        "entropy": entropy(t) if len(t) > 0 else 0,
        "urgent_terms": sum(w in t for w in URGENT_WORDS),
        "sensitive_terms": sum(w in t for w in SENSITIVE_WORDS),
        "brand_terms": sum(w in t for w in BRAND_WORDS),
        "has_ip_url": any(re.search(r'https?://\d+', u) for u in urls),
        "multiple_links": int(len(urls) >= 3),
        "contains_at": int("@" in t),
        "excessive_punctuation": t.count("!") + t.count("?"),
        "html_form": int("<form" in t),
    }

    return list(features.values())
