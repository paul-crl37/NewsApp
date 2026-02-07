from fastapi import APIRouter, Query
from typing import List, Optional
from datetime import datetime
from email.utils import parsedate_to_datetime
from ..services.rss_reader import get_articles_from_rss
from ..services.article_parser import clean_html
from ..services.summarizer import summarize_text
from ..services.filter import filter_by_date
from ..models.article import Article

router = APIRouter()

@router.get("/", response_model=List[Article])
def get_news(
    date_start: Optional[str] = Query(None),
    date_end: Optional[str] = Query(None),
    max_articles: int = Query(10),
    types: Optional[List[str]] = Query(None, description="Liste des types (defense, politique, economie, etc.)"),
    sources: Optional[List[str]] = Query(None, description="Liste des sites (Le Figaro, Le Monde, etc.)")
):
    # Convertir les dates
    date_start = date_start or None
    date_end = date_end or None
    ds = datetime.strptime(date_start, "%Y-%m-%d") if date_start else None
    de = datetime.strptime(date_end, "%Y-%m-%d") if date_end else None

    # Récupérer articles RSS avec filtres types et sources
    articles_raw = get_articles_from_rss(max_articles=max_articles, types=types, sources=sources)

    # Filtrer par date
    articles_filtered = filter_by_date(articles_raw, ds, de)

    # Créer liste finale avec résumé
    final_articles = []
    for art in articles_filtered:
        text = clean_html(art.get("summary", ""))
        summary = summarize_text(text, sentences_count=3)
        final_articles.append(Article(
            title=art["title"],
            summary=summary,
            source=art["source"],
            date=parsedate_to_datetime(art["published"]) if art.get("published") else datetime.now(),
            url=art["link"],
            type=art.get("type", "general")  # Ajouter le type à l'article
        ))
    return final_articles
