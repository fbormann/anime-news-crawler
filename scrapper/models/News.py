from dataclasses import dataclass
from datetime import date


@dataclass
class News:
    title: str
    url: str
    comment_amount: int
    word_count: int
    phrase_count: int
    paragraph_count: int
    publish_date: date
