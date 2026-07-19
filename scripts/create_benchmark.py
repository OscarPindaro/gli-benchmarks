"""Create a new benchmark scaffold inside the benchmarks/ folder.

Usage:
    uv run scripts/create_benchmark.py <name>
"""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCHMARKS_DIR = REPO_ROOT / "benchmarks"

README_TEMPLATE = """# {title}

<!-- Explain the objective of the benchmark and the expected output. -->
"""

FEATURE_TEMPLATE = """## Godot Version

4.7

## Assets

<!-- List and describe the assets required for this benchmark. -->

## Implementation

<!-- Describe the objective of the benchmark and the expected implementation. -->
"""


def create_benchmark(name: str) -> Path:
    bench_dir = BENCHMARKS_DIR / name
    assets_dir = bench_dir / "assets"
    readme_path = bench_dir / "README.md"
    feature_path = bench_dir / f"{name}.md"

    if bench_dir.exists():
        raise SystemExit(f"Benchmark already exists: {bench_dir}")

    assets_dir.mkdir(parents=True)
    title = name.replace("_", " ").title()
    readme_path.write_text(README_TEMPLATE.format(title=title))
    feature_path.write_text(FEATURE_TEMPLATE)

    return bench_dir


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a new benchmark scaffold inside benchmarks/."
    )
    parser.add_argument(
        "name",
        help="Name of the benchmark (used for the folder and feature file).",
    )
    args = parser.parse_args()

    if not args.name.isidentifier():
        raise SystemExit(
            "Name must be a valid identifier (letters, digits, underscores, "
            "not starting with a digit)."
        )

    bench_dir = create_benchmark(args.name)
    print(f"Created benchmark at {bench_dir}")
    print(f"  - {bench_dir / 'assets'}")
    print(f"  - {bench_dir / 'README.md'}")
    print(f"  - {bench_dir / f'{args.name}.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
