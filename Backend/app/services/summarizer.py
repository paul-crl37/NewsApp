from nltk.tokenize import sent_tokenize

def summarize_text(text, sentences_count=3):
    if not text:
        return ""
    try:
        # Découper le texte en phrases avec NLTK
        sentences = sent_tokenize(text, language="french")  # français
    except LookupError:
        # Fallback simple si les ressources NLTK ne sont pas disponibles
        sentences = [sentence.strip() for sentence in text.split(".") if sentence.strip()]
    # Prendre les premières phrases
    summary = sentences[:sentences_count]
    return " ".join(summary)
