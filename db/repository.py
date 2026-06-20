import sqlite3
from pathlib import Path
from typing import List, Optional
from core.models import JournalEntry


class JournalRepository:
    """
    Persistence layer for journal entries.
    Handles all database interactions.
    Business logic must NOT live here.
    """

    def __init__(self, db_path: str = "data/journal.db"):
        self.db_path = db_path
        self._initialize_database()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize_database(self):
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
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT * FROM journal_entries
                ORDER BY timestamp DESC
            """).fetchall()

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
        with self._connect() as conn:
            row = conn.execute("""
                SELECT * FROM journal_entries
                WHERE id = ?
            """, (entry_id,)).fetchone()

        if row is None:
            return None

        return JournalEntry(
            timestamp=row["timestamp"],
            market=row["market"],
            hypothesis=row["hypothesis"],
            observation=row["observation"],
            confidence=row["confidence"],
            tags=row["tags"].split(",") if row["tags"] else []
        )

    def delete_entry(self, entry_id: int) -> bool:
        with self._connect() as conn:
            cursor = conn.execute("""
                DELETE FROM journal_entries
                WHERE id = ?
            """, (entry_id,))
            conn.commit()
            return cursor.rowcount > 0