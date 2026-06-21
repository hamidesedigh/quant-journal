from datetime import datetime
from typing import List, Optional
from core.models import JournalEntry
from db.repository import JournalRepository


class JournalService:
    """
    Business logic layer.
    Responsible for:
    - validation
    - normalization
    - domain workflows
    """

    def __init__(self, repository: JournalRepository):
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

        # Normalize optional collection fields before validation and storage.
        if tags is None:
            tags = []

        # Validate user-provided fields before constructing the domain model.
        self._validate_market(market)
        self._validate_confidence(confidence)
        self._validate_hypothesis(hypothesis)

        # Build the canonical entry representation used by the rest of the app.
        entry = JournalEntry(
            timestamp=datetime.utcnow().isoformat(),
            market=market.upper(),
            hypothesis=hypothesis.strip(),
            observation=observation.strip(),
            confidence=confidence,
            tags=tags
        )

        return self.repository.create_entry(entry)

    # Read operations: expose repository queries through the service layer.
    def get_entries(self) -> List[JournalEntry]:
        return self.repository.get_all_entries()

    def get_entry(self, entry_id: int) -> Optional[JournalEntry]:
        return self.repository.get_entry_by_id(entry_id)

    def delete_entry(self, entry_id: int) -> bool:
        return self.repository.delete_entry(entry_id)

    # Validation helpers: keep domain constraints close to entry creation.
    def _validate_market(self, market: str):
        if not market or len(market.strip()) < 2:
            raise ValueError("Invalid market symbol")

    def _validate_confidence(self, confidence: float):
        if not (0 <= confidence <= 1):
            raise ValueError("Confidence must be between 0 and 1")

    def _validate_hypothesis(self, hypothesis: str):
        if not hypothesis or len(hypothesis.strip()) < 5:
            raise ValueError("Hypothesis too short")
