"""Helpers to maintain the benchmarks table in the root README.md.

The table lives under a `## Benchmarks` heading and has three columns:
Name, Passed, Notes. Rows are keyed by benchmark name so they can be
upserted (inserted or updated) by the other scripts.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README_PATH = REPO_ROOT / "README.md"

SECTION_HEADER = "## Benchmarks"
HEADER_LINES = [
    SECTION_HEADER,
    "",
    "| Name | Passed | Notes |",
    "|------|--------|-------|",
]


def _find_section_range(lines):
    """Return (start, end) indices of the Benchmarks section.

    start is the `## Benchmarks` line, end is the next `## ` heading or EOF.
    Returns None if the section does not exist.
    """
    start = None
    for i, line in enumerate(lines):
        if line.strip() == SECTION_HEADER:
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return (start, end)


def _insert_section(lines):
    """Insert a fresh (empty) Benchmarks section before the first `## ` heading."""
    insert_at = len(lines)
    for i, line in enumerate(lines):
        if line.startswith("## "):
            insert_at = i
            break
    block = list(HEADER_LINES) + [""]
    if insert_at == 0 or lines[insert_at - 1].strip() != "":
        block = [""] + block
    return lines[:insert_at] + block + lines[insert_at:]


def _parse_rows(section_lines):
    """Extract ordered (name, passed, notes) rows from a section's lines."""
    table_lines = [l for l in section_lines if l.strip().startswith("|")]
    # skip header and separator
    body = table_lines[2:] if len(table_lines) >= 2 else []
    rows = []
    for line in body:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        rows.append((cells[0], cells[1], cells[2]))
    return rows


def upsert_row(name: str, passed: str = "", notes: str = "") -> None:
    """Insert or update the row for ``name`` in the Benchmarks table."""
    text = README_PATH.read_text() if README_PATH.exists() else ""
    lines = text.splitlines()

    rng = _find_section_range(lines)
    if rng is None:
        lines = _insert_section(lines)
        rng = _find_section_range(lines)

    start, end = rng
    rows = _parse_rows(lines[start:end])

    index_by_name = {r[0]: i for i, r in enumerate(rows)}
    if name in index_by_name:
        i = index_by_name[name]
        rows[i] = (name, passed, notes)
    else:
        rows.append((name, passed, notes))

    new_section = list(HEADER_LINES)
    for n, p, no in rows:
        new_section.append(f"| {n} | {p} | {no} |")
    if end < len(lines):
        new_section.append("")

    lines = lines[:start] + new_section + lines[end:]
    README_PATH.write_text("\n".join(lines) + "\n")
