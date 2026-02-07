from nltk.tokenize import sent_tokenize

def summarize_text(text, sentences_count=3):
    # Découper le texte en phrases avec NLTK
    sentences = sent_tokenize(text, language="french")  # français
    # Prendre les premières phrases
    summary = sentences[:sentences_count]
    return " ".join(summary)
