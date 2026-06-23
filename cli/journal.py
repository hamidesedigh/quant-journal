"""
Command-line interface for the Quant Journal application.

This file defines the user-facing commands, parses terminal arguments, and
passes valid requests into the journal service layer.
"""

import argparse
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from db.repository import JournalRepository
from services.journal_service import JournalService
from services.report_service import ReportService


def main():
    """
    Run the journal CLI.

    The function creates the repository and service objects, defines available
    commands, reads the user's command-line input, and prints command results.
    """

    # Application wiring: connect the CLI to the service and database layers.
    repo = JournalRepository()
    service = JournalService(repo)

    # CLI parser setup: defines the main command group for journal actions.
    parser = argparse.ArgumentParser(description="Quant Journal CLI")

    subparsers = parser.add_subparsers(dest="command")

    # Add command: captures the required fields for a new journal entry.
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--market", required=True)
    add_parser.add_argument("--hypothesis", required=True)
    add_parser.add_argument("--confidence", type=float, default=0.5)
    add_parser.add_argument("--tags", default="")

    # List command: prints existing journal entries from newest to oldest.
    subparsers.add_parser("list")

    # Report command: prints a summary of the current journal entries.
    subparsers.add_parser("report")

    args = parser.parse_args()

    # Command dispatch: route parsed CLI input to the matching service method.
    if args.command == "add":
        tags = args.tags.split(",") if args.tags else []

        entry_id = service.create_entry(
            market=args.market,
            hypothesis=args.hypothesis,
            confidence=args.confidence,
            tags=tags
        )

        print(f"[OK] Entry created with ID: {entry_id}")

    elif args.command == "list":
        entries = service.get_entries()

        if not entries:
            print("No journal entries found.")
        else:
            for i, entry in enumerate(entries, start=1):
                print(f"\nEntry #{i}")
                print("-" * 40)
                print(f"Timestamp : {entry.timestamp}")
                print(f"Market    : {entry.market}")
                print(f"Hypothesis: {entry.hypothesis}")
                print(f"Observation: {entry.observation}")
                print(f"Confidence: {entry.confidence}")
                print(f"Tags      : {', '.join(entry.tags)}")
    
    elif args.command == "report":
        report_service = ReportService(repo)
        print(report_service.generate_daily_report())

    else:
        # Default output: show available commands when no command is selected.
        parser.print_help()


if __name__ == "__main__":
    # Script entry point for direct execution with python cli/journal.py.
    main()
