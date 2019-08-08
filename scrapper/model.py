from dataclasses import dataclass
from datetime import datetime

@dataclass
class News:
    title: str
    url: str
    comment_amount: int
    word_count: int
    phrase_count: int
    paragraph_count: int


@dataclass
class Metadata:
    root_url: str
    date: datetime
    status: bool
