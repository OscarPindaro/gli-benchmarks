"""Register a benchmark result (pass/fail) with notes in the root README.md table.

Usage:
    uv run scripts/register_result.py <name> --status pass [--notes "..."]
    uv run scripts/register_result.py <name> --status fail [--notes "..."]
"""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCHMARKS_DIR = REPO_ROOT / "benchmarks"

from _readme_table import upsert_row  # noqa: E402

STATUS_LABELS = {
    "pass": "✅",
    "fail": "❌",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Register a benchmark pass/fail result in the README table."
    )
    parser.add_argument("name", help="Name of the benchmark to update.")
    parser.add_argument(
        "--status",
        required=True,
        choices=["pass", "fail"],
        help="Outcome of the benchmark run.",
    )
    parser.add_argument(
        "--notes",
        default="",
        help="Optional notes explaining the result (e.g. reason for failure).",
    )
    args = parser.parse_args()

    if not (BENCHMARKS_DIR / args.name).exists():
        raise SystemExit(f"Benchmark not found: {BENCHMARKS_DIR / args.name}")

    upsert_row(args.name, passed=STATUS_LABELS[args.status], notes=args.notes)
    print(f"Registered {args.status} for '{args.name}' in {REPO_ROOT / 'README.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
