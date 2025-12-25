import unidecode

def normalize_czech_text(text: str) -> str:
    """
    Normalizes Czech text for searching/matching.
    - Lowercase
    - Remove diacritics (háčky/čárky)
    - Strip whitespace
    """
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove diacritics
    text = unidecode.unidecode(text)
    
    return text.strip()
