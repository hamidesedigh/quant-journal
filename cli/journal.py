import argparse
from db.repository import JournalRepository
from services.journal_service import JournalService


def main():
    repo = JournalRepository()
    service = JournalService(repo)

    parser = argparse.ArgumentParser(description="Quant Journal CLI")

    subparsers = parser.add_subparsers(dest="command")

    # ADD ENTRY
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--market", required=True)
    add_parser.add_argument("--hypothesis", required=True)
    add_parser.add_argument("--confidence", type=float, default=0.5)
    add_parser.add_argument("--tags", default="")

    # LIST
    subparsers.add_parser("list")

    args = parser.parse_args()

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
        for e in entries:
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

    else:
        parser.print_help()


if __name__ == "__main__":
    main()