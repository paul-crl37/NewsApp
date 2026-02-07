from pydantic import BaseModel
from datetime import datetime

class Article(BaseModel):
    title: str
    summary: str
    source: str
    date: datetime
    url: str
