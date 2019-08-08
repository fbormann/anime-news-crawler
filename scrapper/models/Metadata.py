from dataclasses import dataclass
from datetime import datetime


@dataclass
class Metadata:
    root_url: str
    date: datetime
    status: bool
