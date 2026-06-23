"""
Shared data models for the Quant Journal application.

Models in this file describe the shape of data that moves between the CLI,
service layer, and database repository.
"""

from typing import List
from pydantic import BaseModel


# JournalEntry contains the complete structured data for one journal record.
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


class DailyReport(BaseModel):
    """
    Summary model for journal activity across all stored entries.
    """

    date: str
    total_entries: int
    markets: List[str]
    avg_confidence: float
    hypotheses: List[str]
