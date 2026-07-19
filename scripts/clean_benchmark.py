"""Delete generated files from a benchmark folder, keeping only the scaffold.

The scaffold created by `create_benchmark.py` is:
  - README.md
  - <name>.md
  - assets/  (source assets; Godot-generated .import files are removed)

Everything else (project.godot, scenes, scripts, .godot/, etc.) is removed so
the benchmark can be re-run from a clean state.

Usage:
    uv run scripts/clean_benchmark.py <name>
    uv run scripts/clean_benchmark.py --all
"""

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCHMARKS_DIR = REPO_ROOT / "benchmarks"


def _scaffold_files(name: str):
    """Return the set of paths preserved by create_benchmark for ``name``."""
    bench_dir = BENCHMARKS_DIR / name
    return {
        bench_dir / "README.md",
        bench_dir / f"{name}.md",
    }


def clean_benchmark(name: str, dry_run: bool = False) -> list[Path]:
    """Remove generated files for one benchmark. Returns the removed paths."""
    bench_dir = BENCHMARKS_DIR / name
    if not bench_dir.exists():
        raise SystemExit(f"Benchmark not found: {bench_dir}")

    preserved_files = _scaffold_files(name)
    preserved_dirs = {bench_dir / "assets"}
    removed: list[Path] = []

    for entry in sorted(bench_dir.iterdir(), reverse=False):
        if entry in preserved_files:
            continue
        if entry in preserved_dirs:
            # keep source assets, drop Godot-generated .import files
            for asset in sorted(entry.rglob("*")):
                if asset.is_file() and asset.suffix == ".import":
                    if dry_run:
                        removed.append(asset)
                    else:
                        asset.unlink()
                        removed.append(asset)
            continue
        if dry_run:
            removed.append(entry)
        else:
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry)
            else:
                entry.unlink()
            removed.append(entry)

    return removed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove generated files from benchmark folders, keeping the scaffold."
    )
    parser.add_argument("name", nargs="?", help="Name of the benchmark to clean.")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Clean every benchmark under benchmarks/.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List what would be removed without deleting anything.",
    )
    args = parser.parse_args()

    if not args.all and not args.name:
        parser.error("provide a benchmark name or use --all")

    if args.all:
        names = sorted(
            p.name for p in BENCHMARKS_DIR.iterdir() if p.is_dir()
        )
    else:
        names = [args.name]

    for name in names:
        removed = clean_benchmark(name, dry_run=args.dry_run)
        label = "Would remove" if args.dry_run else "Removed"
        print(f"{label} from {BENCHMARKS_DIR / name}:")
        for p in removed:
            print(f"  - {p.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
