import feedparser

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

def get_articles_from_rss(max_articles=10, types: list = None, sources: list = None):
    articles = []
    for feed in RSS_FEEDS:
        if types and feed["type"] not in types:
            continue
        if sources and feed["source_name"] not in sources:
            continue

        feed_data = feedparser.parse(feed["url"])
        for entry in feed_data.entries[:max_articles]:
            articles.append({
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "source": feed["source_name"],
                "type": feed["type"]
            })
    return articles


def get_rss_status():
    status = []
    for feed in RSS_FEEDS:
        feed_data = feedparser.parse(feed["url"])
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
