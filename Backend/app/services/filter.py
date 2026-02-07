from datetime import datetime

def filter_by_date(articles, date_start=None, date_end=None):
    if not date_start and not date_end:
        return articles
    filtered = []
    for art in articles:
        try:
            pub_date = datetime.strptime(art["published"], "%a, %d %b %Y %H:%M:%S %Z")
        except:
            pub_date = None
        if pub_date:
            if date_start and pub_date < date_start:
                continue
            if date_end and pub_date > date_end:
                continue
        filtered.append(art)
    return filtered
