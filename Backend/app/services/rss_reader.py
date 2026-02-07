import feedparser
import requests
from datetime import datetime
from email.utils import parsedate_to_datetime

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
}

# Exemples de flux RSS gratuits
RSS_FEEDS = [
    # Defense / Militaire
    {"url": "https://www.defense.gouv.fr/actualites/rss", "type": "defense", "source_name": "Defense.gouv"},

    # Le Figaro
    {"url": "https://www.lefigaro.fr/rss/figaro/politique.xml", "type": "politique", "source_name": "Le Figaro"},
    {"url": "https://www.lefigaro.fr/rss/figaro/monde.xml", "type": "defense", "source_name": "Le Figaro"},
    {"url": "https://www.lefigaro.fr/rss/figaro/economie.xml", "type": "economie", "source_name": "Le Figaro"},

    # CNews
    {"url": "https://www.cnews.fr/fr/rss", "type": "general", "source_name": "CNews"},

    # Libération
    {"url": "https://www.liberation.fr/rss/latest/", "type": "general", "source_name": "Libération"},

    # France Info
    {"url": "https://www.francetvinfo.fr/titres.rss", "type": "general", "source_name": "France Info"},

    # La Nouvelle République Indre et Loire
    {"url": "https://www.lanouvellerepublique.fr/indre-et-loire/rss", "type": "regional", "source_name": "La Nouvelle République"},

    # France Bleu
    {"url": "https://www.francebleu.fr/rss", "type": "general", "source_name": "France Bleu"},

    # Le JDD (Journal du Dimanche)
    {"url": "https://www.lejdd.fr/rss", "type": "politique", "source_name": "Le JDD"},

    # Le Monde
    {"url": "https://www.lemonde.fr/politique/rss_full.xml", "type": "politique", "source_name": "Le Monde"},
    {"url": "https://www.lemonde.fr/international/rss_full.xml", "type": "defense", "source_name": "Le Monde"},
    {"url": "https://www.lemonde.fr/economie/rss_full.xml", "type": "economie", "source_name": "Le Monde"},

    # Les Echos
    {"url": "https://www.lesechos.fr/rss/rss_une.xml", "type": "economie", "source_name": "Les Echos"},
]

def fetch_feed(url: str):
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
        response.raise_for_status()
        return feedparser.parse(response.content)
    except requests.RequestException:
        return feedparser.parse(url)


def pick_entry_date(entry):
    for key in ("published", "updated", "created"):
        value = entry.get(key)
        if value:
            return value
    return ""


def pick_entry_datetime(entry):
    for key in ("published_parsed", "updated_parsed", "created_parsed"):
        value = entry.get(key)
        if value:
            try:
                return datetime(*value[:6])
            except (TypeError, ValueError):
                continue
    text_date = pick_entry_date(entry)
    if text_date:
        try:
            return parsedate_to_datetime(text_date)
        except (TypeError, ValueError):
            return None
    return None


def get_articles_from_rss(max_articles=10, types: list = None, sources: list = None):
    articles = []
    for feed in RSS_FEEDS:
        if types and feed["type"] not in types:
            continue
        if sources and feed["source_name"] not in sources:
            continue

        feed_data = fetch_feed(feed["url"])
        for entry in feed_data.entries:
            articles.append({
                "title": entry.get("title", ""),
                "summary": entry.get("summary", entry.get("description", "")),
                "link": entry.get("link", ""),
                "published": pick_entry_date(entry),
                "published_dt": pick_entry_datetime(entry),
                "source": feed["source_name"],
                "type": feed["type"]
            })
    articles.sort(
        key=lambda item: item.get("published_dt") or datetime.min,
        reverse=True,
    )
    return articles[:max_articles]


def get_rss_status():
    status = []
    for feed in RSS_FEEDS:
        feed_data = fetch_feed(feed["url"])
        ok = not feed_data.bozo and len(feed_data.entries) > 0
        error = None
        if feed_data.bozo:
            error = str(feed_data.bozo_exception)
        elif not feed_data.entries:
            error = "Aucune entrée trouvée"
        status.append({
            "source_name": feed["source_name"],
            "type": feed["type"],
            "url": feed["url"],
            "ok": ok,
            "error": error,
        })
    return status
