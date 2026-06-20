from typing import List
from pydantic import BaseModel


class JournalEntry(BaseModel):
    timestamp: str
    market: str
    hypothesis: str
    observation: str = ""
    confidence: float = 0.5
    tags: List[str] = []