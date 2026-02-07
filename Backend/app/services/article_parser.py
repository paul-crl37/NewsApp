from bs4 import BeautifulSoup

def clean_html(text):
    """Supprime le HTML pour obtenir un texte pur"""
    return BeautifulSoup(text, "html.parser").get_text()
