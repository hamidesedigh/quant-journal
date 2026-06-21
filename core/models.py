from typing import List
from pydantic import BaseModel


class JournalEntry(BaseModel):
    """
    Domain model for a single trading journal entry.

    The service layer validates and normalizes these fields before the
    repository stores them in SQLite.
    """

    # Entry metadata and market context.
    timestamp: str
    market: str

    # Trade idea and later notes about what happened.
    hypothesis: str
    observation: str = ""

    # Confidence score is expected to be between 0 and 1.
    confidence: float = 0.5

    # Flexible labels for filtering or grouping entries later.
    tags: List[str] = []
