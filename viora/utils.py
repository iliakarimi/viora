import re

def clean_urls(text: str) -> str:
    return re.sub(r'https?://\S+', '', text)
