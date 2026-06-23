"""
Business logic for journal entries.

This module receives raw values from the CLI, validates them, normalizes them
into consistent domain models, and delegates storage to the repository layer.
"""

from datetime import datetime
from typing import List, Optional
from core.models import JournalEntry
from db.repository import JournalRepository


# JournalService is the main application layer between the CLI and database.
class JournalService:
    """
    Business logic layer.
    Responsible for:
    - validation
    - normalization
    - domain workflows
    """

    def __init__(self, repository: JournalRepository):
        """
        Store the repository used for all journal persistence operations.
        """

        # Repository dependency keeps persistence separate from business rules.
        self.repository = repository

    def create_entry(
        self,
        market: str,
        hypothesis: str,
        observation: str = "",
        confidence: float = 0.5,
        tags: Optional[List[str]] = None
    ) -> int:
        """
        Validate and create a new journal entry.

        Returns the database ID of the newly stored entry.
        """

        # Normalize optional collection fields before validation and storage.
        if tags is None:
            tags = []

        # Validate user-provided fields before constructing the domain model.
        self._validate_market(market)
        self._validate_confidence(confidence)
        self._validate_hypothesis(hypothesis)

        # Build the canonical entry representation used by the rest of the app.
        entry = JournalEntry(
            timestamp=datetime.now().isoformat(),
            market=market.upper(),
            hypothesis=hypothesis.strip(),
            observation=observation.strip(),
            confidence=confidence,
            tags=tags
        )

        return self.repository.create_entry(entry)

    # Read operations: expose repository queries through the service layer.
    def get_entries(self) -> List[JournalEntry]:
        """
        Return all journal entries ordered by the repository query.
        """

        return self.repository.get_all_entries()

    def get_entry(self, entry_id: int) -> Optional[JournalEntry]:
        """
        Return one journal entry by ID, or None when it does not exist.
        """

        return self.repository.get_entry_by_id(entry_id)

    def delete_entry(self, entry_id: int) -> bool:
        """
        Delete a journal entry by ID.

        Returns True when a row was deleted and False when no row matched.
        """

        return self.repository.delete_entry(entry_id)

    # Validation helpers: keep domain constraints close to entry creation.
    def _validate_market(self, market: str):
        """
        Ensure the market symbol is present and long enough to be meaningful.
        """

        if not market or len(market.strip()) < 2:
            raise ValueError("Invalid market symbol")

    def _validate_confidence(self, confidence: float):
        """
        Ensure the confidence score is inside the accepted 0 to 1 range.
        """

        if not (0 <= confidence <= 1):
            raise ValueError("Confidence must be between 0 and 1")

    def _validate_hypothesis(self, hypothesis: str):
        """
        Ensure the trading hypothesis contains enough detail to be useful.
        """

        if not hypothesis or len(hypothesis.strip()) < 5:
            raise ValueError("Hypothesis too short")
