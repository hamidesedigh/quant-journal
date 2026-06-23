"""
Report generation for journal entries.

This module summarizes existing journal records into a simple daily report
that can be printed by the CLI.
"""

from datetime import datetime

from core.models import DailyReport
from db.repository import JournalRepository


class ReportService:
    """
    Build report summaries from journal entries.
    """

    def __init__(self, repository: JournalRepository):
        """
        Store the repository used to read journal entries.
        """

        self.repository = repository

    def generate_daily_report(self) -> str:
        """
        Return a printable report for the currently stored journal entries.
        """

        report = self._build_daily_report()

        lines = [
            f"Daily Report: {report.date}",
            "-" * 40,
            f"Total entries : {report.total_entries}",
            f"Markets       : {', '.join(report.markets) if report.markets else '-'}",
            f"Avg confidence: {report.avg_confidence:.2f}",
            "",
            "Hypotheses:",
        ]

        if report.hypotheses:
            lines.extend(f"- {hypothesis}" for hypothesis in report.hypotheses)
        else:
            lines.append("- No journal entries found.")

        return "\n".join(lines)

    def _build_daily_report(self) -> DailyReport:
        """
        Aggregate all journal entries into a DailyReport model.
        """

        entries = self.repository.get_all_entries()
        total_entries = len(entries)

        if total_entries == 0:
            avg_confidence = 0.0
        else:
            avg_confidence = sum(entry.confidence for entry in entries) / total_entries

        markets = sorted({entry.market for entry in entries})
        hypotheses = [entry.hypothesis for entry in entries]

        return DailyReport(
            date=datetime.now().date().isoformat(),
            total_entries=total_entries,
            markets=markets,
            avg_confidence=avg_confidence,
            hypotheses=hypotheses,
        )
