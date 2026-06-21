"""
SQLite repository for journal entries.

This module owns database setup and CRUD operations for the journal entry table.
It converts between SQLite rows and the JournalEntry domain model.
"""

import sqlite3
from pathlib import Path
from typing import List, Optional
from core.models import JournalEntry


# JournalRepository isolates persistence details from the rest of the app.
class JournalRepository:
    """
    Persistence layer for journal entries.
    Handles all database interactions.
    Business logic must NOT live here.
    """

    def __init__(self, db_path: str = "data/journal.db"):
        """
        Configure the database location and make sure the schema exists.
        """

        # Database path can be overridden by tests or future configuration.
        self.db_path = db_path
        self._initialize_database()

    def _connect(self):
        """
        Open a SQLite connection with rows addressable by column name.
        """

        # Row factory allows column access by name when hydrating models.
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize_database(self):
        """
        Create the data directory and journal table when they do not exist.
        """

        # Schema setup: create the data directory and journal table if needed.
        Path("data").mkdir(exist_ok=True)

        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS journal_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    market TEXT NOT NULL,
                    hypothesis TEXT NOT NULL,
                    observation TEXT,
                    confidence REAL,
                    tags TEXT
                )
            """)
            conn.commit()

    def create_entry(self, entry: JournalEntry) -> int:
        """
        Store one journal entry and return the new database row ID.
        """

        # Insert a validated journal entry and return its generated row ID.
        with self._connect() as conn:
            cursor = conn.execute("""
                INSERT INTO journal_entries (
                    timestamp,
                    market,
                    hypothesis,
                    observation,
                    confidence,
                    tags
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                entry.timestamp,
                entry.market,
                entry.hypothesis,
                entry.observation,
                entry.confidence,
                ",".join(entry.tags)
            ))
            conn.commit()
            return cursor.lastrowid

    def get_all_entries(self) -> List[JournalEntry]:
        """
        Load every journal entry from SQLite as JournalEntry objects.
        """

        # Fetch newest entries first so recent journal context appears on top.
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT * FROM journal_entries
                ORDER BY timestamp DESC
            """).fetchall()

        # Convert SQLite rows back into domain models for callers.
        entries = []
        for row in rows:
            entries.append(
                JournalEntry(
                    timestamp=row["timestamp"],
                    market=row["market"],
                    hypothesis=row["hypothesis"],
                    observation=row["observation"],
                    confidence=row["confidence"],
                    tags=row["tags"].split(",") if row["tags"] else []
                )
            )

        return entries

    def get_entry_by_id(self, entry_id: int) -> Optional[JournalEntry]:
        """
        Load a single journal entry by ID.

        Returns None when the ID does not exist.
        """

        # Look up one entry by its database identifier.
        with self._connect() as conn:
            row = conn.execute("""
                SELECT * FROM journal_entries
                WHERE id = ?
            """, (entry_id,)).fetchone()

        if row is None:
            return None

        # Hydrate the row into the same model shape used by list queries.
        return JournalEntry(
            timestamp=row["timestamp"],
            market=row["market"],
            hypothesis=row["hypothesis"],
            observation=row["observation"],
            confidence=row["confidence"],
            tags=row["tags"].split(",") if row["tags"] else []
        )

    def delete_entry(self, entry_id: int) -> bool:
        """
        Delete one journal entry by ID and report whether deletion happened.
        """

        # Return whether a row was actually removed.
        with self._connect() as conn:
            cursor = conn.execute("""
                DELETE FROM journal_entries
                WHERE id = ?
            """, (entry_id,))
            conn.commit()
            return cursor.rowcount > 0
