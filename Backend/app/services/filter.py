from datetime import datetime
from email.utils import parsedate_to_datetime

def filter_by_date(articles, date_start=None, date_end=None):
    if not date_start and not date_end:
        return articles
    filtered = []
    for art in articles:
        pub_date = None
        published_raw = art.get("published")
        if published_raw:
            try:
                pub_date = parsedate_to_datetime(published_raw)
            except (TypeError, ValueError):
                pub_date = None
        if pub_date:
            if date_start and pub_date < date_start:
                continue
            if date_end and pub_date > date_end:
                continue
        filtered.append(art)
    return filtered
