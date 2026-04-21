"""
Print column names (and optional row count) for a CSV file.
Usage:
  python scripts/read_csv_columns.py
  python scripts/read_csv_columns.py archive/cities.csv
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Read CSV header row.")
    parser.add_argument(
        "csv_path",
        nargs="?",
        default=root / "archive" / "cities.csv",
        type=Path,
        help="Path to CSV (default: archive/cities.csv)",
    )
    parser.add_argument(
        "-n",
        "--count-rows",
        action="store_true",
        help="Count data rows (excluding header).",
    )
    args = parser.parse_args()

    path: Path = args.csv_path
    if not path.is_file():
        raise SystemExit(f"File not found: {path}")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        n = 0
        if args.count_rows:
            for _ in reader:
                n += 1

    print(path.resolve())
    print("columns:", len(header))
    for i, name in enumerate(header):
        print(f"  [{i}] {name}")
    if args.count_rows:
        print("data_rows:", n)


if __name__ == "__main__":
    main()
