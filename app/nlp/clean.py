import re
import nltk
from nltk.corpus import stopwords

# Download once
nltk.download("stopwords", quiet=True)

STOP_WORDS = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    words = [w for w in text.split() if w not in STOP_WORDS]
    return " ".join(words)
