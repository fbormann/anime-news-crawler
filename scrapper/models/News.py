from dataclasses import dataclass
from datetime import date


@dataclass
class News:
    title: str
    portal_name: str
    url: str
    comment_amount: int
    word_count: int
    phrase_count: int
    paragraph_count: int
    publish_date: date

    def __init__(self):
        # because we don't necessarily want to have all fields initialized at the same time
        pass